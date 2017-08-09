'''
- filehandle to download and zip files
- requests to get HTML source
- BeautifulSoup to crawl data
'''
import filehandle
import requests
from bs4 import BeautifulSoup


class HentaiVN:
    '''
    Now, come on, my docs string is really nonsense
    don't watse time to read it
    '''

    def __init__(self):
        self.hostname = 'http://hentaivn.net'

    def get_data(self, link):
        '''
        GET:
        + the name of manga
        + links of all chapters
        '''
        html_source = requests.get(link).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        title_text = crawl_data.find('title').text
        # title_text = 'Truyện Hentai: chap name
        # [chap name] | Đọc Online'
        manga_name = title_text.split(':')[1].split('[')[0].strip()
        # each item in list_chapters
        # <td class="chuong_td">
        # <a target="_blank"
        # href="link">
        # <h2 class="chuong_t"
        # title="chap name chap num">
        # chap name chap num</h2></a>
        # </td>
        list_chapters = crawl_data.find('tbody').find_all(
            class_='chuong_td')[1:]
        num_of_chaps = len(list_chapters)
        print('\n-> Detect\nWeb:', self.hostname, '\nManga: ', manga_name,
              '\nChaps:', num_of_chaps)
        # [{'name:': .., 'link': ..}, {}, ..]
        data_list_chapters = list(map(lambda x: dict(
            name=x.text.strip(),
            link=self.hostname + x.find('a')['href']),
                                      list_chapters))
        return data_list_chapters

    @staticmethod
    def download_image(data_chapter):
        '''
        Download all images from specific chap
        after that, zip them all into a file
        '''
        print('Name:', data_chapter['name'], '\nLink:', data_chapter['link'])
        # chap name -> chap-name
        file_zip_name = '-'.join(data_chapter['name'].split())
        html_source = requests.get(data_chapter['link']).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        list_images = crawl_data.find(id='image').find_all('img')
        print('{}\nDownloading...'.format('-' * 50))
        # store all downloaded file names to zip
        downloaded_file_names = []
        for num, img, in enumerate(list_images):
            # avoid variable in url
            # link?variable=value
            link_img = img['src'].split('?')[0]
            # http.link.file_extension
            file_extension = '.' + link_img.split('.')[-1]
            if file_extension.lower() not in ('.jpg', '.png', '.jpeg'):
                continue
            file_name = file_zip_name + '-' + str(num) + file_extension
            # filehandle.download_file object returns file_name
            downloaded_file_names.append(filehandle.FileHandle().download_file(
                link_img, file_name))
            print('Loaded', file_name, 'succesfully!')
        print('Zipping...')
        filehandle.FileHandle().zip_file(downloaded_file_names,
                                         file_zip_name + 'hentaivn.net.zip')
        print('Done.')
