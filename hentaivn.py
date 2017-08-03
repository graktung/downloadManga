from requests import get as requests_get
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://hentaivn.net'

def get_data_from_hentaivn(link):
	HTML = requests_get(link).text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('[')[0].split(':')[1].strip()
	chapters =  source.find(class_='listing').find_all('a')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		title = chap.find(class_='chuong_t')
		if title is None:
			continue
		tempData['href'] = hostname + chap['href']
		tempData['title'] = title['title']
		data.append(tempData)
	return data

def save_img_from_hentaivn(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requests_get(data['href']).text
	source = besoup(HTML, 'lxml')
	links = map(lambda x: x['src'].split('?')[0], source.find(id='image').find_all('img'))
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
	filehandle.zip_file(files, filename + '-' + "hentaivn.net" + '.zip')
	print('Done!')