'''
- zipfile to zip ifles
- os to remove files after zip
- requests to download file
'''
import zipfile
import os
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
    def zip_file(files, file_name):
        '''
        zip file
        and delete it
        '''
        zipf = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            zipf.write(file)
            os.remove(file)
        zipf.close()

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
