# coding=utf-8
# !/usr/bin/python
import sys
import requests
import json
import re
from bs4 import BeautifulSoup
import base64
from base.spider import Spider
import os

sys.path.append('..')
调试输出 = 1  # 0为关闭，1为开启  调试文件在根目录GKPY的文件中
folder_path = "/storage/emulated/0/GKPY"
file_name = "调试输出.txt"
file_path = os.path.join(folder_path, file_name)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with open(file_path, 'w') as file:
    file.write("还未开启调试。\n")

headerx2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'

}
本地脚本 = 1  # 0为关闭，1为开启
脚本名称 = '潮湿秘境.json'
file_path2 = os.path.join(folder_path, 脚本名称)
if 本地脚本 == 1:
    with open(file_path2, 'r', encoding='utf-8') as file:
        js1 = json.load(file)
else:
    res = requests.get('./潮湿秘境.json', headers=headerx2)
    js1 = json.loads(res.text)
keys_to_check = ['主页', '协议头', '推荐访问方式', '推荐协议头', '推荐提交数据', '推荐前缀', '推荐数组截取',
                 '推荐标题正则', '推荐地址正则', '推荐图片正则', '推荐小标题正则1', '推荐小标题正则2',
                 '推荐小标题前标1', '推荐小标题前标2', '分类前缀', '分类访问方式', '分类协议头',
                 '分类提交数据', '分类数组截取', '分类标题正则', '分类地址正则', '分类', '分类url',
                 '分类数据数组截取', '分类数据标题正则', '分类数据地址正则', '分类数据图片正则',
                 '分类数据小标题前标1', '分类数据小标题前标2', '分类数据小标题正则1',
                 '分类数据小标题正则2', '获取线路页面数组截取', '获取线路页面访问方式',
                 '获取线路页面协议头', '获取线路页面提交数据', '获取线路页面地址',
                 '获取线路页面片名正则', '获取线路页面年份正则', '获取线路页面简介正则',
                 '获取线路页面类别正则', '获取线路页面线路名正则', '获取线路页面线路地址正则1',
                 '获取线路页面线路数组截取', '获取线路页面线路地址正则2', '播放页面地址', '播放页面访问方式',
                 '播放页面协议头', '播放页面提交数据', '播放页面二次截取', '播放地址正则', '嗅探', '播放地址解码',
                 '搜索url', '搜索前缀', '搜索访问方式', '搜索协议头', '搜索提交数据', '搜索数据数组截取',
                 '搜索数据标题正则', '搜索数据地址正则', '搜索数据图片正则', '搜索数据小标题前标1',
                 '搜索数据小标题前标2', '搜索数据小标题正则1', '搜索数据小标题正则2']

# 批量检查键是否存在并赋值或置空
for key in keys_to_check:
    globals()[key] = js1[key] if key in js1 else ''


