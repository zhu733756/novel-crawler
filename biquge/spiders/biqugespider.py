import scrapy
from ..items import *
from ..connection import get_pymysql_connect
import pymysql
from ..public import format_time
import re
import uuid
from datetime import  datetime

class QuSpider(scrapy.Spider):
    name = 'xbiquge'
    allowed_domains = ['xbiquge.la']
    start_urls = ['http://www.xbiquge.la/xiaoshuodaquan/']

    def __init__(self, *a, **kwargs):
        super(QuSpider, self).__init__(*a, **kwargs)
        self.update_books_flag = kwargs.get("update_books",True)
        self.update_links = kwargs.get("update_links",[])
        self.crawl_book_name = kwargs.get("book_name",None)

    def parse(self, response):
        if self.crawl_book_name:
            raw_urls = response.xpath(f"//div[@id='main']//ul//a[contains(text(),\'{self.crawl_book_name}\')]/@href").extract()
        else:
            raw_urls = response.xpath("//div[@id='main']//ul//a/@href").extract()
        urls=[response.urljoin(url) for url in raw_urls]
        if len(urls) == 0:
            print("无法匹配到小说链接！")
            return
        uncrawled_book_urls = set(urls) if self.update_books_flag else self.check_to_crawl(urls)
        for url in uncrawled_book_urls:
            yield scrapy.Request(url=url, callback=self.parse_description)

    def check_to_crawl(self,urls):
        conn = get_pymysql_connect()
        cusor = conn.cursor()
        sql = "select url from novel_book"
        try:
            res = cusor.execute(sql)
            if res:
                full_crawl_urls = set(r["url"] for r in cusor.fetchall())
                return set(urls)-set(full_crawl_urls)-set(self.update_links)
            return set(urls)- set(self.update_links)
        except Exception as e:
            print(e.args)
            conn.rollback()
            return set(urls)- set(self.update_links).dif
        finally:
            conn.close()

    def parse_description(self, response):
        # item = BiItem()
        two_detail = response.xpath("//div[@id='wrapper']")
        for two in two_detail:
            # 获取小说名称
            item = BookItem()
            item["url"]=response.url
            item["site_name"] = self.name
            item["book_name"] = two.xpath(".//div[@class='box_con']//div[@id='info']/h1/text()").extract_first('')
            # 获取小说作者
            item["author"] = re.sub("[作\s者：:]+","",two.xpath(".//div[@class='box_con']//div[@id='info']/p/text()").extract_first(''))
            # 获取小说类型
            item["book_id"] = str(uuid.uuid1())
            item["book_type"] = two.xpath(".//div[@class='con_top']/a[2]/text()").extract_first('')
            # print(type)
            # 获取小说简介
            item["description"] = re.sub("\s+","",two.xpath(".//div[@id='intro']/p[2]/text()").extract_first(''))
            # print(intro)
            # 获取小说封面
            item["cover"] = two.xpath(".//div[@id='sidebar']/div[@id='fmimg']/img/@src").extract_first('')
            # print(image)
            # 获取小说最后更新时间
            item["last_update_time"] = format_time("".join(two.xpath(".//div[@id='info']/p[3]/text()").re('(\d.*\d)'))) or datetime.now()
            yield item
            # 获取小说章节目录url
            section_urls = two.xpath(".//div[@class='box_con']//dl//a/@href").extract()
            for section in section_urls:
                yield scrapy.Request(url=response.urljoin(section), callback=self.parse_detail,meta={"uuid":item["book_id"]})

    def parse_detail(self, response):
        item = ChapterItem()
        # 获取每一章节目录名称
        section_title = response.xpath("//div[@class='box_con']/div[@class='bookname']/h1/text()").extract_first('')
        
        item['chapter_name'] = section_title
        # 获取每一章节的章节内容
        section_lists = response.xpath("//div[@class='box_con']/div[@id='content']/text()").extract()
        # 设置一个空的字符串进行数据拼接
        sections = []
        for section in section_lists:
            section = re.sub(r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——?【】？~@#￥%……&*]+|\\n+|\\r+|(\\xa0)+|(\\u3000)+|\\t", "", str(section))
            if section:
                sections.append(section)

        item['chapter_content'] = "\n".join(sections)
        item["chapter_url"] = response.url
        item["book_id"] = response.meta.get("uuid")

        yield item