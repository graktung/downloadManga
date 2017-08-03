from requests import get as requests_get
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://www.mangapanda.com'

def get_data_from_mangapanda(link):
	HTML = requests_get(link).text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('-')[0].strip()
	chapters = source.find(id='listing').find_all('a')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		tempData['href'] = hostname + chap['href']
		tempData['title'] = chap.contents[0]
		data.append(tempData)
	return data

def save_img_from_mangapanda(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requests_get(data['href']).text
	source = besoup(HTML, 'lxml')
	num = len(source.find(id='pageMenu').find_all('option'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no in range(1, num + 1):
		html = requests_get(data['href'] + '/' + str(no)).text
		source = besoup(html, 'lxml')
		link = source.find(id='img')['src']
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
	filehandle.zip_file(files, filename + '-' + "mangapanda.com" + '.zip')
	print('Done!')