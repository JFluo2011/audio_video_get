# -*- coding: utf-8 -*-
import re
import os
import time
import json

import scrapy
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from multimedia_crawler.items import MultimediaCrawlerItem
from multimedia_crawler.common.common import get_md5


# class YouKuJiKeSpider(CrawlSpider):
class YouKuJiKeSpider(scrapy.Spider):
    name = "youku_jike"
    download_delay = 2
    # allowed_domains = ["youku.com"]
    # start_urls = ['http://i.youku.com/u/UMzE4MTU1MDEwMA==/videos']
    start_urls = [
        'http://v.youku.com/v_show/id_XMTYzNzc2Mzk1Ng==.html',
        'http://v.youku.com/v_show/id_XMTgxNzY4OTg1Mg==.html',
        'http://v.youku.com/v_show/id_XMTUyODE3MDMxNg==.html',
        'http://v.youku.com/v_show/id_XMTU0MzE3MjU3Ng==.html',
        'http://v.youku.com/v_show/id_XMTU0NzgyMDg4NA==.html',
        'http://v.youku.com/v_show/id_XMTU1MTIwMjgyNA==.html',
        'http://v.youku.com/v_show/id_XMTU2OTczMzMzMg==.html',
        'http://v.youku.com/v_show/id_XMTYyOTQ4MDk2NA==.html',
        'http://v.youku.com/v_show/id_XMTY0MTg4NjE3Mg==.html',
    ]

    # rules = (
    #     Rule(
    #         LinkExtractor(allow=('/i/UMzE4MTU1MDEwMA==/videos\?order=1&', )),
    #         callback='parse_pages',
    #         follow=True,
    #     ),
    # )

    custom_settings = {
        'ITEM_PIPELINES': {
            'multimedia_crawler.pipelines.MultimediaCrawlerPipeline': 100,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'multimedia_crawler.middlewares.RotateUserAgentMiddleware': 400,
            'multimedia_crawler.middlewares.YouKuJiKeDupFilterMiddleware': 1,
        },
    }

    def parse(self, response):
        item = MultimediaCrawlerItem()
        item['host'] = 'youku_jike'
        item['media_type'] = 'video'
        item['stack'] = []
        item['download'] = 0
        item['extract'] = 0
        item['file_dir'] = os.path.join(settings['FILES_STORE'], item['media_type'], self.name)
        item['url'] = response.url
        item['file_name'] = get_md5(item['url'])
        item['info'] = ''
        vid = re.search(r'id_(.*?).html|$', response.url).group(1)
        if vid is None:
            self.logger.error('url: {}, error: failed to find vid'.format(response.url))
            return
        params = {
            'vid': vid,
            'ccode': '0401',
            'client_ip': '192.168.1.1',
            'utid': 'tB2PEWHIKgECAbaWLjUeiFyE',
            'client_ts': str(round(time.time())),
        }
        url = 'https://ups.youku.com/ups/get.json'
        yield scrapy.FormRequest(url, method='GET', meta={'item': item}, formdata=params,
                                 callback=self.parse_download_url)

    # def parse_pages(self, response):
    #     sel_video_list = response.xpath('//div[@class="v va"]')
    #     for sel in sel_video_list:
    #         item = MultimediaCrawlerItem()
    #         item['host'] = 'youku_jike'
    #         item['media_type'] = 'video'
    #         item['stack'] = []
    #         item['download'] = 0
    #         item['extract'] = 0
    #         item['file_dir'] = os.path.join(settings['FILES_STORE'], item['media_type'], self.name)
    #         item['url'] = 'http:' + sel.xpath('div[@class="v-link"]/a/@href').extract()[0]
    #         item['file_name'] = get_md5(item['url'])
    #
    #         item['info'] = {
    #             'title': sel.xpath('.//div[@class="v-meta-title"]/a/@title').extract_first(default='').strip(),
    #             'link': item['url'],
    #             'date': sel.xpath('.//span[@class="v-publishtime"]/text()').extract_first(default=''),
    #             'author': 'UMzE4MTU1MDEwMA==',
    #             'play_count': sel.xpath('.//span[@class="v-num"]/text()').extract_first(default=''),
    #         }
    #         params = {
    #             'spm': (re.search(r'meta name="data-spm" content="(.*?)"', response.body).group(1) + '.' +
    #                     re.search(r'body class="yk-w970" data-spm="(\d+)"', response.body).group(1) + '.0.0')
    #         }
    #         yield scrapy.FormRequest(url=item['url'], method='GET', meta={'item': item}, formdata=params,
    #                                  callback=self.parse_video_url)

    def parse_video_url(self, response):
        item = response.meta['item']
        vid = re.search(r'id_(.*?).html|$', response.url).group(1)
        if vid is None:
            self.logger.error('url: {}, error: failed to find vid'.format(response.url))
            return
        params = {
            'vid': vid,
            'ccode': '0401',
            'client_ip': '192.168.1.1',
            'utid': 'tB2PEWHIKgECAbaWLjUeiFyE',
            'client_ts': str(round(time.time())),
        }
        url = 'https://ups.youku.com/ups/get.json'
        yield scrapy.FormRequest(url, method='GET', meta={'item': item}, formdata=params,
                                 callback=self.parse_download_url)

    def parse_download_url(self, response):
        item = response.meta['item']
        json_data = json.loads(response.body)
        try:
            # r = re.findall(r'"cdn_url":"(.*?hd=0.*?)"', json_data)
            segs = json_data['data']['stream'][0]['segs']
            item['media_urls'] = [seg['cdn_url'] for seg in segs]
            item['file_name'] += '.' + re.findall(r'st/(.*?)/fileid', item['media_urls'][0])[0]
            return item
        except Exception, err:
            self.logger.error('url: {}, error: {}'.format(item['url'], str(err)))
            return None

