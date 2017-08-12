'''
- filehandle to download and zip files
- requests to get HTML source
- BeautifulSoup to crawl data
'''
import filehandle
import requests
from bs4 import BeautifulSoup


class BlogTruyen:
    '''
    I didn't know what I should write for
    docs string of this class
    so I decided to write this.
    Thanks for reading
    '''

    def __init__(self):
        self.hostname = 'http://blogtruyen.com'

    def get_data(self, link):
        '''
        GET:
        + the name of manga
        + links of all chapters
        '''
        html_source = requests.get(link).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        title_text = crawl_data.find('title').text
        # title_text = 'name | BlogTruyen.Com'
        manga_name = title_text.split('|')[0].strip()
        # each item in list_chapters
        # <a href="/id69669/chap-name-chap-num" id="id69669" target="_blank"
        # title="chap name chap num">chap name chap num</a>
        list_chapters = crawl_data.find(id='list-chapters').find_all('a')
        num_of_chaps = len(list_chapters)
        print('\n-> Detect\nWeb:', self.hostname, '\nManga: ', manga_name,
              '\nChaps:', num_of_chaps)
        # [{'name': .., 'link': ..}, {}, ..]
        data_list_chapters = list(map(lambda x: dict(name=x.text.strip(),
                                                     link=self.hostname +
                                                     x['href'])
                                      , list_chapters))
        return data_list_chapters

    @staticmethod
    def download_image(data_chapter):
        '''
        download all images from specific chap
        after that, zip them into a file
        '''
        print('Name:', data_chapter['name'], '\nLink:', data_chapter['link'])
        # chap name -> chap-name
        file_zip_name = '-'.join(data_chapter['name'].split())
        html_source = requests.get(data_chapter['link']).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        list_images = crawl_data.find(id='content').find_all('img')
        print('{}\nDownloading...'.format('-' * 50))
        # store all downloaded file names to zip
        downloaded_file_names = []
        for num, img in enumerate(list_images):
            # avoid variable in url
            # link?variable=value
            link_img = img['src'].split('?')[0]
            # http.link.file_extension
            file_extension = '.' + link_img.split('.')[-1]
            # check is image of not
            if file_extension.lower() not in ('.jpg', '.png', '.jpeg'):
                continue
            file_name = file_zip_name + '-' + str(num) + file_extension
            # filehandle.download_file object returns file_name
            downloaded_file_names.append(filehandle.FileHandle().download_file(
                link_img, file_name))
            print('Loaded', file_name, 'succesfully!')
        print('Zipping...')
        filehandle.FileHandle().zip_file(downloaded_file_names,
                                         file_zip_name + 'blogtruyen.com.zip')
        print('Done.')
