from tools.cookie import *
import massagesend
import modules
import random
import queue
import json
import hashlib

t = 1
cache = {'massage': [],'cookie':[]}
#设置缓存
user=modules.module(table='user')
movies=modules.module(table='movies')


def test(req, res):
    '''
    想法测试
    :param req:
    :param res:
    :return:
    '''
    res('200 ok', [('content-type', 'text/html; charset=utf-8')])
    global t
    t += 1
    return bytes(repr(cache), 'utf-8')


def signup(req, res):
    '''
    注册页
    共两次访问
    第一次携带手机号 number
        与随机验证码储存到缓存中
        向number发送验证码
    第二次访问携带手机号 number 密码 password 验证码 key
        向缓存校验验证码
            将number和password通过插入或修改写入数据库
            删除该条缓存
    验证缓存数量 大于最大缓存数量时删除最后一条缓存
    '''
    res('200 ok', [])
    reqdata = req['params']#选择通过get或post获取请求数据
    massagecache = cache['massage']
    if 'number' in reqdata:
        number = reqdata['number']
        if 'key' not in reqdata:
            tpl_value = ''.join([str(random.randint(0, 10)) for i in range(5)])
            massagecache.insert(0, (number, tpl_value))
            print(number, tpl_value)
            print(massagesend.send(number, tpl_value))
        elif 'password' in reqdata:
            j = -1
            for i in massagecache:
                j+=1
                if i[0] == number:
                    if i[1] == reqdata['key']:
                        id=user.exe("select id from user where usr='{}'".format(number))
                        if id:
                            sql=user.update("id='{0}'".format(id[0][0]),password=reqdata['password'])
                        else:
                            sql=user.insert(usr=number,password=reqdata['password'])
                        print(sql)
                        user.exe(sql)
                        user.commit()
                        massagecache.pop(j)
                        return b'seccess'
                    else:
                        return b'error'
            if not j+1:
                return b'serverError'
        else:
            return b'no password'
    if len(massagecache) > 10:
        massagecache.pop()
    print(massagecache)


def login(req, res):
    '''
    登陆页
    访问携带手机号作用户名 num 密码 password
    向数据库验证user和password
    向客户端返回登陆成功用户名
    '''

    reqdata = req['params']
    if 'num' in reqdata and 'password' in reqdata:
        usr=reqdata['num']
        password=reqdata['password']
        password_=user.select("WHERE usr={0}".format(usr),'password')[0]['password']
        if password_==password:
            cookie=mycookie(
                    cookie=dict(
                        token=hashlib.md5(
                            usr.encode('utf-8')).hexdigest()),
                    user=user
                )
            cache['cookie'].append(cookie)
            res('200 ok', [
                ('Content-Type', 'text/html;charset=UTF-8'),
                ('Server', 'yuyangServer v0.1'),
                *cookie.outputtuple()
            ])
            return bytes(usr,'utf-8')
        else:
            result= bytes('密码错误','utf-8')
    else:
        result= bytes('参数错误','utf-8')
    res('200 ok', [
        ('Content-Type', 'text/html;charset=UTF-8'),
        ('Server', 'yuyangServer v0.1'),
    ])
    return result

def movie(req,res):
    '''
    电影目录和信息获取
    请求可携带参数 id ，则返回movies表该id的整行
    如表中没有该id，则返回空
    如果不携带参数，则返回所有行的id，片名，海报，评分字段
    支持通过 id_start id_limit 两个参数截取表的部分行并返回部分行的id，片名，海报，评分字段
    支持通过参数 searchname 做片名搜索，并返回符合搜索的行的id，片名，海报，评分字段
    '''
    res('200 ok', [
        ('Content-Type', 'text/html;charset=UTF-8'),
        ('Server', 'yuyangServer v0.1'),
    ])
    reqdata = req['params']#选择通过get或post获取请求数据
    try:
        cookie=searchobjbycookie(cache['cookie'],'token',mycookie(req['cookie']).get('token').value)
    except:
        cookie=None
    if not cookie:
        return '没有登陆'.encode('utf-8')
    if not reqdata:
        result=movies.select("",'id','片名','海报','评分')
    elif 'id'in reqdata:
        result=movies.select("WHERE id='{0}'".format(reqdata['id']),'*')
    elif 'id_start' in reqdata and 'id_limit'in reqdata:
        result=movies.select(
            "WHERE id>'{0}' and id<'{1}'".format(reqdata['id_start'],str(int(reqdata['id_start'])+int(reqdata['id_limit']))),
            'id','片名','海报','评分'
        )
    elif 'searchname' in reqdata:
        result = movies.select(
            "WHERE 片名 like '%{0}%'".format(reqdata['searchname']),
            'id', '片名', '海报', '评分'
        )
    else:
        result={'error':'请求参数错误'}
    return bytes(json.dumps(result,ensure_ascii=False),'utf-8','ignore')

def notfound(req, res):
    res('404 notfound', [])
    return b'404 not found'