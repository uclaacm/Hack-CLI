#! /usr/bin/env python

import sys
from Event import Event
from Showcase import Showcase
from Session import Session
from Settings import Settings

def USAGE_INFO():
	return """
Usage: acm [module] [command] [command arguments]
Events:
	acm event list          - lists events
	acm event details [id]  - gets more details about an event
	acm event add           - add a new event
	acm event update [id]   - update an event by its id
	acm event delete [id]   - delete an event by its id
	acm event delete all    - delete all events

Showcase Projects:
	acm showcase list           - lists showcase projects
	acm showcase details [id]   - gets more details about a showcase project
	acm showcase add            - add a new showcase project
	acm showcase update [id]    - update a showcase project by its id
	acm showcase delete [id]    - delete a showcase project by its id
	acm showcase delete all     - delete all showcase projects

Sessions:
	acm session list           - lists session hack school sessions
	acm session details [id]   - gets more details about a session
	acm session add            - add a new hack school session
	acm session update [id]    - update a session by its id
	acm session delete [id]    - delete a session by its id
	acm session delete all     - delete all hack school sessions

	"""

def main():
	if len(sys.argv) == 1:
		print("You must specify a module name")
		print(USAGE_INFO())
		sys.exit(1)

	if sys.argv[1] == 'h' or sys.argv[1] == 'help':
		print(USAGE_INFO())
		sys.exit(0)

	if len(sys.argv) == 2:
		print("You must specify a module command")
		print(USAGE_INFO())
		sys.exit(1)

	modules = {
		"event" : Event,
		"showcase" : Showcase,
		"session" : Session,
		"cli" : Settings
	}

	if sys.argv[1] not in modules.keys():
		print "invalid command"
		print (USAGE_INFO())
		sys.exit(1)
	module = modules[sys.argv[1]](sys.argv[2], sys.argv[3:])
	module.run()
