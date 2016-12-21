from Module import Module
import Global
import requests, pprint, ast

class Event(Module):
	def __init__(self, cmd, cmd_args):
		self.cmd_map = {
			"list": self.list,
			"details": self.details,
			"add": self.add
		}
		Module.__init__(self, cmd, cmd_args)
	
	def list(self):
		r = requests.get(Global.makeURL("/api/v1/event"))
		if (r.status_code != 200):
			print("Error: Malformed request to GET /api/v1/event")
			return
		data = r.json()
		print("Event List")
		print("==========")

		for event in data["events"]:
			self.printEventObject(event, fields=["id","title"])

		if len(data["events"]) == 0:
			print("No events")

	def details(self):
		if len(self.cmd_args) == 0:
			print("Error: event details requires the event ID")
			return
		r = requests.get(Global.makeURL("/api/v1/event/%s"%self.cmd_args[0]))
		if (r.status_code != 200):
			print("Error: Malformed request to GET /api/v1/event/"%self.cmd_args[0])
			return
		data = r.json()
		if len(data["events"]) == 0:
			print("No event with ID %s found."%self.cmd_args[0])
			return
		print("Event Details")
		print("=============")
		self.printEventObject(data["events"][0])

	def add(self):
		print("Creating new event...")
		obj = {
			"event" : {
				"title" : raw_input("(required) title: "),
				"location" : raw_input("(required) location: "),
				"category" : raw_input("(required) category: "),
				"date": {
					"start" : Global.getDateInput("(required) date.start"),
					"end" : Global.getDateInput("(required) date.end") 
				},
				"tagline" : raw_input("(optional) tagline: "),
				"desc" : raw_input("(optional) desc: ")
			}
		}

		pprint.pprint(obj)
		choice = raw_input("Create this event? [y/n]: ")
		if (choice != "y"):
			print("Aborted.")
			return

		r = requests.post(Global.makeURL("/api/v1/event"), json=Global.makeData(obj))
		if (r.status_code == 200):
			print("Your event has been successfully created.")
		else:
			print("There was an error creating your event. Check to make sure your input was valid")

	def printEventObject(self, obj, fields=["id","date","title","category","location","tagline","desc"]):
		if "id" in obj and "id" in fields: print(" id: %s"%obj["id"])
		if "date" in obj and "date" in fields:
			print(" date:")
			if "start" in obj["date"]: print("     start: %s"%obj["date"]["start"])
			if "end" in obj["date"]: print("     end: %s"%obj["date"]["end"])
		if "title" in obj and "title" in fields: print(" title: %s"%obj["title"])
		if "category" in obj and "category" in fields: print(" category: %s"%obj["category"])
		if "location" in obj and "location" in fields: print(" location: %s"%obj["location"])
		if "tagline" in obj and "tagline" in fields: print(" tagline: %s"%obj["tagline"])
		if "desc" in obj and "desc" in fields: print(" desc: %s"%obj["desc"])
			
		print("---")
