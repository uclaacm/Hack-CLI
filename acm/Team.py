from Module import Module
from Info import InfoField, Interpreter

class Team(Module):
	def __init__(self):
		Module.__init__(self)
		self.obj_format = {}
		self.score_obj_format = {
			"score": {
				"sessionNumber": InfoField(required=True, interpreter=int),
				"score": InfoField(required=True, interpreter=float),
				"daysLate": InfoField(interpreter=int)
			}
		}
	
	def printObj(obj, fields=["id","name","totalScore","members","scores","attendance"]):
		if "id" in obj and "id" in fields: print(" id: %s"%obj["id"])
		if "name" in obj and "name" in fields: print(" name: %s"%obj["name"])
		if "totalScore" in obj and "totalScore" in fields: print(" totalScore: %s"%obj["totalScore"])
		if "members" in obj and "members" in fields:
			print(" members: %s"%(", ".join([member["name"] for member in obj["members"]])))
		if "scores" in obj and "scores" in fields:
			print(" scores (%d):"%len(obj["scores"]))
			for score in obj["scores"]:
				print("     session %d: %d"%(score["sessionNumber"], score["score"]))
		if "attendance" in obj and "attendance" in fields:
			print(" attendance: %s"%(", ".join([str(session) for session in obj["attendance"]])))
				
