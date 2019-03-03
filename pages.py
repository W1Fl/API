import hashlib
import json
import random
import time
import messagesend
import modules
from tools.cache import *
from tools.cookie import *
from tools.response import *
from tools.render import *


message = Cache('message')
cookiec = Cache('cookie')
# 设置缓存

# 实例化数据表对象
usertable = modules.module('user')
movietable = modules.module('Movie')
urltable = modules.module('movieUrl')
actortable = modules.module('actor')
actmovietable = modules.module('actor-movie')
clatable = modules.module('class')
clamovietable = modules.module('class-movie')
regtable = modules.module('region')
regmovietable = modules.module('region-movie')
dynamictable = modules.module('dynamic')
datatuple = ('id', '片名', '海报', '简介')


def test(req, res):
    '''
    想法测试
    :param req:
    :param res:
    :return:
    '''
    simpleresponse(res)
    yield render('test.html', {})




def signup(req, res):
    '''
    注册页
    共两次访问
    第一次携带手机号 user
        与随机验证码储存到缓存中
        向user发送验证码
    第二次访问携带手机号 user 密码 password 验证码 key
        向缓存校验验证码
            将user和password通过插入或修改写入数据库
            删除该条缓存
    验证缓存数量 大于最大缓存数量时删除最后一条缓存
    '''
    simpleresponse(res)
    reqdata = req['params']  # 选择通过get或post获取请求数据
    result = b'error'
    if 'user' in reqdata and reqdata['user']:
        number = reqdata['user']

        if 'key' not in reqdata:
            tpl_value = ''.join([str(random.randint(0, 9)) for i in range(6)])
            message.set(number, tpl_value, 120)
            print(message[number])
            messagesend.send(number, tpl_value)
            result = b'waiting'

        elif 'password' in reqdata:
            if message[number] and message[number] == reqdata['key']:
                id = usertable.exe("select id from user where usr='{}'".format(number))
                if id:
                    sql = usertable.update("id='{0}'".format(id[0][0]), password=reqdata['password'])
                else:
                    sql = usertable.insert(usr=number, password=reqdata['password'])
                print(sql)
                usertable.exe(sql)
                usertable.commit()
                message.del_(number)
                result = b'success'

        else:
            result = b'no password'
    else:
        result = '参数错误'.encode('utf-8')

    yield result


def login(req, res):
    '''
    登陆页
    访问携带手机号作用户名 user 密码 password
    向数据库验证user和password
    向客户端返回登陆成功用户名
    '''

    reqdata = req['params']
    if 'user' in reqdata and 'password' in reqdata:
        usr = reqdata['user']
        password = reqdata['password']
        try:
            sqlres = usertable.select("WHERE usr={0}".format(usr), 'id', 'password')[0]
            userid = sqlres['id']
            password_ = sqlres['password']
        except:
            password_ = None
        if password_ == password:
            cookie = mycookie(
                cookie=dict(
                    token=hashlib.md5(
                        (usr + str(time.time())).encode('utf-8')).hexdigest()),
                user=usr,
                id=userid,
            )
            cookiec.set(cookie.user, cookie, 0)
            simpleresponse(res, cookie.outputtuple())
            yield bytes(usr, 'utf-8')
            return
        else:
            result = bytes('密码错误', 'utf-8')
    else:
        result = bytes('参数错误', 'utf-8')
    simpleresponse(res)
    yield result


def findmovie(reqdata):
    '''
    查找电影的其他方法
    :param reqdata: 查询方式和查询参数
    :return: 查询结果
    '''

    result = None

    if 'actorname' in reqdata:
        result = actortable.select("where 姓名='{}'".format(reqdata['actorname']), '*')


    elif 'actorid' in reqdata:
        movieid = tuple(i['电影id'] for i in actmovietable.select("where 演员id='{}'".format(reqdata['actorid']), '电影id'))
        result = movietable.select("where id in {} and 状态='0'".format(str(movieid)), *datatuple)

    elif 'classid' in reqdata:
        if reqdata['classid'] == '0':
            result = clatable.select("", '*')
        else:
            movieid = tuple(
                i['电影id'] for i in clamovietable.select("where 类别id='{}'".format(reqdata['classid']), '电影id'))
            result = movietable.select("where id in {} and 状态='0'".format(str(movieid)), *datatuple)

    return result


