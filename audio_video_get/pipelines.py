# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import shutil
import logging

import scrapy
import requests
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from pymongo import MongoClient
from scrapy.conf import settings

from items import TouTiaoItem


class AudioVideoGetPipeline(object):
    def process_item(self, item, spider):
        return item


class ToutiaoPipeline(object):
    def __init__(self):
        self.client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = self.client.get_database(settings['MONGODB_DB'])
        self.col = self.db.get_collection(settings['MONGODB_COLLECTION'])
        self.col.ensure_index('unique_url', unique=True)

    def open_spider(self, spider):
        pass
        # self.col.remove({'download': -1})
        # print 'downloading: ', (self.col.find({'download': 'downloading'}))
        # self.col.remove({'download': 'downloading'})

    def process_item(self, item, spider):
        try:
            data = {
                'unique_url': item['unique_url'],
                'name': item['name'],
                'intro': item['intro'],
                'album': item['album'],
                'author': item['author'],
                'author_id': item['author_id'],
                'spider': spider.name,
                'download': 0,
                'file_name': '',
                'file_paths': '',
                'video_url': item['video_url'],
            }
            self.col.update({'unique_url': item['unique_url']}, data, upsert=True)
            # self.col.insert(data)
        except Exception, err:
            logging.error(str(err))
            raise DropItem(str(err))
        return item

    def close_spider(self, spider):
        pass
        # for r in self.col.find({'download': 'downloading'}):
        #     if os.path.exists(r['file_paths']):
        #         os.remove(r['file_paths'])
        # self.col.update({'download': 'downloading'}, {'$set': {'download': '0'}})
        # self.col.update({'download': -1}, {'$set': {'download': '0'}})


class YoukuPipeline(object):
    def __init__(self):
        self.client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = self.client.get_database(settings['MONGODB_DB'])
        self.col = self.db.get_collection(settings['MONGODB_COLLECTION'])
        self.col.ensure_index('url', unique=True)

    def process_item(self, item, spider):
        try:
            data = {
                'url': item['url'],
                'file': item['file'],
                'isVideo': item['isVideo'],
                'host': item['host'],
                'localDir': item['localDir'],
                'downloaded': item['downloaded'],
                'info': item['info'],
                'stack': item['stack'],
                'blocks': item['blocks'],
            }
            # self.col.update({'unique_url': item['unique_url']}, data, upsert=True)
            self.col.insert(data)
        except Exception, err:
            logging.error(str(err))
            raise DropItem(str(err))
        return item


class ToutiaoFilePipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super(ToutiaoFilePipeline, self).__init__(*args, **kwargs)
        self.client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = self.client.get_database(settings['MONGODB_DB'])
        self.col = self.db.get_collection(settings['MONGODB_COLLECTION'])
        self.item = TouTiaoItem()

    def get_media_requests(self, item, info):
        self.item = item
        for file_url in item['file_urls']:
            # self.col.update_one({'video_url': file_url}, {'$set': {'download': 'downloading'}})
            # self.col.update({'unique_url': item['unique_url']}, {'$set': {'download': 'downloading'}})
            yield scrapy.Request(file_url)

    def __move_file(self, file_path):
        base_path = os.path.join('Video', 'toutiao')
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        # os.sep
        src_path = os.path.join(os.path.abspath(settings['FILES_STORE']), file_path)
        dre_path = os.path.join(os.path.abspath(settings['FILES_STORE']),
                                base_path, self.item['author_id'], file_path.split(os.sep, 1)[1])
        if not os.path.exists(os.path.split(dre_path)[0]):
            os.makedirs(os.path.split(dre_path)[0])
        print src_path, dre_path
        shutil.move(src_path, dre_path)
        return dre_path

    def item_completed(self, results, item, info):
        file_paths = [x['path'].replace('/', os.sep) for ok, x in results if ok]
        if not file_paths:
            self.col.update({'unique_url': item['unique_url']}, {'$set': {'download': -1}})
            raise DropItem("Item contains no files")
        # item['file_paths'] = self.__move_file(file_paths[0])
        item['file_paths'] = ''
        item['file_name'] = os.path.split(file_paths[0])[0]
        self.col.update({'unique_url': item['unique_url']},
                        {'$set': {
                            'download': 1,
                            'file_name': item['file_name'],
                            # 'file_paths': item['file_paths']
                        }})
        return item

    # def file_path(self, request, response=None, info=None):
    #     # file_name = request.url.split('/')[-1]
    #     file_name = os.path.join(self.item['author_id'], self.item['file_name'])
    #     path = info.spider.name
    #     # self.path_list.append(os.path.join(path, file_name))
    #     logging.error(os.path.join(path, file_name))
    #     return os.path.join(path, file_name)
    #     # return '{path}/{file_name}'.format(path=path, file_name=file_name)


class YoukuFilePipeline(FilesPipeline):
    def __init__(self, *args, **kwargs):
        super(YoukuFilePipeline, self).__init__(*args, **kwargs)
        self.client = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.db = self.client.get_database(settings['MONGODB_DB'])
        self.col = self.db.get_collection(settings['MONGODB_COLLECTION'])
        self.item = TouTiaoItem()

    def _handle_redirect(self, file_url):
        response = requests.head(file_url)
        if response.status_code == 302:
            file_url = response.headers["Location"]
        return file_url

    def get_media_requests(self, item, info):
        self.item = item
        for file_url in item['file_urls']:
            redirect_url = self._handle_redirect(file_url)
            yield scrapy.Request(redirect_url)

    def item_completed(self, results, item, info):
        file_paths = [x['path'].replace('/', os.sep) for ok, x in results if ok]
        if not file_paths:
            self.col.update({'unique_url': item['unique_url']}, {'$set': {'download': -1}})
            raise DropItem("Item contains no files")
        item['file_paths'] = ''
        item['file_name'] = os.path.split(file_paths[0])[0]
        self.col.update({'unique_url': item['unique_url']},
                        {'$set': {
                            'download': 1,
                            'file_name': item['file_name'],
                        }})
        return item
