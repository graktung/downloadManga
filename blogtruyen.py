from requests import get as requestsGet
from re import search as reSearch
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://blogtruyen.com/'

def getDataFromBlogTruyen(link):
	# get HTML source from original link
	HTML = requestsGet(link).text
	# catch the title
	regexTitle = r'<title>.+\|'
	matchTitle = reSearch(regexTitle, HTML)
	if matchTitle.group() is not None:
		title = matchTitle.group().replace('<title>', '').rstrip('|').rstrip()
	else:
		title = 'Unknown'
	# crawl data from source html
	divListChapter = besoup(HTML, 'lxml')
	chapters = divListChapter.find(id='list-chapters')
	chapters = chapters.find_all('p')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	# handle data for return
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
	# get HTML source from link chap
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
			# download file and get filename
			files.append(filehandle.downloadFile(img['src'], name))
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	# zip all files and remove them
	filehandle.zipFile(files, filename + '-' + "blogtruyen.com" + '.zip')
	print('Done!')