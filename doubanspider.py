import requests
from lxml import html
import modules
import re
import threading
import time

#目录页电影个数
pagelimit = 20

#目录页
homeurl = 'https://movie.douban.com/j/search_subjects'

#实例化会话对象
session = requests.Session()

#实例化数据表对象
movietable = modules.module('movies')


def saver(data):
    '''
    数据保存方法
    :param data:数据字典
    '''

    # 构造插入该数据的sql语句
    sql = movietable.insert(**data)

    # 执行插入语句
    movietable.exe(sql)



def pagedownload(movieurl):
    '''
    电影页面的下载和数据提取
    :param movieurl: 电影页面的url
    :return: 提取到的数据
    '''
    #创建一个空的字典用来保存提取到的数据
    data = dict()
    #下载网页并构造成 lxml 的 etree 对象
    h = session.get(movieurl).content
    h = html.fromstring(h)

    #数据提取
    article = h.xpath('.//div[@class="article"]')[0]
    presentation = article.xpath('.//div[@class="subjectwrap clearfix"]')[0]
    data['海报'] = presentation.xpath('.//img')[0].attrib['src']
    maindatalist = presentation.xpath('.//div[@id="info"]')[0]
    maindatatext = maindatalist.text_content()
    maindatatext = [i.lstrip() for i in maindatatext.split('\n')]
    for i in maindatatext:
        i = i.split(':')
        try:
            #由于符号/的存在会造成bug，解决方式为将字符串替换掉
            if i[0] == "制片国家/地区":
                i[0] = "制片国家"
            data[i[0]] = i[1]
        except:
            ...
    score = presentation.xpath('.//strong[@class="ll rating_num"]')[0].text
    data['评分'] = score
    playplace = h.xpath('.//div[@class="gray_ad"]/ul/li/a')
    data['观看地址'] = ''
    for i in playplace:
        site = i.attrib['data-cn']
        playurl = i.attrib['href']
        data['观看地址'] += site + '\t' + playurl + '\n'
    data['片名'] = h.xpath('.//span[@property="v:itemreviewed"]')[0].text
    data['简介'] = h.xpath('.//span[@property="v:summary"]')[0].text.lstrip()
    print(data['片名'])
    keys = list(data.keys())

    #为兼容数据库，去掉多余数据
    for i in keys:
        if i not in {'海报',
                     '导演',
                     '编剧',
                     '主演',
                     '类型',
                     '制片国家',
                     '语言',
                     '上映日期',
                     '片长',
                     '又名',
                     '评分',
                     '观看地址',
                     '片名',
                     '简介'
                     }:
            data.pop(i)
    return data


def homedownload(page):
    '''
    提取电影目录页中电影的url
    :param page: 目录页号如第一页目录，第二页目录
    :return: 电影页面的url
    '''
    params = dict(
        type='movie',
        tag='可播放',
        sort='recommend',
        page_limit=pagelimit,
        page_start=page * pagelimit
    )
    data = session.get(homeurl, params=params).json()
    for i in data['subjects']:
        yield i['url']


def init():
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }


if __name__ == '__main__':
    init()
    for j in range(0, 20):
        for i in homedownload(j):
            data=pagedownload(i)
            saver(data=data)
            time.sleep(2)
        movietable.commit()
    # pagedownload('https://movie.douban.com/subject/26985127/')
