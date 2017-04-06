import math
import time
import json
import hashlib
import re

import requests

from .spider import SpiderBase
from .data import WebsiteType, FileInfo


class TouTiao(SpiderBase):
    def __init__(self):
        self.name = 'ergengtv'
        self.websiteType = WebsiteType.Video
        self.__urlbase = "http://www.toutiao.com/"

    def get_params(self, t=None):
        params = {}
        if not t:
            t = math.floor(time.time() * 1000 / 1e3)
        i = hex(t)[2:].upper()  # "58DC72B1"
        m = hashlib.md5()  # "18435DC055C6F209E430B2D4BB46AA8B"
        m.update(str(t))
        e = m.hexdigest().upper()
        if 8 != len(i):
            return {'as': "479BB4B7254C150", 'cp': '7E0AC8874BB0985'}

        s = e[0:5]
        o = e[-5:]
        a = l = ''
        for n in range(0, 5):
            a += s[n] + i[n]
            l += i[n + 3] + o[n]
        return {'as': 'A1' + a + i[-3:], 'cp': i[0:3] + l + 'E1'}

    def get_start_links(self):
        params = self.get_params()
        user_ids = ['6975800262', '50590890693', '5857206714']
        base_url = ('http://www.toutiao.com/c/user/article/page_type=0&user_id={user_id}&max_behot_time=0&'
                    'count=20&as={AS}&cp={cp}')

        return [base_url.format(user_id=user_id, AS=params['as'], cp=params['cp']) for user_id in user_ids]

    def fetch_links(self, doc, workUnit):
        """
        {"login_status": false, "has_more": true, "next": {"max_behot_time": 1490753623}, "page_type": 0, "message": "success", "data": [{"image_url": "http://p3.pstatp.com/list/190x124/1af600047e712c8917c1", "single_mode": true, "abstract": "\u4e00\u65e6\u5230\u4e86\u66b4\u96e8\u8086\u8650\u7684\u5b63\u8282\uff0c\u8def\u9762\u5e38\u5e38\u662f\u53d8\u5f97\u4e00\u7247\u6c6a\u6d0b\u3002\u8981\u77e5\u9053\uff0c\u5f88\u591a\u57ce\u5e02\u7684\u6392\u6c34\u7cfb\u7edf\u666e\u904d\u52a3\u8d28\uff0c\u5c31\u7b97\u662f\u53ea\u662f\u4e0b\u573a\u5c0f\u96e8\u4e5f\u80fd\u9020\u6210\u8def\u9762\u79ef\u6c34\u3002\u4e0d\u8fc7\u60f3\u8981\u51cf\u7f13\u8fd9\u7c7b\u73b0\u8c61\uff0c\u7edd\u4e0d\u662f\u4e0d\u53ef\u80fd\uff0c\u56e0\u4e3a\u6709\u4eba\u5c31\u53d1\u660e\u51fa\u6765\u4e00\u6b3e\u8d85\u5f3a\u5438\u6c34\u7684\u6df7\u51dd\u571f\u6750\u6599\uff0c\u94fa\u6210\u9a6c\u8def\uff0c\u636e\u8bf41\u5206\u949f\u80fd\u5438\u6c344\u5428\u3002", "image_list": [], "more_mode": false, "tag": "news", "tag_url": "video", "title": "\u4f1a\u201c\u559d\u6c34\u201d\u7684\u9a6c\u8def\uff0c1\u5206\u949f\u5438\u6c344\u5428\uff0c\u600e\u4e48\u4e0b\u96e8\u90fd\u5e72\u71e5", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 608, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 428116, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 473864, "video_duration_str": "01:56", "source_url": "/item/6405465532706849282/", "item_id": "6405465532706849282", "article_genre": "video", "display_url": "http://toutiao.com/group/6405465532706849282/", "behot_time": 1491442768, "has_gallery": false, "group_id": "6405465532706849282"}, {"image_url": "http://p9.pstatp.com/list/190x124/1af9000354c56e075021", "single_mode": true, "abstract": "", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u5168\u7403\u552f\u4e00\u6446\u5f0f\u6865\uff0c\u6765\u8239\u5c31\u7ffb\uff0c\u53cd\u800c\u6210\u4e86\u6781\u9650\u8fd0\u52a8\u7684\u4e50\u56ed", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 100, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 61969, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 92249, "video_duration_str": "02:15", "source_url": "/item/6404345349128847873/", "item_id": "6404345349128847873", "article_genre": "video", "display_url": "http://toutiao.com/group/6405454287204548865/", "behot_time": 1491386675, "has_gallery": false, "group_id": "6405454287204548865"}, {"image_url": "http://p3.pstatp.com/list/190x124/1af00002bc368913fcb2", "single_mode": true, "abstract": "", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u81ea\u5df1\u8bbe\u8ba1\uff0c\u53ea\u89817\u4e071\u5929\u5efa\u6210\u522b\u5885\uff0c\u8282\u7ea670%\u7684\u6210\u672c", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 174, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 378578, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 549395, "video_duration_str": "01:54", "source_url": "/item/6405387014186729985/", "item_id": "6405387014186729985", "article_genre": "video", "display_url": "http://toutiao.com/group/6405387014186729985/", "behot_time": 1491371150, "has_gallery": false, "group_id": "6405387014186729985"}, {"image_url": "http://p3.pstatp.com/list/190x124/1af20001f29c7c2dceca", "single_mode": true, "abstract": "\u4fbf\u643a\u89c6\u529b\u68c0\u6d4b\u4eea", "image_list": [], "more_mode": false, "tag": "video_digital", "tag_url": "video", "title": "\u81ea\u5df1\u7528\u624b\u673a\u9a8c\u5149\uff0cAPP\u914d\u955c\uff0c\u50cf\u73a9\u6e38\u620f\u4e00\u6837\u7b80\u5355", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 6, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 2365, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 2368, "video_duration_str": "01:52", "source_url": "/item/6403974134719578625/", "item_id": "6403974134719578625", "article_genre": "video", "display_url": "http://toutiao.com/group/6403974134719578625/", "behot_time": 1491356907, "has_gallery": false, "group_id": "6403974134719578625"}, {"image_url": "http://p3.pstatp.com/list/190x124/1af60000b63562001749", "single_mode": true, "abstract": "\u94a2\u94c1\u4fa0\u4f5c\u4e3a\u6f2b\u5a01\u89d2\u8272\u4e2d\u6700\u53d7\u6b22\u8fce\u7684\u82f1\u96c4\uff0c\u5f88\u591a\u4eba\u90fd\u88ab\u5b83\u90a3\u8eab\u80fd\u4e0a\u5929\u5165\u5730\u7684\u88c5\u7532\u8ff7\u5f97\u4e0d\u8981\u4e0d\u8981\u7684\uff0c\u8fd9\u8ba9\u50cf\u8d85\u4eba\u4e00\u6837\u505a\u4e2a\u62ef\u6551\u4e16\u754c\u7684\u8d85\u7ea7\u82f1\u96c4\uff0c\u6210\u4e86\u65e0\u6570\u5c4c\u4e1d\u7684\u68a6\u60f3\u3002\u4e8e\u662f\u4e4e\uff0c\u4e2d\u6bd2\u8fc7\u6df1\u7684\u82f1\u56fd\u53d1\u660e\u5bb6\u5c31\u7814\u53d1\u4e86\u4e00\u5957\u4e2a\u4eba\u98de\u884c\u88c5\u7f6e\uff0c\u4e0d\u628a\u81ea\u5df1\u9001\u4e0a\u5929\u8a93\u4e0d\u7f62\u4f11\u3002", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u771f\u6b63\u94a2\u94c1\u4fa0\uff0c\u7ed1\u77406\u4e2a\u55b7\u6c14\u53d1\u52a8\u673a\uff0c\u5192\u9669\u8d77\u98de\uff0c\u592a\u60ca\u9669", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 106, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 13216, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 89907, "video_duration_str": "01:53", "source_url": "/item/6404649235047776770/", "item_id": "6404649235047776770", "article_genre": "video", "display_url": "http://toutiao.com/group/6404649235047776770/", "behot_time": 1491274813, "has_gallery": false, "group_id": "6404649235047776770"}, {"image_url": "http://p2.pstatp.com/list/190x124/1928000ef00f3cec9649", "single_mode": true, "abstract": "\u4e0d\u5c11\u4eba\u90fd\u77e5\u9053\u91d1\u5eb8\u5148\u751f\u7b14\u4e0b\u7684\u8f7b\u529f\u6c34\u4e0a\u6f02\uff0c\u8bf4\u7684\u6b63\u662f\u88d8\u5343\u4ede\u7684\u7edd\u6d3b\uff0c\u53ef\u662f\u6b66\u4fa0\u6bd5\u7adf\u662f\u6b66\u4fa0\uff0c\u4eba\u662f\u4e0d\u53ef\u80fd\u5728\u6c34\u9762\u4e0a\u5954\u8dd1\u5982\u98de\u7684\uff0c\u5c31\u8fde\u4e00\u822c\u7684\u98de\u673a\u4e5f\u96be\u4ee5\u5728\u6c34\u9762\u4f4e\u7a7a\u98de\u884c\u3002\u800c\u5c31\u5728\u4e0d\u4e45\u524d\uff0c\u4fc4\u7f57\u65af\u5c31\u5c55\u793a\u4e86\u4e00\u6b3e\u5168\u65b0\u7684\u8fd0\u8f93\u673agroundskimmer\uff0c\u5b83\u8d34\u4e8e\u6c34\u9762\u98de\u884c\uff0c\u5355\u7a0b\u8f7d\u8d27\u91cf\u7adf\u9ad8\u8fbe500\u5428\u3002", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u4ec0\u4e48\u98de\u884c\u5668\uff0c\u4e00\u6b21\u8fd0\u8f93500\u5428\uff0c\u6bd4\u8fd020\u591a7\u500d", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 157, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 776505, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 801763, "video_duration_str": "01:45", "source_url": "/item/6397666988067389953/", "item_id": "6397666988067389953", "article_genre": "video", "display_url": "http://toutiao.com/group/6397666988067389953/", "behot_time": 1491273555, "has_gallery": false, "group_id": "6397666988067389953"}, {"image_url": "http://p3.pstatp.com/list/190x124/1af30000862ef2341001", "single_mode": true, "abstract": "\u7ed3\u56db\u5341\u79cd\u679c\u5b50\u7684\u6811", "image_list": [], "more_mode": false, "tag": "news_agriculture", "tag_url": "video", "title": "\u7ed3\u6ee140\u79cd\u6c34\u679c\u7684\u6811\uff0c\u79cd10\u68f5\uff0c\u53ef\u4ee5\u5f00\u6c34\u679c\u8d85\u5e02", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 246, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 425054, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 522541, "video_duration_str": "01:51", "source_url": "/item/6404344408782668289/", "item_id": "6404344408782668289", "article_genre": "video", "display_url": "http://toutiao.com/group/6404344408782668289/", "behot_time": 1491272086, "has_gallery": false, "group_id": "6404344408782668289"}, {"image_url": "http://p1.pstatp.com/list/190x124/1af30000eb817450d356", "single_mode": true, "abstract": "\u5bf9\u4e8e\u5f88\u591a\u4eba\u6765\u8bf4\uff0c\u5728\u8def\u4e0a\u9a7e\u8f66\u662f\u4e2a\u8f7b\u677e\u6d3b\uff0c\u53ef\u662f\u4e00\u9047\u5230\u505c\u8f66\u8fd9\u79cd\u9700\u8981\u548c\u6280\u672f\u6cbe\u8fb9\u7684\u95ee\u9898\uff0c\u5c31\u4e0d\u884c\u4e86\u3002\u60f3\u8981\u8f7b\u8f7b\u677e\u677e\u5c31\u505c\u597d\u8f66\uff0c\u4e0d\u5982\u5c31\u8bd5\u8bd5\u6211\u4eec\u5927\u5929\u671d\u7684\u8fd9\u4e2a\u6cca\u8f66\u673a\u5668\u4eba\u5427\u3002", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u56fd\u4ea7\u6cca\u8f66\u673a\u5668\u4eba\uff0c2\u5206\u949f\u505c\u597d\uff0c\u589e\u52a0\u505c\u8f66\u4f4d40%", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 31, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 12989, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 14874, "video_duration_str": "01:46", "source_url": "/item/6404348166723863042/", "item_id": "6404348166723863042", "article_genre": "video", "display_url": "http://toutiao.com/group/6404348166723863042/", "behot_time": 1491192622, "has_gallery": false, "group_id": "6404348166723863042"}, {"image_url": "http://p3.pstatp.com/list/190x124/19fc0005bf5ed4d585f6", "single_mode": true, "abstract": "\u81ea\u4ece\u7535\u8111\u88ab\u53d1\u660e\u51fa\u6765\uff0c\u4eba\u8111\u548c\u7535\u8111\u95f4\u54ea\u4e2a\u66f4\u5f3a\u7684\u4e89\u8bba\u5c31\u6ca1\u6709\u505c\u6b62\u8fc7\uff0c\u4e0d\u8fc7\u5728\u4ebf\u4e07\u5bcc\u7fc1Elon Musk\u770b\u6765\u8fd9\u4e2a\u7b54\u6848\u4e0d\u91cd\u8981\uff0c\u8fd1\u65e5\u4ed6\u5c31\u63a8\u51fa\u4e86\u4e00\u4e2a\u9879\u76ee\uff0c\u60f3\u8981\u5f00\u53d1\u8111\u673a\u63a5\u53e3\uff0c\u5c06\u4eba\u8111\u548c\u7535\u8111\u8fde\u63a5\u8d77\u6765\uff0c\u5b9e\u73b0\u4eba\u7c7b\u60f3\u6cd5\u7684\u4e0a\u4f20\u548c\u4e0b\u8f7d\u3002", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u4eba\u8111\u6309\u4e0a\u63d2\u5b54\uff0c\u53ef\u4e0e\u7535\u8111\u4e0a\u4f20\u4e0b\u8f7d\u8bb0\u5fc6\uff0c\u5f97\u5230\u6c38\u751f", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 197, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 111014, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 262741, "video_duration_str": "01:55", "source_url": "/item/6404344036781457921/", "item_id": "6404344036781457921", "article_genre": "video", "display_url": "http://toutiao.com/group/6404609753478562050/", "behot_time": 1491190336, "has_gallery": false, "group_id": "6404609753478562050"}, {"image_url": "http://p3.pstatp.com/list/190x124/19ff00055911f66d47a0", "single_mode": true, "abstract": "\u706b\u8f66\u5728\u94c1\u8f68\u4e0a\u8dd1\uff0c\u800c\u6c7d\u8f66\u884c\u9a76\u5728\u8def\u4e0a\uff0c\u8fd9\u662f\u5c0f\u5b69\u90fd\u77e5\u9053\u7684\u5e38\u8bc6\u3002\u4e0d\u8fc7\u53d1\u660e\u5bb6\u7684\u521b\u610f\u5c31\u662f\u8981\u6311\u6218\u5e38\u8bc6\uff0c\u82f1\u56fd\u6709\u4e2a\u94c1\u9053\u5de5\u4eba\u5c31\u6539\u88c5\u4e86\u81ea\u5df1\u7684\u8f66\uff0c \u8ba9\u5b83\u80fd\u591f\u5728\u94c1\u8f68\u4e0a\u884c\u9a76\uff0c\u4ece\u6b64\u9a7e\u7740\u5b83\u4e0a\u73ed\u3002", "image_list": [], "more_mode": false, "tag": "news_travel", "tag_url": "video", "title": "\u79c1\u5bb6\u8f66\u4e0a\u94c1\u8def\uff0c\u65e0\u4eba\u9a7e\u9a76\uff0c\u4e0a\u73ed\u4e0d\u5835\u8f66\uff0c\u4e0e\u706b\u8f66\u8d5b\u8dd1", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 149, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 421848, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 462722, "video_duration_str": "01:32", "source_url": "/item/6402862307340206594/", "item_id": "6402862307340206594", "article_genre": "video", "display_url": "http://toutiao.com/group/6404274692076798210/", "behot_time": 1491112487, "has_gallery": false, "group_id": "6404274692076798210"}, {"image_url": "http://p1.pstatp.com/list/190x124/19ff0004fa03fc91f3b8", "single_mode": true, "abstract": "\u4f1a\u88ab\u6bcd\u4e0a\u5927\u4eba\u903c\u7740\u4f60\u7a7f\u4e0a\u7684\u9664\u4e86\u79cb\u88e4\uff0c\u5176\u5b9e\u8fd8\u6709\u8896\u5957\u3002\u7231\u5e72\u51c0\u7684\u4eba\u5728\u5de5\u4f5c\u65f6\u4e00\u5b9a\u4f1a\u5957\u4e0a\u8896\u5957\uff0c\u9632\u6b62\u8896\u5b50\u88ab\u5f04\u810f\u3002\u4e0d\u8fc7\u8896\u5957\u7684\u529f\u80fd\u53ef\u4e0d\u6b62\u5982\u6b64\uff0c\u8fd9\u6b3e\u51ef\u592b\u62c9\u8896\u5957\u5c31\u6709\u88c5\u7532\u6548\u679c\uff0c\u7a7f\u4e0a\u5b83\u4e0d\u6015\u5200\u5272\u706b\u70e7\uff0c\u5f3a\u529b\u4fdd\u62a4\u624b\u81c2\u3002", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u8fd9\u8896\u5957\u6bd4\u94a2\u94c1\u786c5\u500d\uff0c\u53ef\u4ee5\u6321\u5200\uff0c\u7ed9\u8b66\u5bdf\u88c5\u5907\u4e0d\u9519", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 474, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 168341, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 299367, "video_duration_str": "01:36", "source_url": "/item/6403977204555842049/", "item_id": "6403977204555842049", "article_genre": "video", "display_url": "http://toutiao.com/group/6403977204555842049/", "behot_time": 1491098137, "has_gallery": false, "group_id": "6403977204555842049"}, {"image_url": "http://p3.pstatp.com/list/190x124/19fc0003bbb631ef2d6d", "single_mode": true, "abstract": "\u56e0\u4e3a\u6d77\u5e02\u8703\u697c\u7684\u5947\u666f\uff0c\u4eba\u4eec\u5e7b\u60f3\u51fa\u4ed9\u4eba\u5c45\u4f4f\u7684\u84ec\u83b1\u4ed9\u5c9b\u3001\u6d6e\u7a7a\u5929\u5bab\uff0c\u963f\u51e1\u8fbe\u7684\u7f8e\u4e3d\u6d6e\u7a7a\u5c9b\u4e5f\u8ba9\u4eba\u65e0\u6bd4\u795e\u5f80\u3002\u4ed9\u4eba\u548c\u5916\u661f\u4eba\u90fd\u6709\uff0c\u73b0\u5728\u4eba\u7c7b\u4e5f\u63d0\u51fa\u4e86\u4e00\u4e2a\u8d85\u6fc0\u8fdb\u7684\u5efa\u7b51\u8bbe\u8ba1\u6982\u5ff5Analemma Tower\uff0c\u628a\u5927\u53a6\u5efa\u5728\u534a\u7a7a\u4e4b\u4e2d\uff0c\u4ece\u5929\u800c\u964d\u7684\u60ac\u6302\u5728\u4e91\u5c42\u91cc\uff0c\u8fd9\u53ef\u80fd\u5417\uff1f", "image_list": [], "more_mode": false, "tag": "news_travel", "tag_url": "video", "title": "\u60ac\u7a7a\u9ad8\u697c\u6302\u5728\u5c0f\u884c\u661f\u4e0a\uff0c\u4e00\u5929\u98d8\u904d\u4e16\u754c\uff0c\u4f4f\u5728\u592a\u7a7a", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 30, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 4824, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 3952, "video_duration_str": "01:54", "source_url": "/item/6403916568270471681/", "item_id": "6403916568270471681", "article_genre": "video", "display_url": "http://toutiao.com/group/6403916568270471681/", "behot_time": 1491028454, "has_gallery": false, "group_id": "6403916568270471681"}, {"image_url": "http://p3.pstatp.com/list/190x124/19f60003007c74663210", "single_mode": true, "abstract": "\u4e0d\u4e0a\u73ed\u673a\u5668\u4eba", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u6709\u4e86\u8fd9\u9ed1\u79d1\u6280\uff0c\u8ba9\u4ed6\u66ff\u4f60\u4e0a\u73ed\uff0c\u53ef\u4ee5\u8fb9\u73a9\u8fb9\u5de5\u4f5c", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 53, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 17143, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 18756, "video_duration_str": "01:39", "source_url": "/item/6403600228422779394/", "item_id": "6403600228422779394", "article_genre": "video", "display_url": "http://toutiao.com/group/6403600228422779394/", "behot_time": 1491010168, "has_gallery": false, "group_id": "6403600228422779394"}, {"image_url": "http://p1.pstatp.com/list/190x124/19fd0000f76c5d4e29b2", "single_mode": true, "abstract": "", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u670d\u88c5\u6253\u5370\u673a\uff0c\u4e0d\u7528\u88c1\u7f1d\u7ecf\u9a8c\uff0c\u5f00\u4e2a\u5de5\u5382\u4e0a\u6dd8\u5b9d", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 182, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 101355, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 98472, "video_duration_str": "01:42", "source_url": "/item/6403231832250253825/", "item_id": "6403231832250253825", "article_genre": "video", "display_url": "http://toutiao.com/group/6403231832250253825/", "behot_time": 1491008513, "has_gallery": false, "group_id": "6403231832250253825"}, {"image_url": "http://p1.pstatp.com/list/190x124/19fa0002b9a203bed90a", "single_mode": true, "abstract": "\u706b\u7bad\u7b52\u6551\u751f\u5708", "image_list": [], "more_mode": false, "tag": "news", "tag_url": "video", "title": "\u5b66\u751f\u505a\u706b\u7bad\u70ae\uff0c\u5f00\u706b\u62ef\u6551\u6eba\u6c34\u8005\uff0c\u65f1\u9e2d\u5b50\u4e5f\u80fd\u6551\u4eba", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 85, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 14324, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 94660, "video_duration_str": "01:42", "source_url": "/item/6403228519890944514/", "item_id": "6403228519890944514", "article_genre": "video", "display_url": "http://toutiao.com/group/6403480954845626625/", "behot_time": 1490927214, "has_gallery": false, "group_id": "6403480954845626625"}, {"image_url": "http://p1.pstatp.com/list/190x124/1a90000d78c8360c6f68", "single_mode": true, "abstract": "\u6469\u897f\u6865", "image_list": [], "more_mode": false, "tag": "news", "tag_url": "video", "title": "\u6765\u81ea\u5723\u7ecf\uff0c\u6218\u4e89\u5e9f\u589f\u9020\u7684\u9690\u5f62\u6865\uff0c\u8ba9\u4f60\u884c\u8d70\u4e8e\u6c34\u4e2d", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 10, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 5456, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 19090, "video_duration_str": "01:44", "source_url": "/item/6403228083121291778/", "item_id": "6403228083121291778", "article_genre": "video", "display_url": "http://toutiao.com/group/6403228083121291778/", "behot_time": 1490922988, "has_gallery": false, "group_id": "6403228083121291778"}, {"image_url": "http://p3.pstatp.com/list/190x124/19f100055518453f58c3", "single_mode": true, "abstract": "\u4f26\u6566\u5927\u6eda\u6865", "image_list": [], "more_mode": false, "tag": "news", "tag_url": "video", "title": "\u6e38\u5ba2\u7b49\u51e0\u4e2a\u5c0f\u65f6\uff0c\u4e0d\u4e3a\u8fc7\u6865\uff0c\u53ea\u4e3a\u770b\u5b83\u53d8\u5f62", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 1482, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 3778595, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 4767941, "video_duration_str": "01:45", "source_url": "/item/6402429323789206018/", "item_id": "6402429323789206018", "article_genre": "video", "display_url": "http://toutiao.com/group/6402429323789206018/", "behot_time": 1490838536, "has_gallery": false, "group_id": "6402429323789206018"}, {"image_url": "http://p1.pstatp.com/list/190x124/19fb000037a2fcb775eb", "single_mode": true, "abstract": "\u89c1\u8fc7\u4e24\u4e2a\u8f6e\u5b50\u7684\u81ea\u884c\u8f66\uff0c\u4e09\u4e2a\u8f6e\u5b50\u7684\u4e09\u8f6e\u8f66\uff0c\u53ef\u662f\u8fd9\u73a9\u610f\u513f\u6709\u4e94\u4e2a\u8f6e\u5b50\uff0c\u5c45\u7136\u4e5f\u80fd\u79f0\u4e3a\u81ea\u884c\u8f66\uff0c\u4f60\u7edd\u5bf9\u6ca1\u6709\u89c1\u8fc7\u3002\u5b83\u7684\u524d\u8f6e\u88ab\u6362\u4e0a\u4e86\u50cf\u98de\u673a\u8d77\u843d\u67b6\u4e00\u6837\u7684\u56db\u8f6e\u7ed3\u6784\uff0c\u80fd\u8ba9\u4f60\u9a91\u5f97\u98de\u8d77\u3002", "image_list": [], "more_mode": false, "tag": "news_story", "tag_url": "video", "title": "5\u8f6e\u81ea\u884c\u8f66\uff0c\u659c\u7740\u9a91\u4e5f\u4e0d\u4f1a\u5012\uff0c\u5229\u7528\u8eab\u4f53\u8f6c\u5f2f", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 21, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 8437, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 13600, "video_duration_str": "01:26", "source_url": "/item/6402862072777933313/", "item_id": "6402862072777933313", "article_genre": "video", "display_url": "http://toutiao.com/group/6402862072777933313/", "behot_time": 1490836823, "has_gallery": false, "group_id": "6402862072777933313"}, {"image_url": "http://p1.pstatp.com/list/190x124/19f50004bf292e6959d0", "single_mode": true, "abstract": "\u5f53\u4f60\u8eab\u5904\u56fe\u4e66\u9986\u3001\u7f8e\u672f\u9986\u6216\u529e\u516c\u5ba4\u8fd9\u6837\u7684\u5b89\u9759\u573a\u5408\uff0c\u5374\u6709\u7535\u8bdd\u6253\u6765\u8ba9\u4f60\u4e0d\u5f97\u4e0d\u51fa\u53bb\u63a5\uff0c\u8fd9\u6837\u7684\u60c5\u51b5\u80af\u5b9a\u5927\u5bb6\u90fd\u9047\u5230\u8fc7\uff0c\u800c\u5982\u679c\u4f60\u65e2\u4e0d\u60f3\u6253\u6270\u522b\u4eba\uff0c\u53c8\u61d2\u5f97\u8fdb\u8fdb\u51fa\u51fa\u7684\u6253\u63a5\u7535\u8bdd\uff0c\u8fd9\u6b3e\u6d88\u97f3\u53e3\u7f69Hushme\u5c31\u80fd\u5e2e\u4e0a\u5fd9\uff0c\u8ba9\u4f60\u5728\u529e\u516c\u5ba4\u5531K\u90fd\u6ca1\u95ee\u9898\uff0c\u8fd8\u9644\u5e26\u53d8\u58f0\u529f\u80fd\u54e6\u3002", "image_list": [], "more_mode": false, "tag": "video_tech", "tag_url": "video", "title": "\u7528\u8fd9\u9ed1\u79d1\u6280\u53e3\u7f69\uff0c\u5728\u529e\u516c\u5ba4\u5531K\u6b4c\uff0c\u8001\u677f\u4e5f\u542c\u4e0d\u5230", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 277, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 47850, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 147957, "video_duration_str": "01:31", "source_url": "/item/6399518474011410946/", "item_id": "6399518474011410946", "article_genre": "video", "display_url": "http://toutiao.com/group/6399518474011410946/", "behot_time": 1490779995, "has_gallery": false, "group_id": "6399518474011410946"}, {"image_url": "http://p1.pstatp.com/list/190x124/19f5000403b91d8c3f74", "single_mode": true, "abstract": "\u5f53\u6211\u4eec\u5bf9\u519c\u6751\u7684\u5370\u8c61\u8fd8\u505c\u7559\u5728\u6ce5\u6cde\uff0c\u7b80\u964b\uff0c\u6df3\u6734\u7684\u65f6\u5019\uff0c\u6709\u4e00\u4e9b\u5730\u65b9\u65e9\u5df2\u6084\u6084\u5730\u53d1\u751f\u4e86\u53d8\u5316\u3002\u5728\u676d\u5dde\u7684\u5bcc\u9633\u4e1c\u6893\u5173\u6751\uff0c\u767d\u5c4b\u8fde\u7ef5\u6210\u7247\uff0c\u9edb\u74e6\u53c2\u5dee\u9519\u843d\uff0c\u6765\u5230\u8fd9\u91cc\u5c31\u4eff\u4f5b\u8d70\u8fdb\u4e86\u5434\u51a0\u4e2d\u7b14\u4e0b\u7684\u6c34\u58a8\u6c5f\u5357\uff0c\u518d\u4e5f\u770b\u4e0d\u89c1\u5f53\u5e74\u719f\u6089\u7684\u519c\u6751\u666f\u8c61\u3002", "image_list": [], "more_mode": false, "tag": "news_travel", "tag_url": "video", "title": "\u6700\u9002\u5408\u4e2d\u56fd\u4eba\u5c45\u4f4f\uff0c\u8ba9\u5b69\u5b50\u4e0d\u73a9\u624b\u673a\u7684\u623f\u5b50\uff0c\u624d1\u5343\u591a", "has_video": true, "chinese_tag": "\u89c6\u9891", "source": "Maxonor\u521b\u610f\u516c\u5143", "group_source": 2, "comments_count": 44, "media_url": "/m5857206714/", "media_avatar_url": "", "go_detail_count": 18211, "middle_mode": true, "gallary_image_count": 0, "detail_play_effective_count": 21304, "video_duration_str": "01:50", "source_url": "/item/6402128957415621121/", "item_id": "6402128957415621121", "article_genre": "video", "display_url": "http://toutiao.com/group/6402128957415621121/", "behot_time": 1490753623, "has_gallery": false, "group_id": "6402128957415621121"}], "is_self": false}
        """
        json_data = json.loads(doc)
        if not json_data['has_more'] == 0:
            return []
        params = self.get_params()
        base_url = ('http://www.toutiao.com/c/user/article/page_type=0&user_id={user_id}&'
                    'max_behot_time={max_behot_time}&count=20&as={AS}&cp={cp}')
        max_behot_time = json_data['next']['max_behot_time']
        user_id = re.findall(r'user_id=(\d+)', workUnit.url)[0]

        return [base_url.format(user_id=user_id, max_behot_time=max_behot_time, AS=params['as'], cp=params['cp'])]

    def get_video_url(self, display_url):

        return url

    def download_process(self, doc, workUnit):
        json_data = json.loads(doc)
        data_list = json_data['data']
        for data in data_list:
            display_url = data['display_url']
            title = data['title']
            intro = data['abstract']
            author = data['source']
            url = self.get_video_url(display_url)
            yield FileInfo(url, title, intro, '', author)

        requests.get(displayurl)



