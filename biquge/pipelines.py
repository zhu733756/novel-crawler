import re
import os
import json
from datetime import datetime
from scrapy.utils.project import get_project_settings
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import hashlib
from scrapy.utils.python import to_bytes

from biquge.connection import get_dbpool, redis_db, get_pymysql_connect
from biquge.items import *
from biquge.public import format_time
from scrapy.exceptions import DropItem

settings = get_project_settings()


class SaveImagePipeline(ImagesPipeline):
    """保存图片"""

    def get_media_requests(self, item, spider):
        if item.get('cover'):
            return [Request(item['cover'], meta={'name': spider.spider.name})]

    def item_completed(self, results, item, spider):
        local_image_list = []
        for rs in results:
            local_image_list.append('')
            if rs[0]:
                if item.get('cover'):
                    item['cover'] = rs[1]['path']
        return item

    def file_path(self, request, response=None, info=None):
        """定义文件路径"""
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest() + '.jpg'
        return os.path.join(datetime.now().strftime('%Y-%m'),
                            datetime.now().strftime('%Y%m%d'),
                            request.meta['name'],
                            image_guid)



class HandleDataPipeline(object):
    """数据清洗管道"""
    def process_item(self, item, spider):
        # 清洗，处理数据
        for k, v in item.items():
            if isinstance(v, int):
                item[k] = str(v).strip()
            elif isinstance(v, list):
                item[k] = '\n'.join(v).strip()
            elif v is None:
                item[k] = ''
            if isinstance(v, str):
                item[k] = v.strip()
        
        if isinstance(item,BookItem):
            # 统一赋值
            item['fetch_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
        # 根据类别单独处理
        if isinstance(item, ChapterItem):
            # 废弃提取有问题的 item
            if not item['chapter_name']:
                raise DropItem
            if not item['chapter_content']:
                raise DropItem
        # 移到到base里了
        # if isinstance(item, WebarticleItem):
        #     if item['publish_date']:
        #         item['publish_date'] = format_time(item['publish_date'])
        #     else:
        #         item['publish_date'] = ''
        return item

class SaveDataPipeline(object):
    """保存数据到数据库"""

    def __init__(self):
        self.dbpool = get_dbpool()
        self.fetch_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.save_item, item)
        return item

    def save_item(self, cur, item):
        if isinstance(item, BookItem):
            table = 'novel_book'
        elif isinstance(item, ChapterItem):
            table = 'novel_chapter'
        try:
            key_list = list(item.fields.keys())
            sql = 'insert into {table} (`{key}`) values ({value}) on DUPLICATE key update {update}'.format(
                table=table,
                key='`, `'.join(key_list),
                value=', '.join(['%s'] * len(key_list)),
                update=', '.join(
                    ['`{}`=%s'.format(i) for i in key_list if i != 'fetch_date'])
            )
            value = [item.get(key, '') for key in key_list] + \
                    [item.get(key, '') for key in key_list if key != 'fetch_date']
            cur.execute(sql, value)
        except Exception as e:
            print('mysql报错信息\n{} 的 {} 表出现问题\n问题URL为：{}\n报错信息为：{}\n'.format(
                item.get('web_name', '未能找到网站名'), table, item.get('url', '未能找到url'), e))
