import urllib2
import pdfkit
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

# Printing all the elements of the list
def print_URL_List():
	for url in all_URLs:
		print url

# Many reports cannot be viewed cause maybe we don't have enough privilege or maybe they dont exist.
# So we need to create a list which will store valid url
# On doing some kind of enumeration I found that if a url is not valid it will say "Page not found "
# And if its a valid report but not public it will ask us to login. 

#


def validReportURL():
	log_file = open("logfile.txt","w")
	headers = { 'User-Agent' : 'Chrome/51.0.2704.103' }
	for url in all_URLs:

		try :
			req = urllib2.Request(url)
			soup = BeautifulSoup(urllib2.urlopen(req),"html.parser")
			title = soup.title.string

			if title != "Sign in to HackerOne and Start Hacking":
				final_URLs.append(url)
			log_file.write(title+"\n")
			print title
		except :
			log_file.write(url+" Not found !!! 404\n")
			print url+" Not found !!! 404 "

	log_file.close()

def generatePDFofValidReports():
	for url in final_URLs:
		last = url.rfind("/")
		reportNumber = url[last+1 ::]
		fileName = str(reportNumber)+".pdf"
		pdfkit.from_url(url, fileName)

def generateHTMLReports():
	for url in final_URLs:
		last = url.rfind("/")
		reportNumber = url[last+1 ::]
		fileName = str(reportNumber)+".html"
		response = urllib2.urlopen(url)
		webContent = response.read()
		genFile = open(fileName,"w")
		genFile.write(webContent)
		genFile.close()


generateURL(9483,9487)
validReportURL()
#generatePDFofValidReports()
generateHTMLReports()

