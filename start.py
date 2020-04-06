import  os 

os.chdir(os.path.dirname(__file__))

from scrapy.cmdline import execute
execute('scrapy crawl xbiquge -a update_books=False -a book_name=牧神记'.split())