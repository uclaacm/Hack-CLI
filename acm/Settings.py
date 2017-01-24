from Module import Module
from SettingsFile import SettingsFile

class Settings(Module):
	def __init__(self):
		self.settings_file = SettingsFile()	

	def set(self, key, value):
		self.settings_file.set(key, value)

	def get(self, key):
		value = self.settings_file.get(key)
		if not value:
			print("No value set for '%s'"%key)
		else:
			print("%s: %s"%(key, value))
