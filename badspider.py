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
		domain = 'https://' + args.d
	else:
		domain = args.d

	toCrawlUrls.append(domain)

	return domain, domain


def crawl(currentUrl):
	#extract data from HTML
	#print('crawling ' + currentUrl)

	def noDupe(inList, uniqueList, doneList, identity, currentUrl):
		#adds to unique list if not seen before

		count = 0

		for i in inList:
			#check that URL is within scope of domain

			if (i in uniqueList) or (i in doneList):
				continue

			else:
				uniqueList.append(i)

					
		print(identity + '\'s found - ' + str(len(inList)) + ' // Unseen - ' + str(count))


	def noDupeUrl(urlList, toCrawlUrls, crawledUrls, currentUrl):

		count = 0
		countExt = 0

		for i in urlList:

			ignoreMe = False
			for j in ignore:
				#check if url points to unwanted file
				if (re.match('^.*' + j + '.*$', i)):
					ignoreMe = True
			if ignoreMe:
				continue
			

			if (i in toCrawlUrls) or (i in crawledUrls) or (i in externalUrls):
				#url already recorded
				continue


			elif re.match('^.*' + domain + '.*$', i):
				#url in scope
				toCrawlUrls.append(i)
				count += 1

			else:
				#url not in scope
				externalUrls.append(i)
				countExt += 1

		print('URL\'s found on page- ' + str(len(urlList)) + ' // Unseen - ' + str(count))
		print('Unique offsite URLs found - ' + str(countExt))


	def parseUrl(currentUrl):
		#take url and return HTML

		try:
			pageObject = requests.get(currentUrl)#, cookies=cookies)
		except:
			print('Unable to parse, check above URL for validity (maybe add / remove "www." prefix)\naccepted - domain.com, http://domain.com, https://domain.com')
			exit(1)

		return pageObject


	pageObject = parseUrl(currentUrl)
	print('\nDetails for ' + currentUrl + '\n')

	#extract and clean data
	urlList = re.findall('href="(https://.*?)"', pageObject.text)
	noDupeUrl(urlList, toCrawlUrls, crawledUrls, currentUrl)

	jsList = re.findall('(?:\'|src=")(.*\.js)', pageObject.text)
	noDupe(jsList, toCrawlJs, crawledJs, 'JS', currentUrl)

	phpList = re.findall('(?:\'|src=")(.*\.php)', pageObject.text)
	noDupe(phpList, toCrawlPhp, crawledPhp, 'PHP', currentUrl)

	emailList = re.findall('[^\w]([\w\d]+@[\w\d]*\.[\w\d\.]*)', pageObject.text)
	noDupe(emailList, uniqueEmail, uniqueEmail, 'Email', currentUrl)

	
	crawledUrls.append(currentUrl)


	del toCrawlUrls[0]
	print('\nUrls remaining to crawl: ' + str(len(toCrawlUrls)) + '\n\n')

	if len(toCrawlUrls) > 0:
		crawl(toCrawlUrls[0])
	else:
		print('All done.\n')

def report():
	print('\ncrawled Urls:')
	for i in crawledUrls:
		print(i)
	
	print('\nExtermal links:')
	for i in externalUrls:
		print(i)

	print('\nFound email addreses:')
	for i in uniqueEmail:
		print(i)

	print('\nFound JS:')
	for i in toCrawlJs:
		print(i)

	print('\nFound PHP:')
	for i in toCrawlPhp:
		print(i)
	exit(0)

#add cookies parameter to parseUrl() --- eg: pageObject = requests.get(currentUrl, cookies=cookies)
#cookies = {"toolbox_session":"eyJpdiI6InpoaU5ta2ZZTjFUNW45TjUycHE1NWc9PSIsInZhbHVlIjoidG9sOStOazhXa1JtbGc1S0ZQZ2VMQWpycU85eVNNSW1oK0pCMmZ1YlRuNU1oQWxqS1BRME5jZzRvTm1zU2pOQTNzdlVRd1Azbk1QM1dwNUREcUdXMWZ0VlVGTGdqYlVORk9uNEZOd1VUcFhaaEJwblVEenlndDI5RGVaZlVyUzYiLCJtYWMiOiI1YjgyYzA4OTMzYjFkMWM0M2VhYWE2NDdhNGNmMTAzMzFiMjljMjZlNmNjNTNlYTlkNzY0ZjY0MGEyZWU2YTMyIiwidGFnIjoiIn0%3D", "username": "eyJpdiI6IlBUMllkQTRFU0c5OW1qMHFTWDZzS0E9PSIsInZhbHVlIjoiNGhjeFhhZEJZaXlQN29ubUdPa2J3eTFYOEpXTE5aR3p2bFNna0MyQWxyaE9lSExqMWM2dHJrS0V5bHBJMXArSEdhanhuelNRY0Zuc1ZKbXdLVEVHRUE9PSIsIm1hYyI6ImNlMjU3YzBlNzA2MjI4ZTZlYjIwMzlhM2UwOGQ3NDk4ZmMwYjIzOTU1M2JlOWE0NmVhZDcxM2Q2ODI0MGQzYzciLCJ0YWciOiIifQ%3D%3D", "XSRF-TOKEN":"eyJpdiI6ImQyQjljenVtNm1XYzZsYXhKQzkxTWc9PSIsInZhbHVlIjoieHNJNzEwN1QwUEhhbUMwRENCVzVyd3g5Mi9nQmhFUC9BTnpuVmFwTlpYanBCdmFGZ2JLU05JUGtGM0JYRW1vVkh3MGRXeGNTS0hRRU43TTJBbCsybVF3MTBrNlRjZzV6YnYyVVNCMnB5d3RWdkdnTW1ZelRXU01aS0x2eEo4M1IiLCJtYWMiOiI1MjJhMGVkYjU1NWE1N2RmNGM0YzNjMDE1ZDUxMWMwMmEyMzU4MWYxYTBlM2U4N2FlZmFmZTM2ZjdkYjk5ZjE2IiwidGFnIjoiIn0%3D"}

ignore = ['jpg', 'png', 'svg']
#masterlists
externalUrls, crawledUrls, toCrawlUrls = [], [], []
crawledJs, toCrawlJs = [], []
crawledPhp, toCrawlPhp = [], []
uniqueEmail = []

currentUrl, domain = validateArgs()

crawl(currentUrl)
report()
