from Module import Module
from Global import check
import Global
import requests, pprint, ast, copy

class Showcase(Module):
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
		r = requests.get(Global.makeURL("/api/v1/showcase"))
		check(r.status_code == 200, "Malformed request to GET /api/v1/showcase")

		data = r.json()
		print("Showcase Project List")
		print("==========")
		if len(data["projects"]) == 0:
			print "No projects"
		else:
			for project in data["projects"]:
				self.printProjectObject(project, fields=["id", "title"])

	def details(self):
		check(len(self.cmd_args) > 0, "Getting project details requires a project ID")

		r = requests.get(Global.makeURL("/api/v1/showcase/%s"%self.cmd_args[0]))
		check(r.status_code == 200, "Malformed request to GET /api/v1/showcase/%s"%self.cmd_args[0])

		data = r.json()
		check(len(data["projects"]) > 0, "No project with ID '%s' found"%self.cmd_args[0])

		print("Showcase Project Details")
		print("=============")
		self.printProjectObject(data["projects"][0])

	def add(self):
		print("Creating new project...")
		obj = {
			"project" : {
				"title" : raw_input("(required) title: "),
				"link" : raw_input("(required) project link: "),
				"contributors" : [x.strip() for x in raw_input("(required) contributors, comma-separated: ").split(",") if len(x.strip()) > 0],
				"image" : raw_input("(optional) image URL: "),
				"desc" : raw_input("(optional) desc: ")
			}
		}

		self.printProjectObject(obj["project"])
		choice = raw_input("Create this project? [y/n]: ")
		check(choice == "y", "Aborted.")

		r = requests.post(Global.makeURL("/api/v1/showcase"), json=Global.makeData(obj))
		if (r.status_code == 200):
			print("Your project has been successfully created.")
		else:
			print("There was a error creating your project (%d). Check to make sure your input was valid"%r.status_code)

	def update(self):
		check(len(self.cmd_args) > 0, "Updating a project requires a project ID")

		r = requests.get(Global.makeURL("/api/v1/showcase/%s"%self.cmd_args[0]))
		response = r.json()
		check(r.status_code == 200 and response["success"] and len(response["projects"]) > 0, \
			"No project with id '%s' found."%self.cmd_args[0])

		print("Current project data:")
		self.printProjectObject(response["projects"][0])
		print("You will now be prompted to update this project")
		print(" - Only fill out fields you want to change")
		print(" - To leave a field unchanged, press 'enter'")

		obj = {
			"project" : {
				"title" : raw_input("title: "),
				"link" : raw_input("project link: "),
				"contributors" : [x.strip() for x in raw_input("contributors, comma-separated: ").split(",") if len(x.strip()) > 0],
				"image" : raw_input("image URL: "),
				"desc" : raw_input("desc: ")
			}
		}

		obj["project"] = Global.trimDict(obj["project"])
		print("---")
		print("Project changes:")
		self.printProjectObject(obj["project"])

		choice = raw_input("Make these changes? [y/n]: ")
		check(choice == "y", "Aborted.")

		r = requests.patch(Global.makeURL("/api/v1/showcase/%s"%self.cmd_args[0]), json=Global.makeData(obj))
		if (r.status_code == 200):
			print("Your project has been successfully updated.")
		else:
			print("There was an error updating your project (%d). Check to make sure your input was valid"%r.status_code)

	def delete(self):
		check(len(self.cmd_args) > 0, "Deleting a project must specify 'all' or a project ID")
		if self.cmd_args[0] == "all":
			choice = raw_input("Do you really want to delete all showcase projects? [y/n] ")
			check(choice == "y", "Aborted.")
			q = ""
		else:
			q = "/" + self.cmd_args[0]

		r = requests.delete(Global.makeURL("/api/v1/showcase" + q), json=Global.makeData())
		check(r.status_code == 200, "Could not delete project(s). Status code: %d"%r.status_code)

		numRemoved = int(r.json()["removed"])
		print("%d project(s) deleted"%numRemoved if numRemoved > 0 else "No matching projects deleted.")

	def printProjectObject(self, obj, fields=["id","date","title","contributors","link","image","desc"]):
		if "id" in obj and "id" in fields: print(" id: %s"%obj["id"])
		if "date" in obj and "date" in fields: print(" date: %s"%Global.UTCToLocalDisplay(obj["date"]))
		if "title" in obj and "title" in fields: print(" title: %s"%obj["title"])
		if "contributors" in obj and "contributors" in fields: print(" contributors: %s"%", ".join(obj["contributors"]))
		if "link" in obj and "link" in fields: print(" link: %s"%obj["link"])
		if "image" in obj and "image" in fields: print(" image: %s"%obj["image"])
		if "desc" in obj and "desc" in fields: print(" desc: %s"%obj["desc"])

		print("---")
