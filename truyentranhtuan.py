'''
- re to find eval string in HTML source
- filehandle to download and zip file
- requests to get HTML source
- BeautifulSoup to crawl data
'''
import re
import filehandle
import requests
from bs4 import BeautifulSoup


class TruyenTranhTuan:
    '''
    don't read it
    it wastes your time
    I said did not read it
    '''

    def __init__(self):
        self.hostname = 'http://truyentranhtuan.com'

    def get_data(self, link):
        '''
        GET:
        + the name of manga
        + link of all chapters
        '''
        html_source = requests.get(link).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        title_text = crawl_data.find('title').text
        # title_text = chap name - Truyen tranh online - truyentranhtuan.com
        manga_name = title_text.split('-')[0].strip()
        list_chapters = crawl_data.find_all('span', class_='chapter-name')
        num_of_chaps = len(list_chapters)
        print('\n-> Detect\nWeb:', self.hostname, '\nManga: ', manga_name,
              '\nChaps:', num_of_chaps)
        # [{'name': .., 'link': ..}, {}, ..]
        data_list_chapters = list(map(lambda x: dict(name=x.find('a')
                                                     .text.strip()
                                                     .decode('utf-8'),
                                                     link=x.find('a')
                                                     ['href']), list_chapters))
        return data_list_chapters

    def download_image(self, data_chapter):
        '''
        download all images from specific chap
        after that, zip them into a file
        '''
        print('Name:', data_chapter['name'], '\nLink:',
              data_chapter['link'])
        # chap name -> chap-name
        file_zip_name = '-'.join(data_chapter['name'].split())
        html_source = requests.get(data_chapter['link']).text
        list_images = self.get_link_slides_page_url_path(html_source)
        print('{}\nDownloading...'.format('-' * 50))
        # store all downloaded file names to zip
        downloaded_file_names = []
        for num, img in enumerate(list_images):
            # avoid variable in url
            # link?variable=value
            link_img = img.split('?')[0]
            # link.file_extension
            file_extension = '.' + link_img.split('.')[-1]
            if file_extension.lower() not in ('.jpg', '.png', '.jpeg.'):
                continue
            file_name = file_zip_name + '-' + str(num) + file_extension
            # filehandle.download_file object returns file_name
            downloaded_file_names.append(filehandle.FileHandle().download_file(
                link_img, file_name))
            print('Loaded', file_name, 'successfully.')
        print('Zipping...')
        filehandle.FileHandle().zip_file(downloaded_file_names,
                                         file_zip_name +
                                         'truyentranhtuan.com.zip')
        print('Done.')

    @staticmethod
    def get_link_slides_page_url_path(html_source):
        '''
        this page use js variable to hold all of link image
        so we have to this content follow by string
        and handle it.
        It likes this
        var slides_page_url_path = ["link", "link"];
        Let's see what I do ;)
        '''
        regex_get_string = r'var slides_page_url_path.+;'
        long_string_link = re.search(regex_get_string, html_source).group()
        regex_get_string_link = r'".+"'
        short_string_link = re.search(regex_get_string_link,
                                      long_string_link).group()
        list_links = list(map(lambda x: x.strip('"'),
                              short_string_link.split(',')))
        return list_links
