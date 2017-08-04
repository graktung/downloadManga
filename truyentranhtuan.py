from requests import get as requests_get
from re import search as re_search
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://truyentranhtuan.com/'

def get_data(link):
	HTML = requests_get(link).text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('-')[0].strip()
	chapters = source.find_all('span', class_='chapter-name')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		temp = chap.find('a')
		tempData['href'] = temp['href']
		tempData['title'] = chap.text.strip()
		data.append(tempData)
	return data

def save_img(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requests_get(data['href']).text
	regex = r'var slides_page_url_path.+;'
	m = re_search(regex, HTML)
	regex = r'".+"'
	m = re_search(regex, m.group())
	links = map(lambda x: x.strip('"'), m.group().split(','))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('?')[0].split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			files.append(filehandle.download_file(link, name))
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	filehandle.zip_file(files, filename + '-' + "truyentranhtuan.com" + '.zip')
	print('Done!')