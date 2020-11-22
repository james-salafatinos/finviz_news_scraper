#When package installed, this will run.

from setuptools import setup

setup(name='finviz_news_scraper',
      version='0.0.1',
      description='Finviz news scraper',
      author='James Salafatinos',
      author_email='jamessalafatinos@outlook.com',
      url='<>', #Github link
      packages=['finviz_scraper'],
      entry_points = {
          'console_scripts': [
              'finviz_scrape=finviz_scraper.__main__:main'
          ]
      } #defines main files
     )



