'''
- filehandle to download and zip files
- requests to get HTML source
- BeautifulSoup to crawl data
'''
import filehandle
import requests
from bs4 import BeautifulSoup


class MangaPanda:
    '''
    No idea for docs string,
    sorry guy
    but to be honest
    there'se nothing.
    '''

    def __init__(self):
        self.hostname = 'http://www.mangapanda.com'

    def get_data(self, link):
        '''
        GET:
        + the name of manga
        + links of all chapters
        '''
        html_source = requests.get(link).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        title_text = crawl_data.find('title').text
        # title_text = 'chap name Manga - Read chap name Online For Free'
        manga_name = title_text.split('-')[0].replace('Manga', '').strip()
        # each item in list_chapters
        # <a href="link">chap name</a>
        list_chapters = crawl_data.find(id='listing').find_all('a')
        num_of_chaps = len(list_chapters)
        print('\n-> Detect\nWeb:', self.hostname, '\nManga: ', manga_name,
              '\nChaps:', num_of_chaps)
        data_list_chapters = list(map(lambda x: dict(name=x.text.strip(),
                                                     link=self.hostname +
                                                     x['href']),
                                      list_chapters))
        return data_list_chapters

    def download_image(self, data_chapter):
        '''
        download all images from specific chap
        after that zip them into a file
        '''
        print('Name:', data_chapter['name'], '\nLink:', data_chapter['link'])
        file_zip_name = '-'.join(data_chapter['name'].split())
        html_source = requests.get(data_chapter['link']).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        # each option contains each link of image
        list_image_in_options = crawl_data.find_all('option')
        list_images = map(lambda x: self.get_link_img(self.hostname +
                                                      x['value']),
                          list_image_in_options)
        print('{}\nDownloading...'.format('-' * 50))
        # store all downloaded file names to zip
        downloaded_file_names = []
        for num, img in enumerate(list_images):
            # avoid variable in url
            # link?variable=value
            link_img = img.split('?')[0]
            # http.link.file_extension
            file_extension = '.' + link_img.split('.')[-1]
            if file_extension.lower() not in ('.jpg', '.png', '.jpeg'):
                continue
            file_name = file_zip_name + '-' + str(num) + file_extension
            # filehandle.download_file object returns file_name
            downloaded_file_names.append(filehandle.FileHandle().download_file(
                link_img, file_name))
            print('Loaded', file_name, 'successfully.')
        print('Zipping...')
        filehandle.FileHandle().zip_file(downloaded_file_names,
                                         file_zip_name + 'mangapanda.com.zip')
        print('Done.')

    @staticmethod
    def get_link_img(link):
        '''
        get link img
        I have to code this
        because, each url
        contains each img.
        1 url not contains all of images like other websites
        '''
        html_source = requests.get(link).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        img = crawl_data.find('img', id='img')['src']
        return img