class Spider(Spider):
    global file_path
    global 调试输出

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def jxxyt(self, str):
        headerx1 = {}
        parts = str.split('#')
        for part in parts:
            if '$' in part:
                key_value = part.split('$')
                if len(key_value) > 1:
                    key = key_value[0].strip().replace(' ', '-')
                    value = key_value[1].strip()

                    if 'User-Agent' in key and value == '1':
                        value = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.61'
                    if 'User-Agent' in key and value == '2':
                        value = 'Mozilla/5.0 (Linux; Android 12; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36'
                    if 'User-Agent' in key and value == '3':
                        value = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1'
                    headerx1[key.lower()] = value

        return headerx1

    def homeContent(self, filter):
        result = {}
        result['class'] = []
        if '分类' in js1 and js1['分类'] != '':
            parts = js1['分类'].split('#')
            for part in parts:
                if '$' in part:
                    key_value = part.split('$')
                    if len(key_value) > 1:
                        key = key_value[0].strip().replace(' ', '-')
                        value = key_value[1].strip()
                        result['class'].append({'type_id': value, 'type_name': key})
        if '分类协议头' in js1 and js1['分类协议头'] != '':
            header = self.jxxyt(js1['分类协议头'])
        else:
            header = self.jxxyt(协议头)
        if '分类访问方式' in js1 and js1['分类访问方式'] == 'get':
            detail = requests.get(url=主页 + 分类前缀, headers=header)
        else:
            if '分类提交数据' in js1 and js1['分类提交数据'] != '':
                data = self.jxxyt(js1['分类提交数据'])
                detail = requests.post(url=主页 + 分类前缀, headers=header, data=data)

        detail.encoding = "utf-8"
        if '分类数组截取' in js1 and js1['分类数组截取'] != '':
            ym = self.hqjq(detail.text, 分类数组截取)
        else:
            ym = detail.text
        if '分类标题正则' in js1 and js1['分类标题正则'] != '':
            bt = self.zz(ym, 分类标题正则)
        else:
            bt = []
        if '分类地址正则' in js1 and js1['分类地址正则'] != '':
            dz = self.zz(ym, 分类地址正则)
        else:
            dz = []
        for i in range(len(bt)):
            if "http" not in dz[i]:
                id = 主页 + dz[i]
            else:
                id = dz[i]
            result['class'].append({'type_id': dz[i], 'type_name': bt[i]})
        
        if os.path.exists(file_path) and 调试输出 == 1:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("首页分类\n")
                f.write(json.dumps(result, ensure_ascii=False))
                f.write('\n')
        return result

    def homeVideoContent(self):
        result = {}
        videos = []
        try:
            if '推荐协议头' in js1 and js1['推荐协议头'] != '':
                header = self.jxxyt(js1['推荐协议头'])
            else:
                header = self.jxxyt(协议头)

            if '推荐访问方式' in js1 and js1['推荐访问方式'] == 'get':
                detail = requests.get(url=主页 + 推荐前缀, headers=header)
            else:
                if '推荐提交数据' in js1 and js1['推荐提交数据'] != '':
                    data = self.jxxyt(js1['推荐提交数据'])
                    detail = requests.post(url=主页 + 推荐前缀, headers=header, data=data)

            detail.encoding = "utf-8"
            if '推荐数组截取' in js1 and js1['推荐数组截取'] != '':
                ym = self.hqjq(detail.text, 推荐数组截取)
            else:
                ym = detail.text
            if '推荐标题正则' in js1 and js1['推荐标题正则'] != '':
                bt = self.zz(ym, 推荐标题正则)
            else:
                bt = []
            if '推荐地址正则' in js1 and js1['推荐地址正则'] != '':
                dz = self.zz(ym, 推荐地址正则)
            else:
                dz = []
            if '推荐图片正则' in js1 and js1['推荐图片正则'] != '':
                tp = self.zz(ym, 推荐图片正则)
            else:
                tp = []

            if '推荐小标题正则1' in js1 and js1['推荐小标题正则1'] != '':
                remark1 = self.zz(ym, 推荐小标题正则1)

            else:
                remark1 = []
            if '推荐小标题正则2' in js1 and js1['推荐小标题正则2'] != '':
                remark2 = self.zz(ym, 推荐小标题正则2)

            else:
                remark2 = []
            if '推荐小标题前标1' in js1 and js1['推荐小标题前标1'] != '':
                小标1 = js1['推荐小标题前标1']
            else:
                小标1 = ''
            if '推荐小标题前标2' in js1 and js1['推荐小标题前标2'] != '':
                小标2 = js1['推荐小标题前标2']
            else:
                小标2 = ''
            for i in range(len(bt)):
                if "http" not in dz[i]:
                    id = 主页 + dz[i]
                else:
                    id = dz[i]
                if "http" not in tp[i]:
                    pic = 主页 + tp[i]
                else:
                    pic = tp[i]
                value1 = ""
                value2 = ""

                if i < len(remark1):
                    value1 = remark1[i]

                if i < len(remark2):
                    value2 = remark2[i]
                else:
                    value2 = ""

                video = {
                    "vod_id": id,
                    "vod_name": bt[i],
                    "vod_pic": pic,
                    "vod_remarks": 小标1 + value1 + 小标2 + value2
                }

                videos.append(video)

            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        if '类型' in ext.keys():
            class_ = ext['类型']
        else:
            class_ = ''
        if '年代' in ext.keys():
            year = ext['年代']
        else:
            year = ""
        if '地区' in ext.keys():
            area = ext['地区']
        else:
            area = ""
        if '语言' in ext.keys():
            lang = ext['语言']
        else:
            lang = ""
        if '排序' in ext.keys():
            by = ext['排序']
        else:
            by = ""

        if not pg:
            pg = 1

        videos = []
        try:
            if '分类协议头' in js1 and js1['分类协议头'] != '':
                header = self.jxxyt(js1['分类协议头'])
            else:
                header = self.jxxyt(协议头)

            if '分类url' in js1 and js1['分类url'] != '':
                cateId = cid
                catePg = pg
                url = 分类url.format(cateId=cateId, catePg=catePg, **{"area": area}, **{"class": class_},
                                     **{"year": year}, **{"lang": lang}, **{"by": by})
                detail = requests.get(url=url, headers=header)
                detail.encoding = "utf-8"
                if '分类数据数组截取' in js1 and js1['分类数据数组截取'] != '':
                    ym = self.hqjq(detail.text, 分类数据数组截取)
                else:
                    ym = detail.text

                if '分类数据标题正则' in js1 and js1['分类数据标题正则'] != '':
                    bt = self.zz(ym, 分类数据标题正则)
                else:
                    bt = self.zz(ym, 推荐标题正则)
                if '分类数据地址正则' in js1 and js1['分类数据地址正则'] != '':
                    dz = self.zz(ym, 分类数据地址正则)
                else:
                    dz = self.zz(ym, 推荐地址正则)
                if '分类数据图片正则' in js1 and js1['分类数据图片正则'] != '':
                    tp = self.zz(ym, 分类数据图片正则)
                else:
                    tp = self.zz(ym, 推荐图片正则)

                if '分类数据小标题正则1' in js1 and js1['分类数据小标题正则1'] != '':
                    remark1 = self.zz(ym, 分类数据小标题正则1)
                else:
                    if '推荐小标题正则1' in js1 and js1['推荐小标题正则1'] != '':
                        remark1 = self.zz(ym, 推荐小标题正则1)
                    else:
                        remark1 = []

                if '分类数据小标题正则2' in js1 and js1['分类数据小标题正则2'] != '':
                    remark2 = self.zz(ym, 分类数据小标题正则2)
                else:
                    if '推荐小标题正则2' in js1 and js1['推荐小标题正则2'] != '':
                        remark2 = self.zz(ym, 推荐小标题正则2)
                    else:
                        remark2 = []

                if '分类数据小标题前标1' in js1 and js1['分类数据小标题前标1'] != '':
                    小标1 = js1['分类数据小标题前标1']
                else:
                    if '推荐小标题前标1' in js1 and js1['推荐小标题前标1'] != '':
                        小标1 = js1['推荐小标题前标1']
                    else:
                        小标1 = ''
                if '分类数据小标题前标2' in js1 and js1['分类数据小标题前标2'] != '':
                    小标2 = js1['分类数据小标题前标2']
                else:
                    if '推荐小标题前标2' in js1 and js1['推荐小标题前标2'] != '':
                        小标2 = js1['推荐小标题前标2']
                    else:
                        小标2 = ''
                for i in range(len(bt)):
                    if "http" not in dz[i]:
                        id = 主页 + dz[i]
                    else:
                        id = dz[i]
                    if "http" not in tp[i]:
                        pic = 主页 + tp[i]
                    else:
                        pic = tp[i]
                    try:
                        value1 = remark1[i]
                    except IndexError:

                        value1 = ""
                    try:
                        value2 = remark2[i]
                    except IndexError:
                        value2 = ""
                    video = {
                        "vod_id": id,
                        "vod_name": bt[i],
                        "vod_pic": pic,
                        "vod_remarks": 小标1 + value1 + 小标2 + value2
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
        if os.path.exists(file_path) and 调试输出 == 1:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("分类页面\n")
                f.write(json.dumps(result, ensure_ascii=False))
                f.write('\n')
        return result

    def detailContent(self, ids):
        if '获取线路页面地址' in js1 and js1['获取线路页面地址'] != '':
            did = js1['获取线路页面地址']
        else:
            did = ids[0]

        videos = []
        result = {}
        if '获取线路页面协议头' in js1 and js1['获取线路页面协议头'] != '':
            header = self.jxxyt(js1['获取线路页面协议头'])
        else:
            header = self.jxxyt(协议头)
        if '获取线路页面访问方式' in js1 and js1['获取线路页面访问方式'] == 'get':
            detail = requests.get(url=did, headers=header)
        else:
            if '获取线路页面提交数据' in js1 and js1['获取线路页面提交数据'] != '':
                data = self.jxxyt(js1['获取线路页面提交数据'])
                detail = requests.post(url=did, headers=header, data=data)
        detail.encoding = "utf-8"
        if '获取线路页面数组截取' in js1 and js1['获取线路页面数组截取'] != '':
            ym = self.hqjq(detail.text, 获取线路页面数组截取)
        else:
            ym = detail.text

        if '获取线路页面片名正则' in js1 and js1['获取线路页面片名正则'] != '':
            vod_name = self.zz(ym, 获取线路页面片名正则)
        else:
            vod_name = ''
        if '获取线路页面年份正则' in js1 and js1['获取线路页面年份正则'] != '':
            vod_year = self.zz(ym, 获取线路页面年份正则)
        else:
            vod_year = ''
        if '获取线路页面简介正则' in js1 and js1['获取线路页面简介正则'] != '':
            vod_content = self.zz(ym, 获取线路页面简介正则)
        else:
            vod_content = ''
        if '获取线路页面类别正则' in js1 and js1['获取线路页面类别正则'] != '':
            if '(.*?)' in js1['获取线路页面类别正则'] or '&&' in js1['获取线路页面类别正则']:
                type_name = self.zz(ym, 获取线路页面类别正则)
            else:
                type_name = 获取线路页面类别正则
        else:
            type_name = ''
        if '获取线路页面线路数组截取' in js1 and js1['获取线路页面线路数组截取'] != '':
            ym = self.hqjq(detail.text, 获取线路页面线路数组截取)
        else:
            ym = detail.text
        if '获取线路页面线路名正则' in js1 and js1['获取线路页面线路名正则'] != '':
            if '(.*?)' in js1['获取线路页面线路名正则'] or '&&' in js1['获取线路页面线路名正则']:
                playf1 = self.zz(ym, 获取线路页面线路名正则)
                playf = "$$$".join(playf1)
            else:
                playf = 获取线路页面线路名正则
        if '$$$' in playf:
            split_resources = playf.split("$$$")
            count = len(split_resources)

        if '获取线路页面线路地址正则1' in js1 and js1['获取线路页面线路地址正则1'] != '':
            purl = self.xl(ym, 获取线路页面线路地址正则1)
        else:
            purl = did
        if vod_name:
            vod_name = vod_name[0]
        else:
            vod_name = ''
        if type_name:
            type_name = type_name[0]
        else:
            type_name = ''
        if vod_year:
            vod_year = vod_year[0]
        else:
            vod_year = ''
        if vod_content:
            vod_content = vod_content[0]
        else:
            vod_content = ''

        videos.append({
            "vod_id": '',
            "vod_name": vod_name,
            "vod_pic": "",
            "type_name": type_name,
            "vod_year": vod_year,
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": vod_content,
            "vod_play_from": playf,
            "vod_play_url": purl
        })
        result['list'] = videos
        if os.path.exists(file_path) and 调试输出 == 1:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("获取播放页面\n")
                f.write(json.dumps(result, ensure_ascii=False))
                f.write('\n')
        return result

    def playerContent(self, flag, id, vipFlags):
        result = {}
        if '播放页面协议头' in js1 and js1['播放页面协议头'] != '':
            header = self.jxxyt(js1['播放页面协议头'])
        else:
            header = self.jxxyt(协议头)
        if '嗅探' in js1 and js1['嗅探'] != '':
            if 嗅探 == 1:
                if '播放地址解码' in js1 and js1['播放地址解码'] != '':
                    if js1['播放地址解码']=='UTF8':
                        id = bytes.fromhex(id.replace('%', '')).decode('utf-8')
                result["parse"] = 1
                result["playUrl"] = ''
                result["url"] = id
                result["header"] = header
                return result
        if '播放页面访问方式' in js1 and js1['播放页面访问方式'] == 'get':
            detail = requests.get(url=id, headers=header)
        else:
            if '播放页面提交数据' in js1 and js1['播放页面提交数据'] != '':
                data = self.jxxyt(js1['播放页面提交数据'])
                detail = requests.post(url=id, headers=header, data=data)
        detail.encoding = "utf-8"
        if '播放页面二次截取' in js1 and js1['播放页面二次截取'] != '':
            ym = self.hqjq(detail.text, 播放页面二次截取)
        else:
            ym = detail.text
        if '播放地址正则' in js1 and js1['播放地址正则'] != '':
            purl = self.zz(ym, 播放地址正则)
            purl = purl[0].replace('\\', '')
            if '播放地址解码' in js1 and js1['播放地址解码'] != '':
                if js1['播放地址解码'] == 'UTF8':
                    id = bytes.fromhex(id.replace('%', '')).decode('utf-8')
            result["parse"] = 0
            result["playUrl"] = ''
            result["url"] = purl
            result["header"] = header
            if os.path.exists(file_path) and 调试输出 == 1:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("获取播放地址\n")
                    f.write(json.dumps(result, ensure_ascii=False))
                    f.write('\n')
            return result
        else:
            if '播放地址解码' in js1 and js1['播放地址解码'] != '':
                if js1['播放地址解码'] == 'UTF8':
                    id = bytes.fromhex(id.replace('%', '')).decode('utf-8')
            result["parse"] = 1
            result["playUrl"] = ''
            result["url"] = id
            result["header"] = header
            if os.path.exists(file_path) and 调试输出 == 1:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("获取播放地址\n")
                    f.write(json.dumps(result, ensure_ascii=False))
                    f.write('\n')
            return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        if not page:
            page = 1
        if '搜索协议头' in js1 and js1['搜索协议头'] != '':
            header = self.jxxyt(js1['搜索协议头'])
        else:
            header = self.jxxyt(协议头)
        if '搜索url' in js1 and js1['搜索url'] != '':
            cateId = key
            catePg = page
            url = 搜索url.format(cateId=cateId, catePg=catePg)
            detail = requests.get(url=url, headers=header)
            if '搜索数据数组截取' in js1 and js1['搜索数据数组截取'] != '':
                ym = self.hqjq(detail.text, 搜索数据数组截取)
            else:
                ym = detail.text

            if '搜索数据标题正则' in js1 and js1['搜索数据标题正则'] != '':
                bt = self.zz(ym, 搜索数据标题正则)
            else:
                if '推荐标题正则' in js1 and js1['推荐标题正则'] != '':
                    bt = self.zz(ym, 推荐标题正则)
                else:
                    bt = []
            if '搜索数据地址正则' in js1 and js1['搜索数据地址正则'] != '':
                dz = self.zz(ym, 搜索数据地址正则)
            else:
                if '推荐地址正则' in js1 and js1['推荐地址正则'] != '':
                    dz = self.zz(ym, 推荐地址正则)
                else:
                    dz = []
            if '搜索数据图片正则' in js1 and js1['搜索数据图片正则'] != '':
                tp = self.zz(ym, 搜索数据图片正则)
            else:
                if '推荐图片正则' in js1 and js1['推荐图片正则'] != '':
                    tp = self.zz(ym, 推荐图片正则)
                else:
                    tp = []
            if '搜索数据小标题正则1' in js1 and js1['搜索数据小标题正则1'] != '':
                remark1 = self.zz(ym, 搜索数据小标题正则1)
            else:
                if '推荐小标题正则1' in js1 and js1['推荐小标题正则1'] != '':
                    remark1 = self.zz(ym, 推荐小标题正则1)
                else:
                    remark1 = []
            if '搜索数据小标题正则2' in js1 and js1['搜索数据小标题正则2'] != '':
                remark2 = self.zz(ym, 搜索数据小标题正则2)
            else:
                if '推荐小标题正则2' in js1 and js1['推荐小标题正则2'] != '':
                    remark2 = self.zz(ym, 推荐小标题正则2)
                else:
                    remark2 = []
            if '搜索数据小标题前标1' in js1 and js1['搜索数据小标题前标1'] != '':
                小标1 = js1['搜索数据小标题前标1']
            else:
                if '推荐小标题前标1' in js1 and js1['推荐小标题前标1'] != '':
                    小标1 = js1['推荐小标题前标1']
                else:
                    小标1 = ''
            if '搜索数据小标题前标2' in js1 and js1['搜索数据小标题前标2'] != '':
                小标2 = js1['搜索数据小标题前标2']
            else:
                if '推荐小标题前标2' in js1 and js1['推荐小标题前标2'] != '':
                    小标2 = js1['推荐小标题前标2']
                else:
                    小标2 = ''
            for i in range(len(bt)):
                value1 = ""
                value2 = ""

                if i < len(remark1):
                    value1 = remark1[i]

                if i < len(remark2):
                    value2 = remark2[i]
                else:
                    value2 = ""
                if "http" not in dz[i]:
                    id = 主页 + dz[i]
                else:
                    id = dz[i]
                if "http" not in tp[i]:
                    pic = 主页 + tp[i]
                else:
                    pic = tp[i]
                video = {
                    "vod_id": id,
                    "vod_name": bt[i],
                    "vod_pic": pic,
                    "vod_remarks": 小标1 + value1 + 小标2 + value2
                }
                videos.append(video)

        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        if os.path.exists(file_path) and 调试输出 == 1:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("搜索页面\n")
                f.write(json.dumps(result, ensure_ascii=False))
                f.write('\n')
        return result

    def str_decode(self, encoded_str):
        decoded_once = base64.b64decode(encoded_str)
        fully_decoded = base64.b64decode(decoded_once)
        return fully_decoded.decode('utf-8')

    def hqjq(self, text, str):
        start_str, end_str = str.split('&&')
        start_index = text.find(start_str) + len(start_str)
        end_index = text.find(end_str, start_index)
        substring = text[start_index:end_index]
        return substring

    def zz(self, ym, bds):
        if '#忽略' in bds:
            szt1, hl = bds.split('#忽略')
            szt = szt1.replace('&&', '(.*?)')
            hl = hl.split('$')
        else:
            szt = bds.replace('&&', '(.*?)')
            hl = 0

        vod = []
        pattern = rf'{szt}'
        matches = re.finditer(pattern, ym)

        for match in matches:
            id1 = match.group(1)
            if hl == 0:
                vod.append(id1)
            else:
                if any(item in id1 for item in hl):
                    continue
                else:
                    vod.append(id1)

        return vod if vod else []

    def xl(self, ym, bds):
        str = bds
        playf = ''
        playu = ''
        vod = ''
        if '#忽略' in bds:
            szt1, hl1 = bds.split('#忽略')
            szt = szt1
            hl1 = hl.split('$')
        else:
            szt = bds
            hl1 = 0
        szt = szt.replace('&&', '(.*?)')
        pattern = re.compile(rf'{szt}', re.DOTALL)
        matches = re.findall(pattern, ym)
        if len(matches) > 0:
            if '获取线路页面线路地址正则2' in js1 and js1['获取线路页面线路地址正则2'] != '':
                bds2 = js1['获取线路页面线路地址正则2']

                if '#忽略' in bds2:
                    szt2, hl2 = bds2.split('#忽略')
                    szt = szt2
                    hl2 = hl2.split('$')
                else:
                    szt = bds2
                    hl2 = 0
                address_index = szt.index("播放地址")
                title_index = szt.index("播放标题")
                szt3 = szt.replace('播放地址', '(.*?)')
                szt3 = szt3.replace('播放标题', '(.*?)')
                for match in matches:
                    if hl1 != 0:
                        if any(item in match.group(1) for item in hl1):
                            continue
                    pattern = rf'{szt3}'
                    matches2 = re.finditer(pattern, match)
                    for match2 in matches2:
                        if hl2 != 0:
                            if any(item in match2.group(1) for item in hl2) or any(
                                    item in match2.group(2) for item in hl2):
                                continue
                        if address_index < title_index:
                            if "http" not in match2.group(1):
                                vod += match2.group(2) + "$" + 主页 + match2.group(1) + "#"
                            else:
                                vod += match2.group(2) + "$" + match2.group(1) + "#"
                        else:
                            if "http" not in match2.group(1):
                                vod += match2.group(1) + "$" + 主页 + match2.group(2) + "#"
                            else:
                                vod += match2.group(1) + "$" + match2.group(2) + "#"
                    vod = vod + "$$$"
            vod = vod[:-4]

        return vod if vod else ""

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
