# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):

    #网站名称
    site_name = scrapy.Field()
    # 小说名字
    book_name = scrapy.Field()
    # 小说作者
    author = scrapy.Field()
    # 小说url
    url = scrapy.Field()
    # 小说简介
    description = scrapy.Field()
    book_type = scrapy.Field()
    cover = scrapy.Field()
    book_id = scrapy.Field()
    last_update_time = scrapy.Field()
    fetch_date = scrapy.Field()

class ChapterItem(scrapy.Item):

    book_id = scrapy.Field()

    chapter_content = scrapy.Field()

    chapter_name = scrapy.Field()

    chapter_url = scrapy.Field()



