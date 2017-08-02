'''
SUPPORT
- http://blogtruyen.com/
- http://truyentranhtuan.com/
- http://www.mangapanda.com/
- http://hentaivn.net/
'''

#get link from command. Not require
from sys import argv

# each module has its own website
import blogtruyen
import truyentranhtuan
import mangapanda
import hentaivn

BLOGTRUYEN = 'http://blogtruyen.com/'
TRUYENTRANHTUAN = 'http://truyentranhtuan.com/'
MANGAPANDA = 'http://www.mangapanda.com'
HENTAIVN = 'http://hentaivn.net'

# scriptname and link
lenArgv = 2

def handleLink(link):
	if link.startswith(BLOGTRUYEN):
		try:
			data = blogtruyen.getDataFromBlogTruyen(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					blogtruyen.saveImgFromBlogTruyen(d)
			# notification done
			print('\a')
		except:
			exit()
	elif link.startswith(TRUYENTRANHTUAN):
		try:
			data = truyentranhtuan.getDataFromTruyenTranhTuan(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					truyentranhtuan.saveImgFromTruyenTranhTuan(d)
			# notification done
			print('\a')
		except:
			exit()
	elif link.startswith(MANGAPANDA):
		try:
			data = mangapanda.getDataFromMangaPanda(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					mangapanda.saveImgFromMangaPanda(d)
			# notification done
			print('\a')
		except:
			exit()
	elif link.startswith(HENTAIVN):
		try:
			data = hentaivn.getDataFromHentaiVn(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					hentaivn.saveImgFromHentaiVn(d)
			# notification done
			print('\a')
		except:
			exit()

def main():
	# if get link from argv
	if lenArgv == len(argv):
		link = argv[1]
	# else require from input
	else:
		link = input('Link: ')
	# go to check the link
	handleLink(link)

if __name__ == '__main__':
	main()