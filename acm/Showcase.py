from Module import Module
from Global import check
from Info import InfoField, Interpreter
import Global
import pprint

class Showcase(Module):
	def __init__(self):
		Module.__init__(self)
		self.api_url = "/api/v1/showcase"
		self.obj_format = {
			"project" : {
				"title": InfoField(required=True),
				"link": InfoField(required=True),
				"sourceLink": InfoField(),
				"contributors": InfoField(required=True, interpreter=Interpreter.list, additionalInfo="comma-separated"),
				"technologies": InfoField(required=True, interpreter=Interpreter.list, additionalInfo="comma-separated"),
				"screenshots": InfoField(required=True, interpreter=Interpreter.list, additionalInfo="comma-separated"),
				"image": InfoField(),
				"desc": InfoField()
			}
		}

	def list(self):
		data = self.api_request()
		print("Showcase Project List\n==========")
		if len(data["projects"]) == 0:
			print "No projects"
		else:
			for project in data["projects"]:
				self.printObj(project, fields=["id", "title"])

	def details(self, id):
		data = self.api_request(endpoint="/%s"%id)
		check(len(data["projects"]) > 0, "No project with ID '%s' found"%id)

		print("Showcase Project Details\n=============")
		self.printObj(data["projects"][0])

	def add(self):
		print("Creating new project...")
		obj = self.requestInfo()
		self.printObj(obj["project"])
		choice = raw_input("Create this project? [y/n]: ")
		check(choice == "y", "Aborted.")

		self.api_request(method="POST", auth=True, json=obj)
		print("Your project has been successfully created.")

	def update(self, id):
		data = self.api_request(endpoint="/%s"%id)
		check(len(data["projects"]) > 0, "No project with id '%s' found."%id)

		print("Current project data:")
		self.printObj(data["projects"][0])
		obj = self.requestInfo(update=True)
		
		print("---")
		print("Project changes:")
		self.printObj(obj["project"])

		choice = raw_input("Make these changes? [y/n]: ")
		check(choice == "y", "Aborted.")

		self.api_request(method="PATCH", endpoint="/%s"%id, auth=True, json=obj)
		print("Your project has been successfully updated.")

	def delete(self, id):
		endpoint = "/%s"%id
		if id == "all":
			choice = raw_input("Do you really want to delete all showcase projects? [y/n] ")
			check(choice == "y", "Aborted.")
			endpoint = ""

		data = self.api_request(method="DELETE", endpoint=endpoint, auth=True)
		numRemoved = int(data["removed"])
		print("%d project(s) deleted"%numRemoved if numRemoved > 0 else "No matching projects deleted.")

	def printObj(self, obj, fields=["id","date","title","contributors","technologies","screenshots","link","sourceLink","image","desc"]):
		if "id" in obj and "id" in fields: print(" id: %s"%obj["id"])
		if "date" in obj and "date" in fields: print(" date: %s"%Global.UTCToLocalDisplay(obj["date"]))
		if "title" in obj and "title" in fields: print(" title: %s"%obj["title"])
		if "contributors" in obj and "contributors" in fields: print(" contributors: %s"%", ".join(obj["contributors"]))
		if "technologies" in obj and "technologies" in fields: print(" technologies: %s"%", ".join(obj["technologies"]))
		if "screenshots" in obj and "screenshots" in fields: print(" screenshots: %s"%", ".join(obj["screenshots"]))
		if "link" in obj and "link" in fields: print(" link: %s"%obj["link"])
		if "sourceLink" in obj and "sourceLink" in fields: print(" sourceLink: %s"%obj["sourceLink"])
		if "image" in obj and "image" in fields: print(" image: %s"%obj["image"])
		if "desc" in obj and "desc" in fields: print(" desc: %s"%obj["desc"])

		print("---")
