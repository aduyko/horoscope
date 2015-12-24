import urllib
import json
import datetime
import time
import sys
from bs4 import BeautifulSoup

#debug kind of
import pprint

# utf8 nearest neighbors
def parseJSONResponse(response, encoding):
  text = response.read().decode(encoding)
  text = text.replace("\\u2019","'")
  text = text.replace("\\u2014","--")
  text = text.encode('ascii','ignore')
  return text

def parseHTMLResponse(response, encoding):
  text = response.read().decode(encoding).encode('ascii','ignore')
  soup = BeautifulSoup(text, 'html.parser')
  return soup

# takes 20-30 seconds per sign/date, no bulk endpoint though
def getFab40(sign,date):
  url = "http://widgets.fabulously40.com/horoscope.json?sign=" + sign + "&date=" + date
  result = None
  try:
    response = urllib.urlopen(url)
    parsedResponse = parseJSONResponse(response,'utf-8')
    jsonResponse = json.loads(parsedResponse)
    if(len(jsonResponse) > 0):
      result = str(jsonResponse['horoscope']['horoscope'])
  except:
    with open("../data/error.log", "a+") as errorFile:
      errorFile.write("Error opening url for 'getFab40': " + url)
  return result

def parseGoToHoroscopeSoup(soup):
  uTags = soup.findAll('u')
  horoscopes = {}
  for uTag in uTags:
    sign = uTag.text.strip().split(' ', 1)[0]
    # this is so bad but I can't detect "None" for whatever reason
    if(sign == "Today" or sign is None):
      break
    horoscope = uTag.next_sibling.next_sibling.strip()
    horoscopes[sign] = horoscope
  return horoscopes

# takes 1-2 seconds per date, really janky html formatting on their end
# sometimes they forget or mislabel horoscopes????
def getGoToHoroscope(date):
  yearString = date.strftime("%Y") + "-horoscope"
  dayString = date.strftime("%d").lstrip('0') + date.strftime("%B").lower()
  url = "http://gotohoroscope.com/" + yearString + "/" + dayString + ".html"
  result = None
  try:
    response = urllib.urlopen(url)
    parsedResponse = parseHTMLResponse(response,'iso-8859-1')
    cleanedResponse = parseGoToHoroscopeSoup(parsedResponse)
    if(len(cleanedResponse) > 0):
      result = cleanedResponse
  except:
    with open("../data/error.log", "a+") as errorFile:
      errorFile.write("Error opening url for 'getGoToHoroscope': " + url + "\n")
  return result

def getHoroscopes(services,signs,startDate,endDate):
  timestamp = str(int(time.time()*1000))
  serviceHoroscopes = {s: {h: {} for h in signs} for s in services}
  #http://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
  currentDate = startDate
  oneDayDelta = datetime.timedelta(days=1)
  while currentDate <= endDate:
    formattedDate = currentDate.strftime("%Y-%m-%d")
    print formattedDate
    for service in services:
      print service
      if(service == 'goToHoroscope'):
        dateHoroscopes = getGoToHoroscope(currentDate)
      else:
        dateHoroscopes = None
      for sign in signs:
        horoscope = None
        if(service == 'fab40'):
          horoscope = getFab40(sign,formattedDate)
        if(service == 'goToHoroscope'):
          if(sign in dateHoroscopes):
            horoscope = str(dateHoroscopes[sign])
        if(horoscope != None):
          serviceHoroscopes[service][sign][formattedDate] = horoscope
    currentDate += oneDayDelta
  #output results
  with open("../data/allHoroscopes_" + timestamp, "a+") as dumpFile:
    json.dump(serviceHoroscopes, dumpFile, ensure_ascii=False)
  for service in services:
    with open("../data/" + service + "_" + timestamp, "a+") as dumpFile:
      json.dump(serviceHoroscopes[service], dumpFile, ensure_ascii=False)
  #debug
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(serviceHoroscopes)

# services = ["fab40"]
services = ["goToHoroscope"]
# thestar http://www.thestar.com/diversions/horoscope/2015/05/01/horoscope-for-friday-may-1-2015.html
# freewillastrology http://www.freewillastrology.com/horoscopes/horo-archive.html
# russel grant http://www.russellgrant.com/horoscopes_astrology/daily_horoscopes/index/2000/horoscopes-daily-january-01.html
# aladdin fun house http://aladdinfunhouse.com/daily-horoscope-aries-tuesday-december-2-2014/
signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
startDate = datetime.date(2013,1,2)
endDate = datetime.date(2013,1,2)

getHoroscopes(services, signs, startDate, endDate)
