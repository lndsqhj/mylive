# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider
from urllib.parse import unquote
sys.path.append('..')
xurl = "https://www.qdsy14.net"
headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
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
        xurl2 = "https://jzy176.top"
        headerx2 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
        }
        res = requests.get(xurl2, headers=headerx2)
        match = re.search(r'<a href="(.*?)\/\?&"', res.text)

        if match:
            xurl2 = match.group(1)
        set_cookie_header = res.headers.get('Set-Cookie')
        headerx3 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
            'Cookie': set_cookie_header
        }

        res = requests.get(xurl2, headers=headerx3)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        sourcediv = doc.find_all('div', class_='myhot')
        vod = [a for div in sourcediv for a in div.find_all('a')]
        result = {}
        result['class'] = []
        result['class'].append({'type_id': '/best/2024-03', 'type_name': '热门2024年5月'})
        result['class'].append({'type_id': '/best/2024-03', 'type_name': '热门2024年4月'})
        result['class'].append({'type_id': '/best/2024-03', 'type_name': '热门2024年3月'})
        result['class'].append({'type_id': '/best/2024-02', 'type_name': '热门2024年2月'})
        result['class'].append({'type_id': '/best/2024-01', 'type_name': '热门2024年1月'})
        result['class'].append({'type_id': '/best/2023-12', 'type_name': '热门2023年12月'})
        result['class'].append({'type_id': '/best/2023-11', 'type_name': '热门2023年11月'})
        result['class'].append({'type_id': '/best/2023-10', 'type_name': '热门2023年10月'})
        result['class'].append({'type_id': '/best/2023-09', 'type_name': '热门2023年9月'})
        result['class'].append({'type_id': '/best/2023-08', 'type_name': '热门2023年8月'})
        result['class'].append({'type_id': '/best/2023-07', 'type_name': '热门2023年7月'})
        result['class'].append({'type_id': '/best/2023-06', 'type_name': '热门2023年6月'})
        result['class'].append({'type_id': '/best/2023-05', 'type_name': '热门2023年5月'})
        result['class'].append({'type_id': '/best/2023-04', 'type_name': '热门2023年4月'})
        result['class'].append({'type_id': '/best/2023-03', 'type_name': '热门2023年3月'})
        result['class'].append({'type_id': '/best/2023-02', 'type_name': '热门2023年2月'})
        result['class'].append({'type_id': '/best/2023-01', 'type_name': '热门2023年1月'})

        for item in vod:
            name = item.text
            id = item['href']
            if "/list/xvs/" in id or '日韩系列' in name or '少女' in name or '国产系列' in name or '欧美巨屌' in name or '步兵无码' in name or '骑兵有码' in name or '成人动漫' in name:
                continue

            result['class'].append({'type_id': name, 'type_name': name})
        return result

    def homeVideoContent(self):
        try:
            videos = []
            detail = requests.get(url=xurl + '/searchav?k=chicken1806', headers=headerx)
            detail.encoding = "utf-8"
            doc = BeautifulSoup(detail.text, "html.parser")
            soup = doc.find_all('div', class_="frame-block thumb-block")
            for soup2 in soup:
                id = soup2.select_one("div div a")['href']
                pic = soup2.select_one("div div a img")['data-src']
                name = soup2.select_one("div p a").text
                remark1 = soup2.select_one("div p span span").text
                remark2 = soup2.select_one("div div a span").text
                if '秒' in remark2 or '分' in remark2:
                    remark2 = ''
                else:
                    remark2 = '-' + remark2
                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark1 + remark2
                }
                videos.append(video)
            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if not pg:
            pg = 0
        else:
            pg = int(pg) - 1

        videos = []
        try:
            if 'best' in cid:
                #/2024-02/1
                detail = requests.get(xurl + '/' + cid + '/' + str(pg), headers=headerx)
                detail.encoding = "utf-8"
                doc = BeautifulSoup(detail.text, "html.parser")
                soup = doc.find_all('div', class_="frame-block thumb-block")
                for soup2 in soup:
                    id = soup2.select_one("div div a")['href']
                    pic = soup2.select_one("div div a img")['data-src']
                    name = soup2.select_one("div p a").text
                    remark1 = soup2.select_one("div p span span").text
                    remark2 = soup2.select_one("div div a span").text
                    if '秒' in remark2 or '分' in remark2:
                        remark2 = ''
                    else:
                        remark2 = '-' + remark2
                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark1 + remark2
                    }
                    videos.append(video)
                result = {'list': videos}
            else:

                detail = requests.get(xurl + '/searchav?k=' + cid + '&p=' + str(pg), headers=headerx)
                detail.encoding = "utf-8"
                doc = BeautifulSoup(detail.text, "html.parser")
                soup = doc.find_all('div', class_="frame-block thumb-block")
                for soup2 in soup:
                    id = soup2.select_one("div div a")['href']
                    pic = soup2.select_one("div div a img")['data-src']
                    name = soup2.select_one("div p a").text
                    remark1 = soup2.select_one("div p span span").text
                    remark2 = soup2.select_one("div div a span").text
                    if '秒' in remark2 or '分' in remark2:
                        remark2 = ''
                    else:
                        remark2 = '-' + remark2
                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": remark1 + remark2
                    }
                    videos.append(video)
                result = {'list': videos}

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
        result = {}
        videos = []
        res = requests.get(url=xurl + did, headers=headerx)
        match = re.search(r"html5player.setVideoHLS\('(.*?)'", res.text)
        if match:
            playurl = match.group(1)
        videos.append({
            "vod_id": did,
            "vod_name": '',
            "vod_pic": "",
            "type_name": '',
            "vod_year": '',
            "vod_area": '',
            "vod_remarks": "",
            "vod_actor": '',
            "vod_director": '',
            "vod_content": '',
            "vod_play_from": '直链播放',
            "vod_play_url": playurl
        })

        result['list'] = videos

        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}

        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        if not page:
            page = 0
        else:
            page = int(page) - 1

        videos = []

        detail = requests.get(xurl + '/searchav?k=' + key + '&p=' + str(page), headers=headerx)
        detail.encoding = "utf-8"
        doc = BeautifulSoup(detail.text, "html.parser")
        soup = doc.find_all('div', class_="frame-block thumb-block")
        for soup2 in soup:
            id = soup2.select_one("div div a")['href']
            pic = soup2.select_one("div div a img")['data-src']
            name = soup2.select_one("div p a").text
            remark1 = soup2.select_one("div p span span").text
            remark2 = soup2.select_one("div div a span").text
            if '秒' in remark2 or '分' in remark2:
                remark2 = ''
            else:
                remark2 = '-' + remark2
            video = {
                "vod_id": id,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark1 + remark2
            }
            videos.append(video)

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
