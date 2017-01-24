from SettingsFile import SettingsFile
from Global import check, trimDict
from Crypt import getToken
from requests import request

class Module(object):
	def __init__(self):
		self.settings_file = SettingsFile()
		self.obj_format = {}

		use_local = self.settings_file.get('use_local')
		use_local = use_local != None and eval(use_local)
		use_dev = self.settings_file.get('use_dev')
		use_dev = use_dev != None and eval(use_dev)

		self.hostname = "http://localhost:5000" if use_local else "http://hack-ucla.herokuapp.com"
		self.hostname = "http://hack-ucla-dev.herokuapp.com" if use_dev else self.hostname

	def api_request(self, method="GET", endpoint="", params={}, auth=False, json={}):
		if auth:
			if method == "GET":
				params["token"] = getToken()
			else:
				json["token"] = getToken()

		url = self.makeURL(self.api_url + endpoint)
		req = request(method, url, json=json, params=params)
		check(req.status_code == 200 and req.json()["success"] == True, "Error [%s] %s %d: %s"%(method, url, req.status_code, req.json()["error"]))
		
		return req.json()

	def makeURL(self, url):
		return self.hostname + url

	def printObj(self, obj, fields=[]):
		raise NotImplementedError()

	def requestInfo(self, format=None, path="", update=False):
		format = self.obj_format if not format else format
		data = {  }
		for key in sorted(format):
			if type(format[key]) == type({}):
				data[key] = self.requestInfo(format[key], path=path+key+".", update=update)
			else:
				msg = ""
				if not update:
					msg += "(%s) "%("required" if format[key].required else "optional")
				msg += "%s"%(path + key)
				if format[key].additionalInfo:
					msg += " [%s]"%(format[key].additionalInfo)
				msg += ": "
				inpt = format[key].inputter(msg)
				if format[key].interpreter and inpt.strip() != "":
					inpt = format[key].interpreter(inpt)
				data[key] = inpt
		
		return trimDict(data)