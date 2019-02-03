import time

import requests
from lxml import html

import modules

# 目录页电影个数
pagelimit = 20

# 目录页
homeurl = 'https://movie.douban.com/j/search_subjects'
# 实例化会话对象
session = requests.Session()

# 实例化数据表对象
movietable = modules.module('Movie')
urltable = modules.module('movieUrl')
actortable = modules.module('actor')
actmovietable = modules.module('actor-movie')
clatable = modules.module('class')
clamovietable = modules.module('class-movie')
regtable = modules.module('region')
regmovietable = modules.module('region-movie')


def getid(table):
    return table.exe('select max(id) from {}'.format(table.table))


movieid = getid(movietable)
urlid = getid(urltable)
actid = getid(actortable)
classid = getid(clatable)
regid = getid(regtable)


def saver(data):
    '''
    数据保存方法
    :param data:数据字典
    '''

    global movieid, urlid, actid, classid, regid
    # 构造插入该数据的sql语句
    movieid += 1
    data['id'] = movieid
    actor = [i.strip() for i in data.pop('主演').split('/')]
    cla = [i.strip() for i in data.pop('类型').split('/')]
    reg = [i.strip() for i in data.pop('制片国家').split('/')]
    try:
        url = data.pop('观看地址')
        have_url = True
    except:
        have_url = False
    sql = movietable.insert(**data)
    # 执行插入语句
    movietable.exe(sql)
    movietable.commit()

    if have_url:
        for i in url.keys():
            urlid += 1
            sql = urltable.insert(id=urlid, 电影id=movieid, 平台=i, 地址=url[i])
            urltable.exe(sql)
        urltable.commit()

    for i in actor:
        id = actortable.select('where 姓名="{}"'.format(i), 'id')
        if not id:
            actid += 1
            id = actid
            sql = actortable.insert(姓名=i, id=actid)
            actortable.exe(sql)
            actortable.commit()
        else:
            id = id[0]['id']
        sql = actmovietable.insert(电影id=movieid, 演员id=id)
        actmovietable.exe(sql)
    actmovietable.commit()

    print(actor)
    for i in cla:
        id = clatable.select('where 类别名="{}"'.format(i), 'id')
        if not id:
            classid += 1
            id = classid
            sql = clatable.insert(类别名=i, id=classid)
            clatable.exe(sql)
            clatable.commit()
        else:
            id = id[0]['id']
        sql = clamovietable.insert(电影id=movieid, 类别id=id)
        clamovietable.exe(sql)
    clamovietable.commit()

    print(cla)
    for i in reg:
        id = regtable.select('where 地区="{}"'.format(i), 'id')
        if not id:
            regid += 1
            id = regid
            sql = regtable.insert(地区=i, id=regid)
            regtable.exe(sql)
            regtable.commit()
        else:
            id = id[0]['id']
        sql = regmovietable.insert(电影id=movieid, 地区id=id)
        regmovietable.exe(sql)
    print(reg)
    regmovietable.commit()


def pagedownload(movieurl):
    '''
    电影页面的下载和数据提取
    :param movieurl: 电影页面的url
    :return: 提取到的数据
    '''

    # 创建一个空的字典用来保存提取到的数据
    data = dict(豆瓣id=movieurl.split('/')[-2])
    # 下载网页并构造成 lxml 的 etree 对象
    h = session.get(movieurl).content
    h = html.fromstring(h)

    # 数据提取
    article = h.xpath('.//div[@class="article"]')[0]
    presentation = article.xpath('.//div[@class="subjectwrap clearfix"]')[0]
    data['海报'] = presentation.xpath('.//img')[0].attrib['src']
    maindatalist = presentation.xpath('.//div[@id="info"]')[0]
    maindatatext = maindatalist.text_content()
    maindatatext = [i.lstrip() for i in maindatatext.split('\n')]
    for i in maindatatext:
        i = i.split(':')
        try:
            # 由于符号/的存在会造成bug，解决方式为将字符串替换掉
            if i[0] == "制片国家/地区":
                i[0] = "制片国家"
            data[i[0]] = i[1]
        except:
            ...
    score = presentation.xpath('.//strong[@class="ll rating_num"]')[0].text
    data['评分'] = score
    playplace = h.xpath('.//div[@class="gray_ad"]/ul/li/a')
    data['观看地址'] = {}
    for i in playplace:
        site = i.attrib['data-cn']
        playurl = i.attrib['href']
        data['观看地址'][site] = playurl
    data['片名'] = h.xpath('.//span[@property="v:itemreviewed"]')[0].text
    data['简介'] = h.xpath('.//span[@property="v:summary"]')[0].text.lstrip()
    print(data['片名'])
    keys = list(data.keys())

    # 为兼容数据库，去掉多余数据
    for i in keys:
        if i not in {
            '豆瓣id',
            '海报',
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


def newmoviedownload(count=6):
    newmoviedata = session.get('https://api.douban.com/v2/movie/in_theaters?apikey=0b2bdeda43b5688921839c8ecb20399b',
                               params={'count': count}).json()
    return newmoviedata


def init():
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }


if __name__ == '__main__':
    init()
    for j in range(0, 20):
        for i in homedownload(j):
            data = pagedownload(i)
            saver(data=data)
            time.sleep(2)
