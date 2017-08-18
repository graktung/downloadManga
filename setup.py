from setuptools import setup, find_packages
from os import path

setup(
    name='Download Manga',
    version='1.0.0',
    description='Download Manga Package',
    url='https://github.com/graktung/downloadManga',
    author='Idea: drgnz, baivong. Coded: Nguyen Thanh Trung',
    author_email='https://twitter.com/thanhtrung2314',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: MangaFan',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='download manga',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    py_modules=["my_module"],
    install_requires=['bs4', 'jsbeautifier', 'requests'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)