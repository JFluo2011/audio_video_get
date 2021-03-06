# -*- coding: utf-8 -*-

import re
import time
import json

import scrapy

from base_player import BasePlayer
from multimedia_crawler.common.common import get_md5


class YouKuPlayer(BasePlayer):
    name = 'youku_player'

    def __init__(self, logger, page_url, *args, **kwargs):
        super(YouKuPlayer, self).__init__(logger, page_url, *args, **kwargs)
        self.url = self.kwargs['player_url']
        self.method = 'GET'
        self.params = {}
        self.video_id = ''
        self.type = {
            'flvhd': '.flv',
            '3gphd': '.mp4',
            'mp4hd': '.mp4',
            'mp4hd2': '.flv',
            'mp4hd3': '.flv',
        }

    def parse_video(self, response):
        item = response.meta['item']
        url = 'https://api.youku.com/players/custom.json'
        self.video_id = self.url.split('/')[-1]
        params = {
            'refer': self.url,
            'client_id': re.findall(r'\.client_id\s*=\s*"(.*?)"', response.body)[0],
            'video_id': self.video_id,
            'version': '1.0',
            'type': 'h5',
            'embsig': '',
            'callback': 'json' + str(int(time.time() * 1000)),
        }
        yield scrapy.FormRequest(url=url, method='GET', meta={'item': item},
                                 formdata=params, callback=self.parse_video_custom)

    def parse_video_custom(self, response):
        item = response.meta['item']
        json_data = json.loads(response.body[response.body.find('{'): response.body.rfind('}') + 1])
        vid = self.url.split('/')[-1]
        url = 'https://ups.youku.com/ups/get.json'
        params = {
            'vid': vid,
            'ccode': '0590',
            'client_ip': '0.0.0.0',
            'client_ts': str(int(time.time())),
            'utid': 'aKCuEcCdq38CAbaWLjWeW3TI',
            'r': json_data['stealsign'],
            'callback': 'json' + str(int(time.time() * 1000)),
        }
        yield scrapy.FormRequest(url=url, method='GET', meta={'item': item},
                                 formdata=params, callback=self.parse_video_urls)

    def parse_video_urls(self, response):
        item = response.meta['item']
        try:
            json_data = json.loads(response.body[response.body.find('{'): response.body.rfind('}') + 1])
            code = json_data['e']['code']
        except Exception as err:
            self.logger.error('url: {}, error: {}'.format(self.page_url, str(err)))
            return
        else:
            if code != 0:
                self.logger.error('url: {}, code: {}'.format(self.page_url, str(code)))
                return

        try:
            if item['info'].get('play_count', 0) == 0:
                item['info']['play_count'] = json_data['data']['video']['videoid_play']
            if item['info'].get('author', '') == '':
                item['info']['author'] = json_data['data']['video']['username']
        except:
            pass

        try:
            item['media_urls'] = [data['cdn_url'] for data in json_data['data']['stream'][0]['segs']]
            item['file_name'] = (get_md5(self.page_url)
                                 + self.type.get(json_data['data']['stream'][0]['stream_type'], '.mp4'))
            # fileid = json_data['data']['stream'][0]['segs'][0]['fileid']
            # item['file_name'] = get_md5(item['url']) + re.findall(r'{}(.*?)\?'.format(fileid),
            #                                                         item['media_urls'][0])[0]
        except Exception as err:
            self.logger.error('url: {}, error: {}'.format(self.page_url, str(err)))
            return
        else:
            if not item['media_urls']:
                self.logger.error('url: {}, error: did not get any URL in the json data'.format(self.page_url))
                return
        return item

        # url = 'http://v.youku.com/v_show/id_{}.html'.format(self.video_id)
        # yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_vid)

        # def parse_vid(self, response):
        #     item = response.meta['item']
        #     vid = re.findall(r'videoId:"(\d+)"', response.body)[0]
        #     url = ('http://v.youku.com/action/getVideoPlayInfo?beta&timestamp={}&vid={}&showid=290031&'
        #            'param[]=share&param[]=favo&param[]=download&param[]=phonewatch&'
        #            'param[]=updown&callback=tuijsonp5').format(str(int(time.time()*1000)), vid)
        #
        #     yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_play_counts)
        #
        # def parse_play_counts(self, response):
        #     item = response.meta['item']
        #     try:
        #         json_data = json.loads(response.body[response.body.find('{'): response.body.rfind('}') + 1])
        #         item['info']['play_count'] = json_data['data']['stat']['vv']
        #     except:
        #         pass
        #
        #     return item
