from requests import get as requestsGet
import urllib.request as download
from bs4 import BeautifulSoup as besoup

import zipfiles

hostname = 'http://hentaivn.net'

def getDataFromHentaiVn(link):
	# get HTML source from original link
	HTML = requestsGet(link).text
	# crawl data from source html
	source = besoup(HTML, 'lxml')
	# get the title's content
	title = source.find('title').text.split('[')[0].split(':')[1].strip()
	# find all chapters
	chapters =  source.find(class_='listing').find_all('a')
	# the number of chaps
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	# handle data for return
	data = []
	for chap in chapters:
		tempData = {}
		title = chap.find(class_='chuong_t')
		if title is None:
			continue
		tempData['href'] = hostname + chap['href']
		tempData['title'] = title['title']
		# each item in data is a dict with 2 keys: 'title' and 'href'
		data.append(tempData)
	return data

def saveImgFromHentaiVn(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	# get HTML source from link chap
	HTML = requestsGet(data['href']).text
	source = besoup(HTML, 'lxml')
	links = map(lambda x: x['src'].split('?')[0], source.find(id='image').find_all('img'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			# download file and get filename
			files.append(download.urlretrieve(link, name)[0])
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	# zip all files and remove them
	zipfiles.zipFile(filename + '-' + "hentaivn.net" + '.zip', files)
	print('Done!')