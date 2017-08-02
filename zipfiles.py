import zipfile
import os

def zipFile(filename, files):
	zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
	for file in files:
		zipf.write(file)
		os.remove(file)	
	zipf.close()