from Module import Module
import Global
import requests, pprint, ast, copy, os, pickle

class Settings(Module):
	def __init__(self, cmd, cmd_args):
		self.cmd_map = {
			"set" : self.set,
			"get" : self.get
		}
		
		self.settings_file = SettingsFile()	
		Module.__init__(self, cmd, cmd_args)

	def set(self):
		from Global import check
		check(len(self.cmd_args) > 1, "Must provide a key and value")
		self.settings_file.set(self.cmd_args[0], self.cmd_args[1])

	def get(self):
		from Global import check
		check(len(self.cmd_args) > 0, "Must provide a key")
		check(self.settings_file.get(self.cmd_args[0]), "No value set for '%s'"%self.cmd_args[0])
		print("%s: %s"%(self.cmd_args[0], self.settings_file.get(self.cmd_args[0])))

class SettingsFile(object):
	def __init__(self):
		self.filename = os.environ["HOME"] + "/.acm.cfg"
		self.properties = {} if not os.path.exists(self.filename) else self.load()
	
	def get(self, key):
		return self.properties[key] if key in self.properties else None
	
	def set(self, key, value):
		self.properties[key] = value
		self.persist()

	def load(self):
		return pickle.load(open(self.filename, "r"))

	def persist(self):
		pickle.dump(self.properties, open(self.filename, "w"))
