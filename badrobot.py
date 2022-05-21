#!/usr/bin/python3
import requests
import re
import argparse

#usage
#badRobot.py -d [domain] (https:// is added automaticaly)

parser = argparse.ArgumentParser(description='A tool to analyse robots.txt and return a list for investigation')
parser.add_argument('-d', type=str,  help='Domain to analyse')
args=parser.parse_args()

host = 'https://' + args.d
print('Assessing ' + host + '\n\n')

def attempt(file, reg0, reg1, reg2):
	#checks for existance of file.txt
	#separates wildcard entries
	#returns [[non wildcard urls], [wildcard urls]]

	print('checking if ' + file + ' exists')
	picker = requests.get(host + "/" + file)

	if picker.status_code != 200:
		print('Failed: ' + str(picker.status_code))
		return 'Failed'
		exit(1)
	else:
		print('Success')

		output = [[], []]

	for line in picker.iter_lines(decode_unicode=True):
		if re.match(reg0, line):
			output[0].append(host + line[10:])
		elif re.match(reg1, line):
			output[1].append(host + line[10:])
		elif re.match(reg2, line):
			if len(output) != 3:
				print('Sitemap found\nChecking status')
				if requests.get(host + '/sitemap.xml').status_code == 200:
					print('Success - 200')
					output.append(host + line[9:])

	return output

#filter out wildcards
reg0 = "^Disallow:\s.*[^\*]$"
#keep wildcards
reg1 = "^Disallow:\s.*\*.*$"
#look for sitemap
reg2 = '^Sitemap:\s.*\.xml'

robot = attempt('robots.txt', reg0, reg1, reg2)

#output indexes [[2XX], [3XX], [wildcards]]
output = [[], [], []]

#if exists, move sitemap to output list
if len(robot) == 3:
	output.append(robot[2])

for i in robot[0]:
	#iterates over non wildcards and include 2XX / 3XX responses
	print('Checking ' + i)
	urlcode = requests.get(i).status_code

	if re.match('^2\d\d$', str(urlcode)):
		print('SUCCESS - ' + str(urlcode))
		output[0].append(i)
	elif re.match('^3\d\d$', str(urlcode)):
		print('REDIRECT - ' + str(urlcode))
		output[1].append(i)

for i in robot[1]:
	output[2].append(i)

print(output)

#create and write to file
out = open(args.d + '.txt', 'w')
out.write(host + '\n\n')

#write sitemap
if len(output) == 4:
	out.write('\nSITEMAP\n\n' + output[3] + '\n')

titles = ['2XX RESPONSES', '3XX RESPONSES', 'WILDCARDS']

for index, title in enumerate(titles):

	out.write('\n' + title + '\n\n')
	#convert list to dictionary and back - remove dupes
	noDupe = list(dict.fromkeys(output[index]))

	#write results to file
	for i in noDupe:
		out.write(i + '\n')

out.close()