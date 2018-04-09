from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CJKhyperradicals',
    version='1.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests', 'dev']),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask', 'jieba', 'wordfreq', 'regex', 'requests'],
    extras_require={
        'dev': ['bs4'],
        'japanese': ['MeCab'],
        'test': ['pytest'],
    },
    package_data={
        'CJKhyperradicals': ['database', 'static', 'templates'],
    },
)