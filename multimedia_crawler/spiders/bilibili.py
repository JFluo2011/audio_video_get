# coding: utf-8

import re
import os
import time
import copy
import json
import xmltodict

import scrapy
from scrapy.conf import settings

from multimedia_crawler.items import MultimediaCrawlerItem

from multimedia_crawler.common.common import WebUser, get_md5
from multimedia_crawler.common.bilibili_common import BiLiBiLiCommon


class BiLiBiLiSpider(scrapy.Spider):
    name = 'bilibili'
    download_delay = 5
    base_url = 'https://space.bilibili.com/{}#!/video'
    users = [
        # WebUser(id='31964921', name='繁花社长', storage_name='fanhuashezhang'),
        WebUser(id='47683654', name='wsceng', storage_name='wsceng'),
        # WebUser(id='883968', name='暴走漫画', storage_name='baozoumanhua'),
        # WebUser(id='4568410', name='ImbaTV官方', storage_name='imba_tv'),
        # WebUser(id='19591909', name='二更视频', storage_name='ergeng'),
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'multimedia_crawler.pipelines.MultimediaCrawlerPipeline': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'multimedia_crawler.middlewares.RotateUserAgentMiddleware': 400,
            'multimedia_crawler.middlewares.MultimediaCrawlerDupFilterMiddleware': 1,
        },
    }

    def start_requests(self):
        url = 'https://space.bilibili.com/ajax/member/getNavNum'
        for user in self.users:
            params = {
                'mid': user.id,
            }
            yield scrapy.FormRequest(url=url, method='GET', formdata=params, meta={'user': user})

    def parse(self, response):
        page_size = 30
        user = response.meta['user']
        url = 'https://space.bilibili.com/ajax/member/getSubmitVideos'
        json_data = json.loads(response.body)
        total = json_data['data']['video']
        pages = total // page_size if not (total % page_size) else (total // page_size + 1)
        for page in range(1, pages + 1):
            params = {
                'mid': user.id,
                'pagesize': str(page_size),
                'tid': '0',
                'page': str(page),
                'keyword': '',
                'order': 'pubdate',
            }
            yield scrapy.FormRequest(url=url, method='GET', meta={'user': user},
                                     formdata=params, callback=self.parse_items)

    def parse_items(self, response):
        user = response.meta['user']
        json_data = json.loads(response.body)
        base_url = 'https://www.bilibili.com/video/av{}/'
        # base_url = 'http://api.bilibili.com/view'
        for data in json_data['data']['vlist']:
            item = MultimediaCrawlerItem()
            item['host'] = 'bilibili'
            item['media_type'] = 'video'
            item['stack'] = []
            item['download'] = 0
            item['extract'] = 0
            item['file_dir'] = os.path.join(settings['FILES_STORE'], item['media_type'], self.name, user.storage_name)
            item['url'] = base_url.format(data['aid'])
            item['file_name'] = get_md5(item['url'])
            item['info'] = {
                'link': item['url'],
                'title': data.get('title', ''),
                'intro': data.get('description', ''),
                'author': user.name,
                'play_count': data.get('play', 0),
                'comments_count': data.get('comment', 0),
                'date': (time.strftime('%Y-%m-%d', time.localtime(data.get('created', 0)))
                         if data.get('created', 0) != 0 else ''),
            }
            meta = {
                # 'aid': data['aid'],
                'item_base': item,
            }
            yield scrapy.Request(url=item['url'], meta=meta, callback=self.parse_videos)

    def parse_videos(self, response):
        item_base = response.meta['item_base']
        sels = response.xpath(r'//div[@id="plist"]//option')
        url = 'https://interface.bilibili.com/playurl'
        bilibili_common = BiLiBiLiCommon()
        item_base['file_dir'] += '\\' + item_base['info']['title']
        if sels:
            for sel in sels:
                item = copy.deepcopy(item_base)
                cid = sel.xpath('@cid').extract()[0]
                item['url'] = item['info']['link'] = 'https://www.bilibili.com{}'.format(
                    sel.xpath('@value').extract()[0])
                item['file_name'] = sel.xpath(r'text()').extract()[0]
                params = bilibili_common.get_params(cid)
                yield scrapy.FormRequest(url=url, method='GET', meta={'item': item},
                                         formdata=params, callback=self.parse_video_urls)
        else:
            item = copy.deepcopy(item_base)
            cid = re.search(r'cid\s*=\s*(\d+)[\'\"&]', response.body).group(1)
            item['file_name'] = response.xpath(r'//meta[@property="media:title"]/@content').extract()[0]
            params = bilibili_common.get_params(cid)
            yield scrapy.FormRequest(url=url, method='GET', meta={'item': item},
                                     formdata=params, callback=self.parse_video_urls)

    def parse_video_urls(self, response):
        item = response.meta['item']
        try:
            json_data = json.loads(json.dumps(xmltodict.parse(response.body)))
        except Exception as err:
            self.logger.error('url: {}, error: {}'.format(item['url'], str(err)))
            return
        try:
            if isinstance(json_data['video']['durl'], list):
                item['media_urls'] = [data['url'] for data in json_data['video']['durl']]
            else:
                item['media_urls'] = [json_data['video']['durl']['url']]
            # item['media_urls'] = [json_data['video']['durl']['url']]
        except Exception as err:
            self.logger.error('url: {}, error: {}'.format(item['url'], str(err)))
            return
        else:
            if not item['media_urls']:
                self.logger.error('url: {}, error: did not get any URL in the json data'.format(item['url']))
                return

        item['file_name'] += '.' + item['media_urls'][0].split('?')[0].split('.')[-1]

        yield item

