from requests import get as requestsGet
from re import search as reSearch
from bs4 import BeautifulSoup as besoup

import filehandle

hostname = 'http://truyentranhtuan.com/'

def get_data_from_truyentranhtuan(link):
	# get HTML source from original link
	HTML = requestsGet(link).text
	# crawl data from source html
	source = besoup(HTML, 'lxml')
	# catch the title
	title = source.find('title').text.split('-')[0].strip()
	chapters = source.find_all('span', class_='chapter-name')
	num = len(chapters)
	print('\n-> Detect\nWeb:', hostname, '\nManga: ', title, '\nChaps:', num)
	# handle data for return
	data = []
	for chap in chapters:
		tempData = {}
		temp = chap.find('a')
		tempData['href'] = temp['href']
		tempData['title'] = chap.text.strip()
		data.append(tempData)
	return data

def save_img_from_truyentranhtuan(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	# get HTML source from link chap
	HTML = requestsGet(data['href']).text
	# get all link img from javascript variable.
	regex = r'var slides_page_url_path.+;'
	m = reSearch(regex, HTML)
	regex = r'".+"'
	m = reSearch(regex, m.group())
	links = map(lambda x: x.strip('"'), m.group().split(','))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('?')[0].split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			# download file and get filename
			files.append(filehandle.download_file(link, name))
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	print('Zipping...')
	# zip all files and remove them
	filehandle.zip_file(files, filename + '-' + "truyentranhtuan.com" + '.zip')
	print('Done!')