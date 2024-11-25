# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider
import random

sys.path.append('..')
xurl = "https://xn--n6wedekmhijklmnopqrstuvwxyz0a1a2a3a4a5a6a.semanji5.shop/"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
}
class Spider(Spider):
    global xurl
    global headerx


    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        res = requests.get(xurl, headers=headerx)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        sourcediv = doc.find('div', class_='content clearfix')
        vod = sourcediv.find_all('li', class_='is-keyword btn btn-default')
        result = {}
        result['class'] = []
        for item in vod:
            id = item.find('a')['href']
            name = item.find('a').text
            result['class'].append({'type_id': id, 'type_name': name})

        return result

    def homeVideoContent(self):
        videos = []
        try:
            res = requests.get(xurl, headers=headerx)
            res.encoding = "utf-8"
            # print(res.text)
            doc = BeautifulSoup(res.text, "html.parser")
            sourcediv = doc.find('div', id='content')
            vod = sourcediv.find_all('div', class_='thumb-block')
            for item in vod:
                name = item.select_one("div p a")['title']
                pic = item.select_one("div a img")["data-src"]
                remark1 = item.select_one("div a span").text
                remark2 = item.select_one("div p span span").text
                id = item.select_one("div p a")['href']
                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark1 + ' 时长: ' + remark2
                }
                videos.append(video)
        except:
            pass
        result = {'list': videos}
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if not pg:
            pg = "1"
        else:
            pg = int(pg)-1

        url = xurl + cid+"&p="+str(pg)
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        sourcediv = doc.find('div', id='content')
        vod = sourcediv.find_all('div', class_='thumb-block')
        for item in vod:
            name = item.select_one("div p a")['title']
            pic = item.select_one("div a img")["data-src"]
            remark1 = item.select_one("div a span").text
            remark2 = item.select_one("div p span span").text
            id = item.select_one("div p a")['href']
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark1 + ' 时长: ' + remark2
            }
            videos.append(video)

        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        result = {}
        res = requests.get(url=xurl + did, headers=headerx)
        res = res.text
        source_match = re.search(r"html5player.setVideoHLS\('(.*?)'", res)
        if source_match:
            plurl = source_match.group(1)
        videos = []
        source_match = re.search(r'<title>(.*?) - XVIDEOS\.COM</title>', res)
        if source_match:
            tx = source_match.group(1)
        videos.append({
            "vod_id": did,
            "vod_name": tx,
            "vod_pic": "",
            "type_name": "ぃぅおか🍬 คิดถึง",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": "",
            "vod_play_from": "XVIDEOS",
            "vod_play_url": plurl
        })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        str3 = id
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = str3
        result["header"] = headerx
        return result

    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def searchContentPage(self, key, quick, page):

        result = {}
        videos = []
        if not page:
            page = "1"
        else:
            page = int(page) - 1

        url = xurl + key + "&p=" + str(pg)
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        sourcediv = doc.find('div', id='content')
        vod = sourcediv.find_all('div', class_='thumb-block')
        for item in vod:
            name = item.select_one("div p a")['title']
            pic = item.select_one("div a img")["data-src"]
            remark1 = item.select_one("div a span").text
            remark2 = item.select_one("div p span span").text
            id = item.select_one("div p a")['href']
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark1 + ' 时长: ' + remark2
            }
            videos.append(video)

        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None
