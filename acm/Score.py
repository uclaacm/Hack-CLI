from Team import Team
from Global import check
import Global, Crypt
import requests, pprint, ast, copy

class Score(Team):
	def __init__(self):
		Team.__init__(self)
		self.api_url = "/api/v1/hackschool/team/score"

	def list(self, id):
		data = self.api_request(auth=True, endpoint="/%s"%id)
		print("Team '%s' Scores List\n=========="%id)
		if len(data["scores"]) == 0:
			print "No scores"
		else:
			for score in data["scores"]:
				self.printScoreObj(score)

	def add(self, id, verb="add"):
		print("%s score for team '%s'"%(verb,id))
		obj = self.requestInfo(format=self.score_obj_format)
		
		self.printScoreObj(obj["score"])
		choice = raw_input("%s this score? [y/n]: "%verb)
		check(choice == "y", "Aborted.")

		data = self.api_request(method="POST", endpoint="/%s"%id, auth=True, json=obj)
		print("The score has been successfully %sed"%verb)

	def update(self, id):
		self.add(id, verb="update")

	def delete(self, id, num):
		choice = raw_input("Do you really want to delete score %d for team '%s'? [y/n] "%(int(num), id))
		check(choice == "y", "Aborted.")
		endpoint = "/%s"%id
		obj = { "score": { "sessionNumber": int(num) } }

		self.api_request(method="DELETE", endpoint=endpoint, auth=True, json=obj)
		print("The score has been deleted successfully")

	def printScoreObj(self, obj, fields=["sessionNumber","score","daysLate"]):
		if "sessionNumber" in obj and "sessionNumber" in fields:
			print(" sessionNumber: %d"%obj["sessionNumber"])
		if "score" in obj and "score" in fields:
			print(" score: %d"%obj["score"])
		if "daysLate" in obj and "daysLate" in fields:
			print(" daysLate: %d"%obj["daysLate"])
		
		print("--")