def movie(req, res):
    '''
    电影目录和信息获取
    请求可携带参数 id ，则返回movies表该id的整行
    如表中没有该id，则返回空
    如果不携带参数，则返回所有行的id，片名，海报，评分字段
    支持通过 id_start id_limit 两个参数截取表的部分行并返回部分行的id，片名，海报，评分字段
    支持通过参数 searchname 做片名搜索，并返回符合搜索的行的id，片名，海报，评分字段
    其他查询:
    actorname:演员姓名,返回该演员的id
    classid:类别id,返回该类别所有电影的基本参数,如果传递的值为0则返回类别表
    '''
    simpleresponse(res)
    reqdata = req['params']  # 选择通过get或post获取请求数据
    cookie = logined(cookiec, req)
    state = int(reqdata.get('state', -1))
    # if not cookie:
    #     yield '没有登陆'.encode('utf-8')
    #     return
    if not reqdata:
        result = movietable.select("", *datatuple)

    elif ~state:
        result = movietable.select("where 状态='{}'".format(state), *datatuple)

    elif 'id' in reqdata:
        result = movietable.select("WHERE id='{0}'".format(reqdata['id']), '*')
        actorids = tuple(i['演员id'] for i in actmovietable.select("where 电影id='{}'".format(reqdata['id']), '演员id'))
        result[0]['演员'] = actortable.select("where id in {}".format(str(actorids)), '*')
        result[0]['类别'] = clatable.select(
            "where id in (select 类别id from `class-movie` where 电影id='{}')".format(reqdata['id']), '*')
        # 使用两种方法实现了演员(分开查询)和类别(子查询)的查询
        result[0]['观看链接'] = {i['平台']: i['地址'] for i in urltable.select("where 电影id='{}'".format(reqdata['id']), '*')}


    elif 'searchname' in reqdata:
        result = movietable.select(
            "WHERE 片名 like '%{0}%'".format(reqdata['searchname']),
            *datatuple
        )

    elif 'id_start' in reqdata and 'id_limit' in reqdata:
        result = movietable.select(
            "WHERE id between '{0}' and '{1}'".format(reqdata['id_start'],
                                                      str(int(reqdata['id_start']) + int(reqdata['id_limit']))),
            *datatuple
        )
    else:
        result = findmovie(reqdata)
        if not result:
            result = {'error': '请求参数错误'}

    yield bytes(json.dumps(result, ensure_ascii=False), 'utf-8', 'ignore')


def dynamic(req, res):
    '''
    查看动态和写动态的功能
    写动态的参数有
    constant:动态内容
    base:回复的动态id,不回复则不传递该参数
    movie:被评论的电影id,不对电影评论则不传递该参数
    查看动态的参数有
    start:分页查询开始
    end:分页查询结束
    以下是不必要参数:
        userid:用户id,查询这个用户的动态
        movieid:电影id,查询这个电影的评论
        baseid:动态id,查询这条动态的所有回复
    '''
    simpleresponse(res)
    reqdata = req['params']  # 选择通过get或post获取请求数据
    cookie = logined(cookiec, req)
    if not cookie:
        yield '没有登陆'.encode('utf-8')
        return
    contant = reqdata.get('constant', 'NULL')
    if contant != 'NULL':
        try:
            base = reqdata.get('base', 'NULL')
            movieid = reqdata.get('movie', 'NULL')
            userid = cookie.id
            sql = dynamictable.insert(用户id=userid, 回复=base, 电影id=movieid, 内容=contant)
            dynamictable.exe(sql)
            dynamictable.commit()
            yield '动态发表成功'.encode('utf-8')
        except Exception as e:
            yield '参数错误'.encode('utf-8')
            yield str(e).encode('utf-8')
            return
    elif 'start' in reqdata and 'end' in reqdata:
        if 'userid' in reqdata:
            result = dynamictable.select("where 用户id='%s' order by id desc limit %d,%d" % (
                reqdata['userid'], int(reqdata['start']), int(reqdata['end'])), '*')

        elif 'movieid' in reqdata:
            result = dynamictable.select("where 电影id ='%s' order by id desc limit %d,%d" % (
                reqdata['movieid'], int(reqdata['start']), int(reqdata['end'])), '*')
        elif 'baseid' in reqdata:
            result = dynamictable.select("where 回复 ='%s' order by id desc limit %d,%d" % (
                reqdata['baseid'], int(reqdata['start']), int(reqdata['end'])), '*')

        else:
            result = dynamictable.select("order by id desc limit %d,%d" % (int(reqdata['start']), int(reqdata['end'])),
                                         '*')
        for i in range(len(result)):
            result[i]['时间'] = result[i]['时间'].strftime('%Y-%m-%d %H:%M:%S')
        yield bytes(json.dumps(result, ensure_ascii=False), 'utf-8', 'ignore')


def notfound(req, res):
    res('404 notfound', [])
    yield b'404 not found'


def sqlexe(req, res):
    '''
    sql注入点,可以直接传递sql语句
    '''
    # cookie = logined(cookiec, req)
    # if not cookie:
    #     yield '没有登陆'.encode('utf-8')
    #     return
    try:
        reqdata = req['params']
        sql = reqdata['sql'].replace('+', ' ')
        if 'DELETE' in sql.upper() or 'DROP' in sql.upper():
            simpleresponse(res)
            yield "还想给我删库".encode('utf-8')
            return
        table = modules.module(None)
        result = table.exe(sql)
        table.commit()
        simpleresponse(res)
        yield bytes(json.dumps(result), 'utf-8')
    except Exception as e:
        res500(res)
        yield bytes(str(e), 'utf-8')
