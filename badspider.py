#!/usr/bin/python3
import requests
import re
import argparse

#usage
#badspider.py -d [domain] (https:// is added automaticaly)

parser = argparse.ArgumentParser(description='A tool to spider a domain and return a list for investigation')
parser.add_argument('-d', type=str,  help='Domain to analyse')
args=parser.parse_args()

if not re.match('^(?:http://|https://).*$', args.d):
	host = 'https://' + args.d
else:
	host = args.d

print('Assessing ' + host + '\n')

try:
	root = requests.get(host)
except:
	print('Unable to parse, check above URL for validity\naccepted - domain.com, http://domain.com, https://domain.com')
	exit(1)
def crawl(root):

	#urllist = re.findall('href="(https://.*?)"', root.text)

	#jsList = re.findall('(?:\'|src=")(.*\.js)', root.text)

	emailList = re.findall('[^\w]([\w\d]*@[\w\d]*\.[\w\d]*?)', root.text)
	print(emailList)
crawl(root)