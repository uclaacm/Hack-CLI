from datetime import datetime
from dateutil import tz
import time

hostname = "http://localhost:5000"
def makeURL(path):
	return hostname + path

def getToken():
	return "1f4e84260a56245f229d311720a0d497baec20c91603dbe0ccd3bc08dc7f3525a47f52f2cb4273051bb072151d"

def makeData(partial_obj={}):
	obj = { "token" : getToken() }
	obj.update(partial_obj)
	return obj

def getDateInput(query):
	user_input = raw_input("%s (formatted as YYYY-MM-DD HH:MM 24-hr format): "%query)
	
	date_obj = datetime.strptime(user_input.strip(), "%Y-%m-%d %H:%M")
	utc_time = datetime.fromtimestamp(time.mktime(date_obj.timetuple()), tz.gettz('UTC'))

	return utc_time.isoformat()
