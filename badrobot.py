#!/usr/bin/python3
import requests
import re

host = 'https://host.com'

def attempt(file, reg0, reg1):
	#checks for existance of file.txt
	#separates wildcard entries
	#returns [[non wildcard urls], [wildcard urls]]

	print('checking if ' + file + '.txt exists')
	picker = requests.get(host + "/" + file + ".txt")

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

	return output

#filter out wildcards
reg0 = "^Disallow:\s.*[^\*]$"
#keep wildcards
reg1 = "^Disallow:\s.*\*.*$"
robot = attempt('robots', reg0, reg1)

#output indexes [[2XX], [3XX], [wildcards]]
output = [[], [], []]

for i in robot[0]:
	#iterates over non wildcards and include 2XX / 3XX responses
	print('Checking ' + i)
	urlcode = requests.get(i).status_code

	if re.match('^2\d\d$', str(urlcode)):
		print('SUCCESS ' + str(urlcode))
		output[0].append(i)
	elif re.match('^3\d\d$', str(urlcode)):
		print('REDIRECT ' + str(urlcode))
		output[1].append(i)

for i in robot[1]:
	output[2].append(i)

print(output)

#create and write to file
out = open('1.txt', 'w')

titles = ['2XX RESPONSES', '3XX RESPONSES', 'WILDCARDS']

for index, title in enumerate(titles):

	out.write('\n' + title + '\n\n')
	#convert list to dictionary and back - remove dupes
	noDupe = list(dict.fromkeys(output[index]))

	#write results to file
	for i in noDupe:
		out.write(i + '\n')

out.close()