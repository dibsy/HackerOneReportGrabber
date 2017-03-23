import urllib2
import sys
from json2html import *
from bs4 import BeautifulSoup

all_URLs = [] #  This list contains all the valid urls 
final_URLs = [] # This list contains all the final urls
# This function will generate urls like https://hackerone.com/reports/9485. It will have two parameters which will act
# as lower range and upper range so that user can enter the range between which they want to fetch the report

def generateURL(lower,upper):
	base_url = "https://hackerone.com/reports/"
	for i in range(lower,upper+1,1):
		final_url=base_url+str(i)
		all_URLs.append(final_url)
# Many reports cannot be viewed cause maybe we don't have enough privilege or maybe they dont exist.
# So we need to create a list which will store valid url
# On doing some kind of enumeration I found that if a url is not valid it will say "Page not found "
# And if its a valid report but not public it will ask us to login. 

def validReportURL():
	for url in all_URLs:
		try :
			print "Trying url : "+url
			req = urllib2.Request(url)
			soup = BeautifulSoup(urllib2.urlopen(req),"html.parser")
			title = soup.title.string
			if title != "Sign in to HackerOne and Start Hacking":
				final_URLs.append(url) #Get the JSON of the file
				print "Public Report Found "+title
		except :
			e = sys.exc_info()[0]
			print e.encode("utf-8") # Need to fix this with proper message

def generateHTMLReports():
	for url in final_URLs:
		last = url.rfind("/") # Getting the last index of /
		reportNumber = url[last+1 ::] # Getting the numeric part of the url, which is the report number
		fileName = str(reportNumber)+".html" # Creating a <reportNumner>.html file , ex 4569.html 
		response = urllib2.urlopen(url+".json") # Getting the json file https://hackerone.com/reports/9485.json
		webContent = response.read() # Read the contents
		html = json2html.convert(json = webContent) # convert the json content to html
		genFile = open(fileName,"w") #create a html file
		genFile.write(html.encode("utf-8")) # write the converted html contents
		genFile.close() # close it

# The first parameter is the lower range of report number and the second parameter is the upper range of the report parameter
generateURL(9400,9500) 
validReportURL()
generateHTMLReports()
print "Reports Generated in current directory\n"
