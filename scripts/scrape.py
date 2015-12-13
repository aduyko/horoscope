import urllib
import json
import datetime
import time
#debug kind of
import pprint

# utf8 nearest neighbors
def parseResponse(response):
	text = response.read().decode('utf-8')
	text = text.replace("\\u2019","'")
	text = text.replace("\\u2014","--")
	return text

# takes 20-30 seconds per sign/date, no bulk endpoint though
def getFab40(sign,date):
	url = "http://widgets.fabulously40.com/horoscope.json?sign=" + sign + "&date=" + date
	try:
		response = urllib.urlopen(url)
		parsedResponse = parseResponse(response)
		jsonResponse = json.loads(parsedResponse)
		if(len(jsonResponse) > 0):
			return str(jsonResponse['horoscope']['horoscope'])
	except:
		with open("../data/error.log", "a+") as errorFile:
		  errorFile.write("Error opening url for 'getFab40': " + url)
	return None

def getHoroscopes(services,signs,startDate,endDate):
	serviceHoroscopes = {s: {h: {} for h in signs} for s in services}
	#http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
	currentDate = startDate
	oneDayDelta = datetime.timedelta(days=1)
	while currentDate <= endDate:
		formattedDate = currentDate.strftime("%Y-%m-%d")
		print formattedDate
		for service in services:
			print service
			for sign in signs:
				horoscope = None
				if(service == 'fab40'):
				  horoscope = getFab40(sign,formattedDate)
				if(horoscope != None):
					serviceHoroscopes[service][sign][formattedDate] = horoscope
		currentDate += oneDayDelta
	#output results
	timestamp = str(int(time.time()*1000))
	pp = pprint.PrettyPrinter(indent=4)
	with open("../data/allHoroscopes_" + timestamp, "a+") as dumpFile:
		json.dump(serviceHoroscopes, dumpFile, ensure_ascii=False)
	for service in services:
		with open("../data/" + service + "_" + timestamp, "a+") as dumpFile:
			json.dump(serviceHoroscopes[service], dumpFile, ensure_ascii=False)
	pp.pprint(serviceHoroscopes)

services = ["fab40"]
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
startDate = datetime.date(2013,1,1)
endDate = datetime.date(2013,1,1)

getHoroscopes(services, signs, startDate, endDate)
