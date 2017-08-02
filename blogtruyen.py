from requests import get as requestsGet
from re import search as reSearch
import urllib.request as download
from bs4 import BeautifulSoup as besoup

import zipfiles

hostname = 'http://blogtruyen.com/'

def getDataFromBlogTruyen(link):
	HTML = requestsGet(link).text
	regexTitle = r'<title>.+\|'
	matchTitle = reSearch(regexTitle, HTML)
	if matchTitle.group() is not None:
		title = matchTitle.group().replace('<title>', '').rstrip('|').rstrip()
	else:
		title = 'Unknown'
	divListChapter = besoup(HTML, 'lxml')
	chapters = divListChapter.find(id='list-chapters')
	chapters = chapters.find_all('p')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		temp = chap.find('a')
		tempData['href'] = hostname + temp['href']
		tempData['title'] = temp['title']
		data.append(tempData)
	return data

def saveImgFromBlogTruyen(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requestsGet(data['href']).text
	source = besoup(HTML, 'lxml')
	article = source.find(id='content')
	imgs = article.find_all('img')
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, img in enumerate(imgs):
		fileExtension = img['src'].split('?')[0].split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			files.append(download.urlretrieve(img['src'], name)[0])
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	zipfiles.zipFile(filename + '-' + "blogtruyen.com" + '.zip', files)
	print('Done!')