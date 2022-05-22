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

			elif re.match('.*' + domain + '.*', i):
				uniqueList.append(i)
				count += 1

			else:
				#Url points externally
				if (i not in externalUrls):
					externalUrls.append(i)
					
		print(identity + '\'s found - ' + str(len(inList)) + ' // Unseen - ' + str(count))


	def noDupeUrl(urlList, toCrawlUrls, crawledUrls, currentUrl):

		count = 0
		countExt = 0

		for i in urlList:

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
			pageObject = requests.get(currentUrl)
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

	emailList = re.findall('[^\w]([\w\d]*@[\w\d]*\.[\w\d]*?)', pageObject.text)
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

	exit(0)


#masterlists
externalUrls, crawledUrls, toCrawlUrls = [], [], []
crawledJs, toCrawlJs = [], []
uniqueEmail = []

currentUrl, domain = validateArgs()

crawl(currentUrl)
report()
