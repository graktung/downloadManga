'''
SUPPORT
- http://blogtruyen.com/
- http://truyentranhtuan.com/
- http://www.mangapanda.com/
- http://hentaivn.net/
- http://manganel.com/
'''

#get link from command. Not require
from sys import argv

# each module has its own website
import blogtruyen
import truyentranhtuan
import mangapanda
import hentaivn
import manganel

BLOGTRUYEN = 'http://blogtruyen.com/'
TRUYENTRANHTUAN = 'http://truyentranhtuan.com/'
MANGAPANDA = 'http://www.mangapanda.com'
HENTAIVN = 'http://hentaivn.net'
MANGANEL = 'http://manganel.com'

# scriptname and link
lenArgv = 2

def handle_link(link):
	if link.startswith(BLOGTRUYEN):
		try:
			data = blogtruyen.get_data_from_blog_truyen(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					blogtruyen.save_img_from_blog_truyen(d)
			# notification done
			print('\a')
		except:
			exit()
	elif link.startswith(TRUYENTRANHTUAN):
		try:
			data = truyentranhtuan.get_data_from_truyentranhtuan(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					truyentranhtuan.save_img_from_truyentranhtuan(d)
			# notification done
			print('\a')
		except:
			exit()
	elif link.startswith(MANGAPANDA):
		try:
			data = mangapanda.get_data_from_mangapanda(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					mangapanda.save_img_from_mangapanda(d)
			# notification done
			print('\a')
		except:
			exit()
	elif link.startswith(HENTAIVN):
		try:
			data = hentaivn.get_data_from_hentaivn(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					hentaivn.save_img_from_hentaivn(d)
			# notification done
			print('\a')
		except:
			exit()
	elif link.startswith(MANGANEL):
		try:
			data = manganel.get_data_from_manganel(link)
			askDown = input('Download (y/n) ')
			if askDown.lower().strip() in ('y', 'yes'):
				for d in data:
					manganel.save_img_from_manganel(d)
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
	handle_link(link)

if __name__ == '__main__':
	main()