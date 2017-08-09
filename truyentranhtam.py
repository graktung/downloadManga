'''
- re to find eval string in HTML source
- filehandle to download and zip files
- requests to get HTML source
- BeautifulSoup to crawl data
- beautify to decode eval javascript string
'''
import re
import filehandle
import requests
from bs4 import BeautifulSoup
from jsbeautifier import beautify


class TruyenTranhTam:
    '''
    no docs string
    don't read
    unless you have unlimited time
    '''

    def __init__(self):
        self.hostname = 'http://truyentranh8.net'

    def get_data(self, link):
        '''
        GET:
        + the name of manga
        + links of all chapters
        '''
        html_source = requests.get(link).text
        crawl_data = BeautifulSoup(html_source, 'lxml')
        title_text = crawl_data.find('title').text
        # title_text = 'chap name - Truyện Tranh'
        manga_name = title_text.split('-')[0].strip()
        # drop 3 element from head because not element in list chapters
        list_chapters = crawl_data.find_all(itemprop='itemListElement')[3:]
        # each item in list_chapters
        # <a itemprop="itemListElement" href=link title=chap name><li><h2>
        # text[1]<span class="hm"> some unuseful text </span> <strong>text[0]
        # </strong>
        # <time datetime=datime-string title=datime-string>time-update</time>
        # </h2></li></a>
        num_of_chaps = len(list_chapters)
        print('\n-> Detect\nWeb:', self.hostname, '\nManga: ', manga_name,
              '\nChaps:', num_of_chaps)
        # [{'name': .., 'link': ..}, {}, ..]
        data_list_chapters = list(map(lambda x: dict(
            name=' '.join(x.text.split('\n')), link=x['href']), list_chapters))
        return data_list_chapters

    def download_image(self, data_chapter):
        '''
        download all images from specific chap
        after that zip them into a file
        '''
        print('Name:', data_chapter['name'], '\nLink:', data_chapter['link'])
        # chap name -> chap-name
        file_zip_name = '-'.join(data_chapter.split())
        html_source = requests.get(data_chapter['link']).text
        list_link_images = self.sort_link(self.get_link_by_regex(
            self.decode_eval(
                self.get_eval_string(html_source))))
        print('{}\nDownloading...'.format('-' * 50))
        # store all downloaded file names to zip
        downloaded_file_names = []
        for num, link in enumerate(list_link_images):
            # avoid variable in url
            # link?variable=value
            file_extension = '.' + link.split('.')[-1]
            if file_extension.lower() not in ('.jpg', '.png', '.jpeg'):
                continue
            file_name = file_zip_name + '-' + str(num) + file_extension
            # filehandle.download_file object returns file_name
            downloaded_file_names.append(filehandle.FileHandle().download_file(
                link, file_name))
            print('Loaded', file_name, 'successfully.')
        print('Zipping...')
        filehandle.FileHandle().zip_file(downloaded_file_names,
                                         file_zip_name + 'truyentranh8.net.zip')
        print('Done.')

    def sort_link(self, list_links):
        '''
        don't waste time
        to read this docs string
        '''
        return sorted(set(list_links), key=self.get_num_in_link)

    @staticmethod
    def get_eval_string(html_source):
        '''
        get eval string from html source
        docs string just for PEP8
        '''
        regex_find_eval = r'eval.+'
        match_eval_string = re.search(regex_find_eval, html_source)
        if match_eval_string is not None:
            eval_string = match_eval_string.group()
        else:
            print('Can not find eval string')
            exit()
        return eval_string

    @staticmethod
    def decode_eval(eval_string):
        '''
        docs string for PEP8
        not for anything else
        '''
        decoded_eval_string = beautify(eval_string)
        return decoded_eval_string

    @staticmethod
    def get_link_by_regex(html_string):
        '''
        useless docs string
        dont' read
        '''
        regex_find_link = r'http:\/\/.+"'
        list_links = map(lambda x: x.rstrip('"'), re.findall(regex_find_link,
                                                             html_string))
        return list_links

    @staticmethod
    def get_num_in_link(link):
        '''
        I said
        do not read docs string
        you are wasting your time
        oh, god, you're still reading it

        '''
        # link = bla/bla/bla/file_name_num.file_extension
        file_name = link.split('/')[-1].split('.')[0]
        num_string = ''
        # file_name_num[::-1] -> num_name_file
        for letter in file_name[::-1]:
            if letter.isdigit():
                num_string += letter
            else:
                break
        # check whether got num file or not
        if num_string != '':
            # 'abc' -> 'cba' to got num_string, after that, int('abc')
            return int(num_string[::-1])
        return 1
