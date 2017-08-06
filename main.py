'''
SUPPORT
- http://blogtruyen.com/
- http://truyentranhtuan.com/
- http://www.mangapanda.com/
- http://hentaivn.net/
- http://manganel.com/
- http://truyentranh8.net/
'''

import threading
from time import sleep
from os import system, mkdir
# get link from command and download immediately. Not require
from sys import argv

SUPPORT_WEBSITES_DOWNLOAD = [
	{'domain': 'http://blogtruyen.com/', 'module': 'blogtruyen'},
	{'domain': 'http://truyentranhtuan.com/', 'module': 'truyentranhtuan'},
	{'domain': 'http://www.mangapanda.com', 'module': 'mangapanda'},
	{'domain': 'http://hentaivn.net', 'module': 'hentaivn'},
	{'domain': 'http://manganel.com', 'module': 'manganel'},
	{'domain': 'http://truyentranh8.net/', 'module': 'truyentranh8'}
]

SUPPORT_WEBSITES_SEARCH = [
	{'domain': 'http://manganel.com', 'module': 'manganel'},
	{'domain': 'http://truyentranh8.net/', 'module': 'truyentranh8'}
]

# scriptname and link
lenArgv = 2
# get the maximum threading
try:
	with open('database/configthreading.txt') as f:
		nTs = f.read().strip()
		if nTs.isdigit():
			nTs = int(nTs) if int(nTs) <= 10 else 3
		else:
			nTs = 1
except:
	try:
		with open('database/configthreading.txt', 'w') as f:
			f.write('1')
	except:
		mkdir('database')
		with open('database/configthreading.txt', 'w') as f:
			f.write('1')
	nTs = 1

def get_and_down(moduleDownload, link):
	try:
		data = moduleDownload.get_data(link)
		askDown = input('Download (y/n) ')
		if askDown.lower().strip() in ('y', 'yes'):
			n = input('How many? ')
			if not n.isdigit() or n.lower().strip() == ('all'):
				n = None
			else:
				n = int(n)
			for i in range(0, n, nTs):
				for d in data[i: i + nTs if i + nTs < n else n]:
					threading.Thread(target=moduleDownload.save_img, \
										args=(d,)).start()
				# if there's not only main thread
				while threading.active_count() != 1:
					sleep(0.1)
		# notification done
		print('\a')
	except:
		exit()

def handle_link_download(link):
	for site in SUPPORT_WEBSITES_DOWNLOAD:
		if site['domain'] in link:
			moduleDownload = __import__(site['module'])
			get_and_down(moduleDownload, link)
			break

def handle_search(keyword, n):
	data = []
	for site in SUPPORT_WEBSITES_SEARCH:
		data.append(__import__(site['module']).search(keyword, n))
	if len(data) == 0:
		print('No results found from keyword %r' %keyword)
		return None
	for d in data:
		print('Enter to continue, Ctrl + C to stop')
		try:
			print('=' * 50, '\n')
			print('Web:' + d[0] + '\n')
			for f in d[1:]:
				print('-' * 50)
				print('Name:', f[0]['title'], '\nLatest:', f[1]['title'])
				print('+' * 50)
				print('Chap:       ', f[0]['href'])
				print('Latest chap:', f[1]['href'])
				try:
					input()
				except KeyboardInterrupt:
					print()
					break
			input()
		except KeyboardInterrupt:
			print()
			break

def load_only(link):
	try:
		for site in SUPPORT_WEBSITES_DOWNLOAD:
			if site['domain'] in link:
				moduleDownload = __import__(site['module'])
				moduleDownload.save_img({'title': site['module'],\
										'href': link})
				break
		print('\a')
	except:
		exit()

def read_command():
	command = ''
	while command == '':
		command = input('=]] ').lower().strip()
	return command

def decide(command):
	if command in ('load', 'download', 'down'):
		link = input('Link: ')
		# go to check the link
		handle_link_download(link)
	elif command in ('load only'):
		link = input('Link: ')
		load_only(link)
	elif command in ('search', 'serch', 'sarch'):
		key = input('Keyword: ')
		nResult = input('Which maximum results do u wanna display: ')
		if not nResult.isdigit() or nResult.lower().strip() == ('all'):
			nResult = None
		else:
			nResult = int(nResult)
		handle_search(key, nResult)
	elif command in ('cls', 'clear', 'cear'):
		system('cls')
	elif command in ('quit', 'q', 'exit'):
		exit()

def main():
	# if get link from argv
	if lenArgv == len(argv):
		link = argv[1]
	else:
		while 1:
			command = read_command()
			decide(command)

if __name__ == '__main__':
	main()