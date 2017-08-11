'''
SUPPORT
- http://blogtruyen.com/
- http://truyentranhtuan.com/
- http://www.mangapanda.com/
- http://hentaivn.net/
- http://manganel.com/
- http://truyentranh8.net/
'''
import threading
import importlib
from time import sleep
from os import system, mkdir

SUPPORT_WEBSITES_DOWNLOAD = [
    {'domain': 'http://blogtruyen.com/',
     'module': 'blogtruyen', 'class': 'BlogTruyen'},
    {'domain': 'http://truyentranhtuan.com/',
     'module': 'truyentranhtuan', 'class': 'TruyenTranhTuan'},
    {'domain': 'http://www.mangapanda.com/',
     'module': 'mangapanda', 'class': 'MangaPanda'},
    {'domain': 'http://hentaivn.net/', 'module': 'hentaivn', 'class': 'HentaiVN'},
    {'domain': 'http://manganel.com/', 'module': 'manganel', 'class': 'Manganel'},
    {'domain': 'http://truyentranh8.net/',
     'module': 'truyentranhtam', 'class': 'TruyenTranhTam'}
]

SUPPORT_WEBSITES_SEARCH = [
    {'domain': 'http://manganel.com/', 'module': 'manganel', 'class': 'Manganel'},
    {'domain': 'http://truyentranh8.net/',
     'module': 'truyentranhtam', 'class': 'TruyenTranhTam'}
]


class Main:
    '''
    I am not used to writing docs string
    so this what I wrote
    sorry for its uselessness
    '''

    def main(self):
        '''
        main method
        MAIN METHOD
        main METHOD
        MAIN method
        Main Method
        '''
        while 1:
            command = self.read_command()
            self.decide(command)

    def decide(self, command):
        '''
        If you want more detailed information
        visit here: https://github.com/graktung/downloadManga
        check README.md out
        '''
        if command in ('load', 'download', 'down'):
            link = input('Link: ')
            # go to check the link download
            self.handle_link_download(link)
        elif command in ('load only', 'laod only'):
            link = input('Link: ')
            self.load_only(link)
        elif command in ('search', 'serch', 'sarch'):
            key = input('Keyword: ')
            self.handle_search(key)
        elif command in ('cls', 'clear', 'cear'):
            system('cls')
        elif command in ('quit', 'q', 'exit'):
            exit()

    def handle_link_download(self, link):
        '''
        pick suitable module and class for downloading
        '''
        for site in SUPPORT_WEBSITES_DOWNLOAD:
            if site['domain'] in link:
                module = importlib.import_module(site['module'])
                class_ = getattr(module, site['class'])
                object_of_class = class_()
                self.get_and_down(object_of_class, link)
                break

    def get_and_down(self, object_of_class, link):
        '''
        get data by get_data method
        and download chapters if want to down
        '''
        data_list_chapters = object_of_class.get_data(link)
        down_or_not = input('Download (y/n)? ').lower().strip()
        if down_or_not in ('y', 'yes'):
            num_of_desire_chap = input('How many? ')
            if not num_of_desire_chap.isdigit() or\
            num_of_desire_chap.lower().strip() == ('all'):
                num_of_desire_chap = len(data_list_chapters)
            else:
                num_of_desire_chap = int(num_of_desire_chap)
            # this is hard code
            # :D
            # if you don't understand it but want to understand
            # contact me
            # Twitter: https://twitter.com/thanhtrung2314
            for i in range(0, num_of_desire_chap, self.threading_num):
                for small_data in data_list_chapters[i: i + self.threading_num\
                if i + self.threading_num < num_of_desire_chap
                                                     else num_of_desire_chap]:
                    threading.Thread(target=object_of_class.download_image,
                                     args=(small_data,)).start()
                # if there's not only main thread
                while threading.active_count() != 1:
                    sleep(0.0001)
        # notification done
        print('\a')

    @staticmethod
    def read_command():
        '''
        read input from keyboard
        drop all space from left and right of input string
        '''
        command = ''
        while command == '':
            command = input('=]] ').lower().strip()
        return command

    @staticmethod
    def handle_search(keyword):
        '''
        search by given keyword
        maximum searched results each site
        given in run-time
        '''
        maximum_results = input('How many results do you want to display? ')
        if maximum_results.isdigit():
            maximum_results = int(maximum_results)
            # invalid maximum results
            if maximum_results < 1 or maximum_results > 10:
                maximum_results = 3
        else:
            maximum_results = 3
        searched_data = []
        # pick suitable module
        for site in SUPPORT_WEBSITES_SEARCH:
            module = importlib.import_module(site['module'])
            class_ = getattr(module, site['class'])
            object_of_class = class_()
            searched_data.append(object_of_class.search(
                keyword)[:maximum_results])
        # equal 1, because first element is hostname
        # if it's empty, it should have length is one
        is_searched_data_empty = len(searched_data) == 1
        if is_searched_data_empty:
            print('No results found from keyword %r' % keyword)
            return None
        # each item in searched_data contains results from one web
        # each item in small_data contains information about one chap
        # let's mini_date hold each item in small_data
        for small_data in searched_data:
            print('Enter to continue, Ctrl + C to stop')
            try:
                # drop first element: hostname
                print('=' * 50, '\n')
                print('Web:' + small_data[0] + '\n')
                for mini_data in small_data[1:]:
                    print('-' * 50)
                    print('Name:', mini_data[0]['name'], '\nLatest:',
                          mini_data[1]['name'])
                    print('+' * 50)
                    print('Chap:       ', mini_data[0]['link'])
                    print('Latest chap:', mini_data[1]['link'])
                    try:
                        input()
                    except KeyboardInterrupt:
                        print()
                        break
                input()
            except KeyboardInterrupt:
                print()
                break

    @staticmethod
    def load_only(link):
        '''
        download only a specific chap
        not anything else :3
        '''
        for site in SUPPORT_WEBSITES_DOWNLOAD:
            if site['domain'] in link:
                module = importlib.import_module(site['module'])
                class_ = getattr(module, site['class'])
                object_of_class = class_()
                object_of_class.download_image({'name': 'Tac gia khong biet ten',
                                                'link': link})
                break
        print('\a')

    @property
    def threading_num(self):
        '''
        get the number of threading
        config in database/configthreading.txt'
        maximum threading is 10
        minimum threading is 1
        '''
        try:
            with open('database/configthreading.txt') as read_file:
                str_num_of_threads = read_file.read().strip()
            # check valid num of threading
            if str_num_of_threads.isdigit():
                num_of_threads = int(str_num_of_threads) if 1 <=\
                    int(str_num_of_threads) <= 10 else 3
            else:
                num_of_threads = 1
        # if file does not exist
        except FileNotFoundError:
            # make file to next read
            try:
                with open('database/configthreading.txt', 'w') as written_file:
                    written_file.write('1')
            # if folder does not exist
            except FileNotFoundError:
                mkdir('database')
                with open('database/configthreading.txt', 'w') as written_file:
                    written_file.write('1')
            num_of_threads = 1
        return num_of_threads

if __name__ == '__main__':
    Main().main()
