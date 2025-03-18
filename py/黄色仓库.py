# coding=utf-8
# !/usr/bin/python
import sys
import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider

sys.path.append('..')

headerx = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
    }
url = "http://666896.xyz/?u=http://6367ck.cc//&p="
response = requests.get(url,headers=headerx,allow_redirects=False)
xurl = response.headers.get("Location")
res = requests.get(xurl, headers=headerx)
res.encoding = "utf-8"

pattern = r'https://[\w\d\.\-]+:\d+/\?u='

result = re.search(pattern, res.text)
if result:
    extracted_url = result.group()
    xurl=extracted_url+xurl+'/&p='
    res= requests.get(xurl,headers=headerx,allow_redirects=False)
    xurl = res.headers.get("Location")

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
        try:
            res = requests.get(xurl, headers=headerx)
            res.encoding = "utf-8"
            doc = BeautifulSoup(res.text, "html.parser")
            sourcediv = doc.find_all('div', class_='stui-warp-content')

            vod = [a for div in sourcediv for a in div.find_all('li')]
            # print(vod)
            string_list = ["正宗莞式服务一条龙", "同城免费约炮", "免费约炮", "24小时同城大学生上门服务",
                           "24小时在线匹配首次免费"]
            for item in vod:
                name = item.select_one("h4 a").text
                if name in string_list:
                    continue
                id = item.find('a')['href']
                pic = item.select_one("a")["data-original"]
                remark = item.find("span", class_="pic-text text-right").text

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": "时长:" + remark
                }
                videos.append(video)
        except:
            pass
        result = {'list': videos}
        return result

    def homeContent(self, filter):
        res = requests.get(xurl, headers=headerx)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        sourcediv = doc.find_all('div', class_='stui-pannel stui-top-menu clearfix')
        # print(sourcediv)
        vod = [a for div in sourcediv for a in div.find_all('li')]
        result = {}
        result['class'] = []

        for item in vod:
            id = item.find('a')['href']
            id=id.replace(".html","")
            name = item.find('a').text
            name = re.sub(r'\d+', '', name)
            result['class'].append({'type_id': id, 'type_name': name})

        return result

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if pg:
            page = int(pg)
        else:
            page = 1
        res = requests.get(url=xurl + cid + "-" + str(page) + ".html", headers=headerx)
        res.encoding = "utf-8"
        res = res.text

        doc = BeautifulSoup(res, "html.parser")
        sourcediv = doc.find_all('div', class_='stui-warp-content')

        vod = [a for div in sourcediv for a in div.find_all('li')]
        # print(vod)
        string_list = ["正宗莞式服务一条龙", "同城免费约炮", "免费约炮", "24小时同城大学生上门服务"]
        for item in vod:
            h4_tag = item.select_one('h4.title > a')
            if h4_tag is not None:
                title = h4_tag.get('title')
                if title is not None:
                    name = title
                    if name in string_list:
                        continue
                    id = h4_tag.get('href')
                    pic = item.select_one('a', class_="stui-vodlist__thumb lazyload")['data-original']
                    remark = item.select_one('a', class_="stui-vodlist__thumb lazyload")
                    remark = remark.find('span', class_="pic-text text-right").text
                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": "时长:" + remark
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
        url = xurl
        res = requests.get(url + did, headers=headerx)
        res.encoding = "utf-8"
        res = res.text

        name_match = re.search(r'name="description" content="(.*?)剧情:" />', res)
        if name_match:
            tx = name_match.group(1)
        source_match = re.search(r'"url":\s*"([^"]+\.m3u8)"', res)
        if source_match:
            play_url = source_match.group(1)

        play_url = play_url.replace("\\", "")

        videos = []
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
            "vod_play_from": "在线播放",
            "vod_play_url": play_url
        })

        result = {}
        result['list'] = videos

        return (result)

    def playerContent(self, flag, id, vipFlags):
        result = {}

        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        result["header"] = headerx
        return result

    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        url = xurl + '/vodsearch/{0}----------{1}---.html'.format(key, page)
        res = requests.get(url=url, headers=headerx)
        res.encoding = "utf-8"
        doc = BeautifulSoup(res.text, "html.parser")
        sourcediv = doc.find_all('div', class_='stui-pannel-bd')

        vod = [a for div in sourcediv for a in div.find_all('li')]

        string_list = ["正宗莞式服务一条龙", "同城免费约炮", "免费约炮", "24小时同城大学生上门服务"]
        for item in vod:
            h4_tag = item.select_one('h4.title > a')
            if h4_tag is not None:
                title = h4_tag.get('title')
                if title is not None:
                    name = title
                    if name in string_list:
                        continue
                    id = h4_tag.get('href')
                    pic = item.select_one('a', class_="stui-vodlist__thumb lazyload")['data-original']
                    remark = item.select_one('a', class_="stui-vodlist__thumb lazyload")
                    remark = remark.find('span', class_="pic-text text-right").text
                    video = {
                        "vod_id": id,
                        "vod_name": name,
                        "vod_pic": pic,
                        "vod_remarks": "时长:" + remark
                    }
                    videos.append(video)
        result['list'] = videos
        result['page'] = page
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
