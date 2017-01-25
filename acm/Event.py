from Module import Module
from Global import check
from Info import InfoField
import Global
import pprint

class Event(Module):
	def __init__(self):
		Module.__init__(self)
		self.api_url = "/api/v1/event"
		self.obj_format = {
			"event" : {
				"title" : InfoField(required=True),
				"location" : InfoField(required=True),
				"category" : InfoField(required=True),
				"date": {
					"start" : InfoField(required=True, inputter=Global.getDateInput),
					"end" : InfoField(required=True, inputter=Global.getDateInput)
				},
				"tagline" : InfoField(),
				"desc" : InfoField()
			}
		}

	def list(self):
		data = self.api_request()
		print("Event List\n=========")
		if len(data["events"]) == 0:
			print "No events"
		else:
			for event in data["events"]:
				self.printObj(event, fields=["id", "title"])

	def details(self, id):
		data = self.api_request(endpoint="/%s"%id)
		check(len(data["events"]) > 0, "No event with ID '%s' found"%self.cmd_args[0])

		print("Event Details\n=============")
		self.printObj(data["events"][0])

	def add(self):
		print("Creating new event...")
		obj = self.requestInfo()

		self.printObj(obj["event"])
		choice = raw_input("Create this event? [y/n]: ")
		check(choice == "y", "Aborted.")

		self.api_request(method="POST", auth=True, json=obj)
		print("Your event has been successfully created.")

	def update(self, id):
		data = self.api_request(endpoint="/%s"%id)
		check(len(data["events"]) > 0, "No event with id '%s' found."%id)

		print("Current event data:")
		self.printObj(data["events"][0])
		obj = self.requestInfo(update=True)
		
		print("---")
		print("Event changes:")
		self.printObj(obj["event"])

		choice = raw_input("Make these changes? [y/n]: ")
		check(choice == "y", "Aborted.")

		self.api_request(method="PATCH", endpoint="/%s"%id, auth=True, json=obj)
		print("Your event has been successfully updated.")

	def delete(self, id):
		endpoint = "/%s"%id
		if id == "all":
			choice = raw_input("Do you really want to delete all events? [y/n] ")
			check(choice == "y", "Aborted.")
			endpoint = ""
		
		data = self.api_request(method="DELETE", endpoint=endpoint, auth=True)
		numRemoved = int(data["removed"])
		print("%d event(s) deleted"%numRemoved if numRemoved > 0 else "No matching events deleted.")

	def printObj(self, obj, fields=["id","date","title","category","location","tagline","desc"]):
		if "id" in obj and "id" in fields: print(" id: %s"%obj["id"])
		if "date" in obj and "date" in fields:
			print(" date:")
			if "start" in obj["date"]: print("     start: %s"%Global.UTCToLocalDisplay(obj["date"]["start"]))
			if "end" in obj["date"]: print("     end: %s"%Global.UTCToLocalDisplay(obj["date"]["end"]))
		if "title" in obj and "title" in fields: print(" title: %s"%obj["title"])
		if "category" in obj and "category" in fields: print(" category: %s"%obj["category"])
		if "location" in obj and "location" in fields: print(" location: %s"%obj["location"])
		if "tagline" in obj and "tagline" in fields: print(" tagline: %s"%obj["tagline"])
		if "desc" in obj and "desc" in fields: print(" desc: %s"%obj["desc"])

		print("---")
