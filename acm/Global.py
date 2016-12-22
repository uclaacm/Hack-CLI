from Settings import SettingsFile
from datetime import datetime
from dateutil import tz
from dateutil.parser import parse
import time, sys

use_local = SettingsFile().get('use_local')
use_local = use_local != None and eval(use_local)
hostname = "http://localhost:5000" if use_local else "http://acm-hack-dev.herokuapp.com"

def check(cond, msg=None):
	if not cond:
		if msg:
			print("Error: %s"%msg)
		sys.exit(1)

def makeURL(path):
	return hostname + path

def getToken():
	return "1f4e84260a56245f229d311720a0d497baec20c91603dbe0ccd3bc08dc7f3525a47f52f2cb4273051bb072151d"

def makeData(partial_obj={}):
	obj = { "token" : getToken() }
	obj.update(partial_obj)
	return obj

def getDateInput(query):
	user_input = raw_input("%s (formatted as MM-DD-YYYY HH:MM 24-hr format): "%query)

	if (user_input.strip() == ""):
		return ""

	date_obj = datetime.strptime(user_input.strip(), "%m-%d-%Y %H:%M")
	utc_time = datetime.fromtimestamp(time.mktime(date_obj.timetuple()), tz.gettz('UTC'))

	return utc_time.isoformat().split("+")[0] + 'Z'

def UTCToLocalDisplay(utc):
	date = parse(utc).astimezone(tz.tzlocal())
	return date.strftime("%x %X")

def trimDict(d):
	newObj = {}
	for key in d:
		if type(d[key]) == type({}):
			val = trimDict(d[key])
			if len(val) > 0:
				newObj[key] = val
		elif type(d[key]) == type([]):
			if len(d[key]) > 0:
				newObj[key] = d[key]
		elif type(d[key]) == type(""):
			if d[key].strip() != "":
				newObj[key] = d[key].strip()
		elif d[key] != None:
			newObj[key] = d[key]
	return newObj
