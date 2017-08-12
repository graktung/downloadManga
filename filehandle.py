'''
- zipfile to zip ifles
- os to remove files after zip
- copy to copy file
- requests to download file
'''
import zipfile
import os
import shutil
import sys
import requests


class FileHandle:
    '''
    ah, now need to talk
    class name describes exactly
    what it does
    so, why are you reading this docs string?
    OMGGGGGGGGGGGG
    '''

    @staticmethod
    def zip_files(files, file_name):
        '''
        zip files
        '''
        zipf = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            zipf.write(file)
        zipf.close()
        return file_name

    @staticmethod
    def delete_files(files):
        '''
        delete files
        '''
        for file in files:
            os.remove(file)

    @staticmethod
    def download_file(url, file_name):
        '''
        download file
        return file_name
        '''
        req = requests.get(url, stream=True)
        with open(file_name, 'wb') as written_file:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    written_file.write(chunk)
        return file_name

    @staticmethod
    def make_html_file(formatting_data, files):
        '''
        this function
        makes an html file
        for reading
        formatting_data[0] is chap_name
        formatting_data[1] is favicon name
        formatting_data[2] is backgroud name
        '''
        file_name = '-'.join(formatting_data[0].split()) + '.html'
        html_file = open(file_name, 'w')
        # get head html
        with open(sys.path[0].replace('\\', '/') + '/html_maker/head.txt')\
        as head_html_file:
            head_html = head_html_file.read().rstrip()
        # get tail html
        with open(sys.path[0].replace('\\', '/') + '/html_maker/tail.txt')\
        as tail_html_file:
            tail_html = tail_html_file.read().rstrip()
        html_file.write(head_html.format(chap_name=formatting_data[0],
                                         icon_name=formatting_data[1],
                                         background_name=formatting_data[2]))
        html_file.write('<h1 id="title">{chap_name}</h1>'
                        .format(chap_name=formatting_data[0]))
        for file in files:
            html_file.write('<img src="{file}">'.format(file=file))
        html_file.write(tail_html)
        html_file.close()
        return file_name

    @staticmethod
    def make_dir(dir_name):
        '''
        make directory to store files
        '''
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    @staticmethod
    def copy_file(from_, to_):
        '''
        copy a file from from_ to to_
        '''
        shutil.copy(from_, to_)

    @staticmethod
    def get_current_directory():
        '''
        get current directory
        that's all
        '''
        return os.getcwd().replace('\\', '/')
