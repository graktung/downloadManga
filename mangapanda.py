from requests import get as requestsGet
import urllib.request as download
from bs4 import BeautifulSoup as besoup

import zipfiles

hostname = 'http://www.mangapanda.com'

def getDataFromMangaPanda(link):
	# get HTML source from original link
	HTML = requestsGet(link).text
	# crawl data from source html
	source = besoup(HTML, 'lxml')
	# get the title's content
	title = source.find('title').text.split('-')[0].strip()
	# find all chapters
	chapters = source.find(id='listing').find_all('a')
	# the number of chaps
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	# handle data for return
	data = []
	for chap in chapters:
		tempData = {}
		tempData['href'] = hostname + chap['href']
		tempData['title'] = chap.contents[0]
		# each item in data is a dict with 2 keys: 'title' and 'href'
		data.append(tempData)
	return data

def saveImgFromMangaPanda(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	# get HTML source from link chap
	HTML = requestsGet(data['href']).text
	source = besoup(HTML, 'lxml')
	num = len(source.find(id='pageMenu').find_all('option'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no in range(1, num + 1):
		# get each image from each url
		html = requests.get(data['href'] + '/' + str(no)).text
		source = besoup(html, 'lxml')
		link = source.find(id='img')['src']
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
	zipfiles.zipFile(filename + '-' + "mangapanda.com" + '.zip', files)
	print('Done!')