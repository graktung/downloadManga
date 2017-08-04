from requests import get as requests_get
from re import search as re_search, findall as find_all
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://manganel.com'
linkSearch = 'http://manganel.com/search/'

def get_data(link):
	HTML = requests_get(link).text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('Manga')[0].replace('Read', '').strip()
	chapters = source.find(class_='chapter-list').find_all('a')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		tempData['href'] = chap['href']
		tempData['title'] = chap.contents[0]
		data.append(tempData)
	return data

def save_img(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requests_get(data['href']).text
	source = besoup(HTML, 'lxml')
	links = map(lambda x: x['src'], source.find(id='vungdoc').find_all('img'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			files.append(filehandle.download_file(link, name))
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	filehandle.zip_file(files, filename + '-' + "manganel.com" + '.zip')
	print('Done!')

def search(keyword, num):
	regexKeyword = r'\w+'
	key = '_'.join(find_all(regexKeyword, keyword))
	HTML = requests_get(linkSearch + key).text
	source = besoup(HTML, 'lxml')
	results = source.find_all(class_='daily-update-item')[:num]
	results = map(lambda x: x.find_all('a'), results)
	results = [hostname] + list(map(lambda x: [{'title': x[0].text, 'href': x[0]['href']}\
								, {'title': x[1].text, 'href': x[1]['href']}],\
								results))
	return results