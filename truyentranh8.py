from requests import get as requests_get
from bs4 import BeautifulSoup as besoup
from re import search as re_search, findall as re_findall
from jsbeautifier import beautify

import filehandle

hostname = 'http://truyentranh8.net/'

def getInt(link):
	name = link.split('/')[-1].split('-')[-1].split('.')[0]
	n = ''
	for letter in n[::-1]:
		if letter.isdigit():
			n += letter
		else:
			break
	if n != '':
		return n[::-1]
	return 1

def get_data(link):
	HTML = requests_get(link).text
	source = besoup(HTML, 'lxml')
	title = source.find('title').contents[0].split('(')[0].strip()
	chapters = source.find(id='ChapList').find('ul').find_all('a')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		tempData['href'] = chap['href']
		h2 = chap.find('h2')
		title = h2.find('span').contents[0].strip() + ' ' \
									+ h2.find('strong').contents[0]
		tempData['title'] = title
		data.append(tempData)
	return data

def get_link_img(html):
	regexEval = r'eval.+'
	regexLink = r'http:\/\/.+"'
	jsEval = re_search(regexEval, html)
	jsUnEval = beautify(jsEval.group())
	listLink = map(lambda x: x.rstrip('"').split('?')[0], \
		re_findall(regexLink, jsUnEval))
	return sorted((set(listLink)), key=lambda x: int(getInt(x)))

def save_img(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requests_get(data['href']).text
	links = get_link_img(HTML)
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