# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider

sys.path.append('..')
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}
res=requests.get('https://www.fldz8.buzz/go.php',headers=headerx)
res.encoding = "utf-8"

match = re.search(r"var randUrl = '(.*?)'", res.text)
if match:
    xurl = match.group(1)

a=0
while a<5:
    try:
        res=requests.get(xurl,headers=headerx)
        if res.status_code==200:
            a=5
    except:
        res = requests.get('https://www.fldz8.buzz/go.php', headers=headerx)
        res.encoding = "utf-8"
        match = re.search(r"var randUrl = '(.*?)'", res.text)
        if match:
            xurl = match.group(1)
        a=a+1



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

    def fl(self, key):
        videos = []
        doc = BeautifulSoup(key, "html.parser")
        soup = doc.find('ul', class_="videos")
        soup2 = soup.find_all('li')
        for vods in soup2:
            name = vods.select_one("div a")['title']
            if "[" in name or "]" in name:
                name = name.replace("[", "").replace("]", "")
            if "'" in name:
                name = name.replace("'", "")
            id = xurl + vods.select_one("div a")["href"]
            if 'http' in vods.select_one("div a")["href"]:
                continue
            pic = vods.select_one("div a div img ")["src"]
            remark = vods.find('span', class_='video-overlay').get_text()

            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": '播放量:' + remark
            }
            videos.append(video)
        return videos

    def homeContent(self, filter):
        res = requests.get(xurl, headers=headerx, timeout=20)
        res.encoding = "utf-8"
        res = res.text
        doc = BeautifulSoup(res, "html.parser")
        result = {}
        result['class'] = []
        vodss = doc.find('div', class_="VIP")
        vod = vodss.find_all('a')
        for item in vod:
            id = item['href'].replace('.html', "")
            if 'http' in id or id == '/':
                continue
            name = item.text
            result['class'].append({'type_id': id, 'type_name': name})
        return result

    def homeVideoContent(self):

        try:
            res = requests.get(url=xurl, headers=headerx)
            res.encoding = "utf-8"
            res = res.text
            videos = self.fl(res)
            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        if not pg:
            pg = 1
        try:
            res = requests.get(xurl + cid + '/page/' + str(pg) + '.html', headers=headerx)
            res.encoding = "utf-8"
            res = res.text
            videos = self.fl(res)
        except:
            pass
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        did = ids[0]
        videos = []
        result = {}
        res = requests.get(did, headers=headerx)
        res.encoding = "utf-8"
        match = re.search(r'<div class="play"><a href="(.*?)"', res.text)

        if match:
            purl = xurl + match.group(1)

        videos.append({
            "vod_id": '',
            "vod_name": '',
            "vod_pic": "",
            "type_name": "ぃぅおか🍬 คิดถึง",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": "",
            "vod_play_from": "直链播放",
            "vod_play_url": purl
        })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        res = requests.get(id, headers=headerx)
        res.encoding = "utf-8"
        match = re.search(r'\},"url":"(.*?)"', res.text)

        if match:
            purl = match.group(1).replace('\\', '')
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = purl
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, page):
        result = {}
        if not page:
            page = 1

        res = requests.get(xurl + '/index.php/vod/search/page/' + str(page) + '/wd/' + key + '.html', headers=headerx)
        res.encoding = "utf-8"
        res = res.text
        videos = self.fl(res)
        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None
