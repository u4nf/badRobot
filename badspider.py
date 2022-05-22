#!/usr/bin/python3
import requests
import re
import argparse

#usage
#badspider.py -d [domain] (https:// is added automaticaly)

def validateArgs():
	#validate arguments and set base variables

	parser = argparse.ArgumentParser(description='A tool to spider a domain and return a list for investigation')
	parser.add_argument('-d', type=str,  help='Domain to analyse')
	args=parser.parse_args()

	if not re.match('^(?:http://|https://).*$', args.d):
		host = 'https://' + args.d
	else:
		host = args.d

	return host


#masterlists
uniqueUrls = []
uniqueJs = []
uniqueEmail = []

def crawl(currentUrl):
	#extract data from HTML

	def noDupe(inList, UniqueList, identity, currentUrl):
		#adds to unique list if not seen before

		print('Details for ' + currentUrl)
		count = 0
		for i in inList:
			if i not in UniqueList:
				UniqueList.append(i)
				count += 1

		print(identity + '\'s found - ' + str(len(inList)) + ' // Unseen - ' + str(count))


	def parseUrl(currentUrl):
		#take url and return HTML

		try:
			pageObject = requests.get(currentUrl)
		except:
			print('Unable to parse, check above URL for validity\naccepted - domain.com, http://domain.com, https://domain.com')
			exit(1)

		return pageObject


	pageObject = parseUrl(currentUrl)

	#extract and clean data
	urlList = re.findall('href="(https://.*?)"', pageObject.text)
	noDupe(urlList, uniqueUrls, 'URL', currentUrl)

	jsList = re.findall('(?:\'|src=")(.*\.js)', pageObject.text)
	noDupe(jsList, uniqueJs, 'JS', currentUrl)

	emailList = re.findall('[^\w]([\w\d]*@[\w\d]*\.[\w\d]*?)', pageObject.text)
	noDupe(emailList, uniqueEmail, 'Email', currentUrl)


currentUrl = validateArgs()
print('Assessing ' + currentUrl + '\n')
crawl(currentUrl)
