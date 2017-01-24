#! /usr/bin/env python

from __future__ import print_function
import sys
from Event import Event
from Score import Score
from Session import Session
from Showcase import Showcase
from Settings import Settings

def USAGE_INFO():
	return """
Usage: acm [module] [command] [command arguments]
CLI:
  acm cli:set [key] [value]            - set (key,value) setting for the CLI
  acm cli:get [key]                    - get the value for key [key]

Events:
  acm event:list                       - lists events
  acm event:details [id]               - gets more details about an event
  acm event:add                        - add a new event
  acm event:update [id]                - update an event by its id
  acm event:delete [id]                - delete an event by its id
  acm event:delete all                 - delete all events

Showcase Projects:
  acm showcase:list                    - lists showcase projects
  acm showcase:details [id]            - gets more details about a showcase project
  acm showcase:add                     - add a new showcase project
  acm showcase:update [id]             - update a showcase project by its id
  acm showcase:delete [id]             - delete a showcase project by its id
  acm showcase:delete all              - delete all showcase projects

Sessions:
  acm session:list                     - lists session hack school sessions
  acm session:details [id]             - gets more details about a session
  acm session:add                      - add a new hack school session
  acm session:update [id]              - update a session by its id
  acm session:delete [id]              - delete a session by its id
  acm session:delete all               - delete all hack school sessions

Team:
  Scores:
    acm team:score:list [id]           - Get team [id]'s scores
    acm team:score:add [id]            - Add a score to team [id]
    acm team:score:update [id]         - Update a team [id]'s score for a session
    acm team:score:delete [id] [num]   - Delete a team [id]'s score for session [num]
  
  """

def main():
	if len(sys.argv) == 1:
		print("You must specify a module and command")
		print(USAGE_INFO())
		sys.exit(1)

	if sys.argv[1] == 'h' or sys.argv[1] == 'help':
		print(USAGE_INFO())
		sys.exit(0)

	modules = {
		"event" : Event,
		"team:score" : Score,
		"showcase" : Showcase,
		"session" : Session,
		"cli" : Settings
	}

	if len(sys.argv[1].split(":")) < 2:
		print("Invalid command: %s"%sys.argv[1])
		print(USAGE_INFO())

	module = sys.argv[1].rsplit(":", 1)[0]
	command = sys.argv[1].split(":")[-1]
	arguments = sys.argv[2:]
	getattr(modules[module](), command)(*arguments)
