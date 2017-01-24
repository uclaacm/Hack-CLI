import os, pickle

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
