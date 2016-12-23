from Module import Module
from Global import check
import Global
import requests, pprint, ast, copy
import json
class Event(Module):
	def __init__(self, cmd, cmd_args):
		self.cmd_map = {
			"list": self.list,
			"details": self.details,
			"add": self.add,
			"update" : self.update,
			"delete" : self.delete
		}
		self.categories = {"hack school", "general"}
		Module.__init__(self, cmd, cmd_args)

	def list(self):
		filter = len(self.cmd_args) == 2 and self.cmd_args[0] == "--filter" and self.cmd_args[1].lower() in self.categories

		r = requests.get(Global.makeURL("/api/v1/event"))
		check(r.status_code == 200, "Malformed request to GET /api/v1/event")

		data = r.json()
		print data
		print("Event List")
		print("==========")
		if len(data["events"]) == 0:
			print "No events"
		else:
			for event in data["events"]:
				if not filter or (filter and data["events"]["category"].lower() == self.cmd_args[1].lower()):
					self.printEventObject(event, fields=["id", "title"])

		return data["events"] if len(data["events"]) > 0 else None

	def details(self):
		# once we have the functionality to search by category or title, we will
		# probably want to change this function
		check(len(self.cmd_args) > 0, "Getting event details requires an event ID")

		r = requests.get(Global.makeURL("/api/v1/event/%s"%self.cmd_args[0]))
		check(r.status_code == 200, "Malformed request to GET /api/v1/event/%s"%self.cmd_args[0])

		data = r.json()
		check(len(data["events"]) > 0, "No event with ID '%s' found"%self.cmd_args[0])

		print("Event Details")
		print("=============")
		self.printEventObject(data["events"][0])

		return data["events"][0]

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

		self.printEventObject(obj["event"])
		choice = raw_input("Create this event? [y/n]: ")
		check(choice == "y", "Aborted.")

		r = requests.post(Global.makeURL("/api/v1/event"), json=Global.makeData(obj))
		if (r.status_code == 200):
			print("Your event has been successfully created.")
		else:
			print("There was an error creating your event (%d). Check to make sure your input was valid"%r.status_code)

		return r.json() if r.status_code == 200 else None

	def update(self):
		check(len(self.cmd_args) > 0, "Updating an event requires an event ID")

		r = requests.get(Global.makeURL("/api/v1/event/%s"%self.cmd_args[0]))
		response = r.json()
		check(r.status_code == 200 and response["success"] and len(response["events"]) > 0, \
			"No event with id '%s' found."%self.cmd_args[0])

		print("Current event data:")
		self.printEventObject(response["events"][0])
		print("You will now be prompted to update this event")
		print(" - Only fill out fields you want to change")
		print(" - To leave a field unchanged, press 'enter'")

		obj = {
			"event" : {
				"title" : raw_input("title: "),
				"location" : raw_input("location: "),
				"category" : raw_input("category: "),
				"date": {
					"start" : Global.getDateInput("date.start"),
					"end" : Global.getDateInput("date.end")
				},
				"tagline" : raw_input("tagline: "),
				"desc" : raw_input("desc: ")
			}
		}

		obj["event"] = Global.trimDict(obj["event"])
		print("---")
		print("Event changes:")
		self.printEventObject(obj["event"])

		choice = raw_input("Make these changes? [y/n]: ")
		check(choice == "y", "Aborted.")

		r = requests.patch(Global.makeURL("/api/v1/event/%s"%self.cmd_args[0]), json=Global.makeData(obj))
		if (r.status_code == 200):
			print("Your event has been successfully updated.")
		else:
			print("There was an error updating your event (%d). Check to make sure your input was valid"%r.status_code)

		return r.json() if r.status_code == 200 else None

	def delete(self):
		check(len(self.cmd_args) > 0, "Deleting an event must specify 'all' or an event ID")
		if self.cmd_args[0] == "all":
			choice = raw_input("Do you really want to delete all events? [y/n] ")
			check(choice == "y", "Aborted.")
			q = ""
		else: q = "/" + self.cmd_args[0]

		r = requests.delete(Global.makeURL("/api/v1/event" + q), json=Global.makeData())
		check(r.status_code == 200, "Could not delete event(s). Status code: %d"%r.status_code)

		numRemoved = int(r.json()["removed"])
		print("%d event(s) deleted"%numRemoved if numRemoved > 0 else "No matching events deleted.")

		return r.json(), numRemoved

	def printEventObject(self, obj, fields=["id","date","title","category","location","tagline","desc"]):
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
