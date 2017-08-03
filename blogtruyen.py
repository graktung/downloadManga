from requests import get as requests_get
from re import search as re_search
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://blogtruyen.com/'

def get_data_from_blog_truyen(link):
	HTML = requests_get(link).text
	regexTitle = r'<title>.+\|'
	matchTitle = re_search(regexTitle, HTML)
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

def save_img_from_blog_truyen(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	HTML = requests_get(data['href']).text
	source = besoup(HTML, 'lxml')
	article = source.find(id='content')
	imgs = article.find_all('img')
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, img in enumerate(imgs):
		fileExtension = img['src'].split('?')[0].split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			files.append(filehandle.download_file(img['src'], name))
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	filehandle.zip_file(files, filename + '-' + "blogtruyen.com" + '.zip')
	print('Done!')