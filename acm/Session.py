from Info import InfoField, Interpreter
from Module import Module
from Global import check
import Global, Crypt

class Session(Module):
	def __init__(self):
		Module.__init__(self)
		self.api_url = "/api/v1/hackschool/session"
		self.obj_format = {
			"session" : {
				"number": InfoField(required=True, interpreter=int),
				"name": InfoField(required=True, additionalInfo="title"),
				"secret": InfoField(required=True, additionalInfo="attendance secret"),
				"desc": InfoField(required=True),
				"image": InfoField(required=True),
				"date": {
					"start": InfoField(required=True, inputter=Global.getDateInput),
					"end": InfoField(required=True, inputter=Global.getDateInput),
				},
				"blogPostLink": InfoField(),
				"project": {
					"points": InfoField(interpreter=int),
					"videoLink": InfoField(),
					"slidesLink": InfoField(),
					"submissionLink": InfoField(),
					"sourceCodeLink": InfoField(),
				}
			}
		}

	def list(self):
		data = self.api_request(auth=True)
		print("Hack School Session List\n==========")
		if len(data["sessions"]) == 0:
			print "No sessions"
		else:
			for session in data["sessions"]:
				self.printObj(session, fields=["id", "name", "number"])

	def details(self, id):
		data = self.api_request(endpoint="/%s"%id, auth=True)
		check(len(data["sessions"]) > 0, "No session with ID '%s' found"%id)

		print("Hack School Session Details\n=============")
		self.printObj(data["sessions"][0])

	def add(self):
		print("Creating new Hack School Session...")
		obj = self.requestInfo()
		self.printObj(obj["session"])
		choice = raw_input("Create this session? [y/n]: ")
		check(choice == "y", "Aborted.")

		self.api_request(method="POST", json=obj, auth=True)
		print("Your session has been successfully created.")

	def update(self, id):
		data = self.api_request(endpoint="/%s"%id, auth=True)
		check(len(data["sessions"]) > 0, "No session with id '%s' found."%id)

		print("Current session data:")
		self.printObj(data["sessions"][0])
		print("You will now be prompted to update this session")
		print(" - Only fill out fields you want to change")
		print(" - To leave a field unchanged, press 'enter'")

		obj = self.requestInfo(update=True)
		print("---")
		print("Project changes:")
		self.printObj(obj["session"])

		choice = raw_input("Make these changes? [y/n]: ")
		check(choice == "y", "Aborted.")

		self.api_request(method="PATCH", endpoint="/%s"%id, auth=True, json=obj)
		print("Your session has been successfully updated.")

	def delete(self, id):
		endpoint = "/%s"%id
		if id == "all":
			choice = raw_input("Do you really want to delete all session sessions? [y/n] ")
			check(choice == "y", "Aborted.")
			endpoint = ""

		data = self.api_request(method="DELETE", endpoint=endpoint, auth=True)
		numRemoved = int(data["removed"])
		print("%d session(s) deleted"%numRemoved if numRemoved > 0 else "No matching sessions deleted.")

	def printObj(self, obj, fields=["id","number","name","secret","date","desc","image","blogPostLink","project"]):
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
			if "sourceCodeLink" in obj["project"]: print("     sourceCodeLink: %s"%obj["project"]["sourceCodeLink"])

		print("---")
