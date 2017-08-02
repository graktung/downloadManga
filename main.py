'''
SUPPORT
- http://blogtruyen.com/
- http://truyentranhtuan.com/
- http://www.mangapanda.com/
- http://hentaivn.net/
'''

# handle HTML and load files
import requests
import re
import urllib.request as download
from bs4 import BeautifulSoup as besoup

# folders and files
import zipfile
import os

from sys import argv

BLOGTRUYEN = 'http://blogtruyen.com/'
TRUYENTRANHTUAN = 'http://truyentranhtuan.com/'
MANGAPANDA = 'http://www.mangapanda.com'
HENTAIVN = 'http://hentaivn.net'

lenArgv = 2

def saveImgFromBlogTruyen(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	req = requests.get(data['href'])
	HTML = req.text
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
	zipf = zipfile.ZipFile(filename + '-' + "blogtruyen.com" + '.zip', 'w', zipfile.ZIP_DEFLATED)
	print('Zipping...')
	for file in files:
		zipf.write(file)
		os.remove(file)
	zipf.close()
	print('Done!')

def saveImgFromTruyenTranhTuan(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	req = requests.get(data['href'])
	HTML = req.text
	regex = r'var slides_page_url_path.+;'
	m = re.search(regex, HTML)
	regex = r'".+"'
	m = re.search(regex, m.group())
	links = map(lambda x: x.strip('"'), m.group().split(','))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('?')[0].split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			files.append(download.urlretrieve(link, name)[0])
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	zipf = zipfile.ZipFile(filename + '-' + "truyentranhtuan.com" + '.zip', 'w', zipfile.ZIP_DEFLATED)
	print('Zipping...')
	for file in files:
		zipf.write(file)
		os.remove(file)
	zipf.close()
	print('Done!')

def saveImgFromMangaPanda(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	req = requests.get(data['href'])
	HTML = req.text
	source = besoup(HTML, 'lxml')
	num = len(source.find(id='pageMenu').find_all('option'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no in range(1, num + 1):
		html = requests.get(data['href'] + '/' + str(no)).text
		source = besoup(html, 'lxml')
		link = source.find(id='img')['src']
		fileExtension = link.split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			print(link)
			files.append(download.urlretrieve(link, name)[0])
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	zipf = zipfile.ZipFile(filename + '-' + "mangapanda.com" + '.zip', 'w', zipfile.ZIP_DEFLATED)
	print('Zipping...')
	for file in files:
		zipf.write(file)
		os.remove(file)
	zipf.close()
	print('Done!')

def saveImgFromHentaiVn(data):
	print('Title:', data['title'], '\nLink:', data['href'])
	filename = '-'.join(data['title'].split())
	req = requests.get(data['href'])
	HTML = req.text
	source = besoup(HTML, 'lxml')
	links = map(lambda x: x['src'].split('?')[0], source.find(id='image').find_all('img'))
	files = []
	print('{}\nDownloading...'.format('-' * 50))
	for no, link in enumerate(links, 1):
		fileExtension = link.split('.')[-1]
		try:
			name = filename + '-' + str(no) + '.' + fileExtension
			files.append(download.urlretrieve(link, name)[0])
			print('Loaded', name, 'Successfully!')
		except KeyboardInterrupt:
			exit()
		except:
			print('Missed %r' %(filename + '-' + str(no) + '.' + fileExtension))
	zipf = zipfile.ZipFile(filename + '-' + "hentaivn.net" + '.zip', 'w', zipfile.ZIP_DEFLATED)
	print('Zipping...')
	for file in files:
		zipf.write(file)
		os.remove(file)
	zipf.close()
	print('Done!')

def getDataFromBlogTruyen(link):
	blogtruyenRequest = requests.get(link)
	HTML = blogtruyenRequest.text
	regexTitle = r'<title>.+\|'
	matchTitle = re.search(regexTitle, HTML)
	if matchTitle.group() is not None:
		title = matchTitle.group().replace('<title>', '').rstrip('|').rstrip()
	else:
		title = 'Unknown'
	divListChapter = besoup(HTML, 'lxml')
	chapters = divListChapter.find(id='list-chapters')
	chapters = chapters.find_all('p')
	num = len(chapters)
	print('\n-> Detect\nWeb:', BLOGTRUYEN, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		temp = chap.find('a')
		tempData['href'] = BLOGTRUYEN + temp['href']
		tempData['title'] = temp['title']
		data.append(tempData)
	return data

def getDataFromTruyenTranhTuan(link):
	truyentranhtuanRequest = requests.get(link)
	HTML = truyentranhtuanRequest.text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('-')[0].strip()
	chapters = source.find_all('span', class_='chapter-name')
	num = len(chapters)
	print('\n-> Detect\nWeb:', TRUYENTRANHTUAN, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		temp = chap.find('a')
		tempData['href'] = temp['href']
		tempData['title'] = chap.text.strip()
		data.append(tempData)
	return data

def getDataFromMangaPanda(link):
	mangapandaRequest = requests.get(link)
	HTML = mangapandaRequest.text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('-')[0].strip()
	chapters = source.find(id='listing').find_all('a')
	num = len(chapters)
	print('\n-> Detect\nWeb:', TRUYENTRANHTUAN, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		tempData['href'] = MANGAPANDA + chap['href']
		tempData['title'] = chap.contents[0]
		data.append(tempData)
	return data

def getDataFromHentaiVn(link):
	hentaivnRequest = requests.get(link)
	HTML = hentaivnRequest.text
	source = besoup(HTML, 'lxml')
	title = source.find('title').text.split('[')[0].split(':')[1].strip()
	chapters =  source.find(class_='listing').find_all('a')
	num = len(chapters)
	print('\n-> Detect\nWeb:', TRUYENTRANHTUAN, '\nManga: ', title, '\nChaps:', num)
	data = []
	for chap in chapters:
		tempData = {}
		title = chap.find(class_='chuong_t')
		if title is None:
			continue
		tempData['href'] = HENTAIVN + chap['href']
		tempData['title'] = title['title']
		data.append(tempData)
	return data	

def handleLink(link):
	if link.startswith(BLOGTRUYEN):
		data = getDataFromBlogTruyen(link)
		askDown = input('Download (y/n) ')
		if askDown.lower().strip() in ('y', 'yes'):
			for d in data:
				saveImgFromBlogTruyen(d)
		# notification done
		print('\a')
	elif link.startswith(TRUYENTRANHTUAN):
		data = getDataFromTruyenTranhTuan(link)
		askDown = input('Download (y/n) ')
		if askDown.lower().strip() in ('y', 'yes'):
			for d in data:
				saveImgFromTruyenTranhTuan(d)
		# notification done
		print('\a')
	elif link.startswith(MANGAPANDA):
		data = getDataFromMangaPanda(link)
		askDown = input('Download (y/n) ')
		if askDown.lower().strip() in ('y', 'yes'):
			for d in data:
				saveImgFromMangaPanda(d)
		# notification done
		print('\a')
	elif link.startswith(HENTAIVN):
		data = getDataFromHentaiVn(link)
		askDown = input('Download (y/n) ')
		if askDown.lower().strip() in ('y', 'yes'):
			for d in data:
				saveImgFromHentaiVn(d)
		# notification done
		print('\a')

def main():
	if lenArgv == len(argv):
		link = argv[1]
	else:
		link = input('Link: ')
	handleLink(link)

if __name__ == '__main__':
	main()