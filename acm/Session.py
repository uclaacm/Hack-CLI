from Module import Module
from Global import check
import Global, Crypt
import requests, pprint, ast, copy

class Session(Module):
	def __init__(self, cmd, cmd_args):
		self.cmd_map = {
			"list": self.list,
			"details": self.details,
			"add": self.add,
			"update" : self.update,
			"delete" : self.delete
		}
		Module.__init__(self, cmd, cmd_args)

	def list(self):
		r = requests.get(Global.makeURL("/api/v1/session?token=%s"%Crypt.getToken()))
		check(r.status_code == 200, "Malformed request to GET /api/v1/session")

		data = r.json()
		print("Hack School Session List")
		print("==========")
		if len(data["sessions"]) == 0:
			print "No sessions"
		else:
			for session in data["sessions"]:
				self.printSessionObject(session, fields=["id", "name", "number"])

		return data["sessions"] if len(data["sessions"]) > 0 else None

	def details(self):
		check(len(self.cmd_args) > 0, "Getting session details requires a session ID")

		r = requests.get(Global.makeURL("/api/v1/session/%s"%self.cmd_args[0]))
		check(r.status_code == 200, "Malformed request to GET /api/v1/session/%s"%self.cmd_args[0])

		data = r.json()
		check(len(data["sessions"]) > 0, "No session with ID '%s' found"%self.cmd_args[0])

		print("Hack School Session Details")
		print("=============")
		self.printSessionObject(data["sessions"][0])

		return data["sessions"][0]

	def add(self):
		print("Creating new Hack School Session...")
		obj = {
			"session" : {
				"number": int(raw_input("(required) session number: ")),
				"name": raw_input("(required) session title: "),
				"secret": raw_input("(required) attendence secret: "),
				"desc": raw_input("(required) desc: "),
				"image": raw_input("(required) image: "),
				"date": {
					"start": Global.getDateInput("(required) date.start"),
					"end": Global.getDateInput("(required) date.end")
				},
				"blogPostLink": raw_input("(optional) blogPostLink: "),
				"project": {
					"points": raw_input("(optional) project.points: "),
					"videoLink": raw_input("(optional) project.videoLink: "),
					"slidesLink": raw_input("(optional) project.slidesLink: "),
					"submissionLink": raw_input("(optional) project.submissionLink: ")
				}
			}
		}

		obj = Global.trimDict(obj)
		self.printSessionObject(obj["session"])
		choice = raw_input("Create this session? [y/n]: ")
		check(choice == "y", "Aborted.")

		r = requests.post(Global.makeURL("/api/v1/session"), json=Global.makeData(obj))
		if (r.status_code == 200 and r.json()["success"]):
			print("Your session has been successfully created.")
		else:
			print("There was a error creating your session:")
			pprint.pprint(r.json()["error"])

		return r.json() if r.status_code == 200 else None

	def update(self):
		check(len(self.cmd_args) > 0, "Updating a session requires a session ID")

		r = requests.get(Global.makeURL("/api/v1/session/%s"%self.cmd_args[0]))
		response = r.json()
		check(r.status_code == 200 and response["success"] and len(response["sessions"]) > 0, \
			"No session with id '%s' found."%self.cmd_args[0])

		print("Current session data:")
		self.printSessionObject(response["sessions"][0])
		print("You will now be prompted to update this session")
		print(" - Only fill out fields you want to change")
		print(" - To leave a field unchanged, press 'enter'")

		obj = {
			"session" : {
				"number": int(raw_input("session number: ")),
				"name": raw_input("session title: "),
				"secret": raw_input("attendence secret: "),
				"desc": raw_input("desc: "),
				"image": raw_input("image: "),
				"date": {
					"start": Global.getDateInput("date.start"),
					"end": Global.getDateInput("date.end")
				},
				"blogPostLink": raw_input("blogPostLink: "),
				"project": {
					"points": raw_input("project.points: "),
					"videoLink": raw_input("project.videoLink: "),
					"slidesLink": raw_input("project.slidesLink: "),
					"submissionLink": raw_input("project.submissionLink: ")
				}
			}
		}

		obj["session"] = Global.trimDict(obj["session"])
		print("---")
		print("Project changes:")
		self.printSessionObject(obj["session"])

		choice = raw_input("Make these changes? [y/n]: ")
		check(choice == "y", "Aborted.")

		r = requests.patch(Global.makeURL("/api/v1/session/%s"%self.cmd_args[0]), json=Global.makeData(obj))
		if (r.status_code == 200 and r.json()["success"]):
			print("Your session has been successfully updated.")
		else:
			print("There was an error updating your session:")
			pprint.pprint(r.json()["error"])

		return r.json() if r.status_code == 200 else None

	def delete(self):
		check(len(self.cmd_args) > 0, "Deleting a session must specify 'all' or a session ID")
		if self.cmd_args[0] == "all":
			choice = raw_input("Do you really want to delete all session sessions? [y/n] ")
			check(choice == "y", "Aborted.")
			q = ""
		else:
			q = "/" + self.cmd_args[0]

		r = requests.delete(Global.makeURL("/api/v1/session" + q), json=Global.makeData())
		check(r.status_code == 200, "Could not delete session(s). Status code: %d"%r.status_code)

		numRemoved = int(r.json()["removed"])
		print("%d session(s) deleted"%numRemoved if numRemoved > 0 else "No matching sessions deleted.")

		return r.json(), numRemoved

	def printSessionObject(self, obj, fields=["id","number","name","secret","date","desc","image","blogPostLink","project"]):
		if "id" in obj and "id" in fields: print(" id: %s"%obj["id"])
		if "name" in obj and "name" in fields: print(" name: %s"%obj["name"])
		if "number" in obj and "number" in fields: print(" number: %s"%obj["number"])
		if "secret" in obj and "secret" in fields: print(" secret: %s"%obj["secret"])
		if "blogPostLink" in obj and "blogPostLink" in fields: print(" blogPostLink: %s"%obj["blogPostLink"])
		if "image" in obj and "image" in fields: print(" image: %s"%obj["image"])
		if "desc" in obj and "desc" in fields: print(" desc: %s"%obj["desc"])
		if "date" in obj and "date" in fields:
			print(" date:")
			if "start" in obj["date"]: print("     start: %s"%Global.UTCToLocalDisplay(obj["date"]["start"]))
			if "end" in obj["date"]: print("     end: %s"%Global.UTCToLocalDisplay(obj["date"]["end"]))
		if "project" in obj and "project" in fields:
			print(" project:")
			if "points" in obj["project"]: print("     points: %s"%obj["project"]["points"])
			if "videoLink" in obj["project"]: print("     videoLink: %s"%obj["project"]["videoLink"])
			if "slidesLink" in obj["project"]: print("     slidesLink: %s"%obj["project"]["slidesLink"])
			if "submissionLink" in obj["project"]: print("     submissionLink: %s"%obj["project"]["submissionLink"])

		print("---")
