class Module(object):
	def __init__(self, cmd, cmd_args):
		if not hasattr(self, 'cmd_map'):
			raise NotImplementedError("Child class must declare a command map")
		self.cmd = cmd
		self.cmd_args = cmd_args
		if not self.cmd in self.cmd_map:
			raise Exception("Invalid command '%s'"%self.cmd)
	
	def run(self):
		self.cmd_map[self.cmd]()

