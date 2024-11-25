# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider


sys.path.append('..')
xurl = "https://jzy176.top"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
}
res=requests.get(xurl, headers=headerx)
match = re.search(r'<a href="(.*?)\/\?&"', res.text)
if match:
    xurl=match.group(1)
set_cookie_header = res.headers.get('Set-Cookie')
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
    'Cookie': set_cookie_header,
    'Referer':xurl
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

    def homeVideoContent(self):
        videos = []

        url = xurl + "/list/xvs.html"

        try:
            detail = requests.get(url=url, headers=headerx, timeout=10)
            detail.encoding = "utf-8"
            doc = BeautifulSoup(detail.text, "html.parser")
            soup = doc.find("div", class_='myvod')
            sourcediv = soup.find_all('li')
            for item in sourcediv:
                name = item.select_one("h4 a").text
                if "[" in name or "]" in name:
                    name = name.replace("[", "").replace("]", "")
                if "'" in name:
                    name = name.replace("'", "")
                id = xurl + item.select_one("h4 a")["href"]
                pic = item.select_one("a img ")["data-original"]
                remark = item.select_one("a span ").text
                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                }
                videos.append(video)
            result = {'list': videos}
            return result
        except:
            pass

    def homeContent(self, filter):
        url = xurl + "/list/xvs.html"
        res = requests.get(xurl, headers=headerx, timeout=10)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        sourcediv = doc.find_all('div', class_='myhot')
        vod = [a for div in sourcediv for a in div.find_all('a')]
        result = {}
        result['class'] = []
        for item in vod:
            name = item.text
            id = item['href']
            if "/list/xvs/" in id:
                continue
            else:
                id = id.replace("/list/xvs/", "")
            id = id.replace('0.html', '')
            result['class'].append({'type_id': id, 'type_name': name})
        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if not pg:
            pg = 1
        url = xurl + cid + "/" + str(pg) + '.html'
        detail = requests.get(url=url, headers=headerx, timeout=10)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        soup = doc.find("div", class_='myvod')
        sourcediv = soup.find_all('li')
        for item in sourcediv:
            name = item.select_one("h4 a").text
            if "[" in name or "]" in name:
                name = name.replace("[", "").replace("]", "")
            if "'" in name:
                name = name.replace("'", "")
            id = xurl + item.select_one("h4 a")["href"]
            pic = item.select_one("a img ")["data-original"]
            remark = item.select_one("a span ").text
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
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
        videos = []
        res = requests.get(url=did, headers=headerx, timeout=10)
        res = res.text
        source_match = re.search(r'<title>(.*?)- 剧情详细信息', res)
        if source_match:
            tx = source_match.group(1)
        source_match = re.search(r'<iframe src="(.*?)"', res)
        if source_match:
            plurl2 = source_match.group(1)
        res = requests.get(url=xurl + plurl2, headers=headerx, timeout=10)
        res = res.text

        source_match = re.search(r'"source": "(.*?)",', res)
        if source_match:
            plurl = source_match.group(1)
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
                "vod_play_from": "AV集中营",
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
        videos = []
        result = {}
        if not page:
            pg = 1
        else:
            pg = page
        url = xurl + '/search/xvs/' + key + "/" + str(pg) + '.html'

        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        soup = doc.find("div", class_='myvod')
        sourcediv = soup.find_all('li')
        for item in sourcediv:
            name = item.select_one("h4 a").text
            if "[" in name or "]" in name:
                name = name.replace("[", "").replace("]", "")
            if "'" in name:
                name = name.replace("'", "")
            id = xurl + item.select_one("h4 a")["href"]
            pic = item.select_one("a img ")["data-original"]
            remark = item.select_one("a span ").text
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
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
