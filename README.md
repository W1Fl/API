<h1>
一个看电影app的后台接口
</h1>
<hr/>
<h2>
目录结构
</h2>
<pre>
.
├── application.py
├── doubanspider.py
├── img
│   └── 1.jpg
├── messagesend.py
├── modules.py
├── pages.py
├── post.py
├── README.md
├── setting.py
├── sql
│   ├── movie_Movie.sql
├── temp.html
├── tools
│   ├── cache.py
│   ├── cookie.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── cache.cpython-36.pyc
│   │   ├── cookie.cpython-35.pyc
│   │   ├── cookie.cpython-36.pyc
│   │   ├── __init__.cpython-35.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── render.cpython-36.pyc
│   │   └── response.cpython-36.pyc
│   ├── render.py
│   └── response.py
├── try.py
├── urls.py
└── uwsgi.ini
</pre>
<hr/>
<h3>
API文档
</h3>
<p>
这是一个wsgi规范的服务器应用,<br/>提供的接口有
<table>
<tr>
    <td>
    功能<br/>
    </td>
    <td>
    路径<br/>
    </td>
    <td>
    请求参赛<br/>
    </td>
    <td>
    响应<br/>
    </td>
    <td>
    注释<br/>
    </td>
</tr>
<tr>
    <td>
    注册和重设密码<br/>
    </td>
    <td>
    /signup<br/>
    </td>
    <td>
    user<br/>
    password<br/>
    key<br/>
    </td>
    <td>
    /
    </td>
    <td>
    完成注册操作需要请求两次,<br/>
    第一次发送电话号码,<br/>
    第二次发送电话号码,要设置的密码和验证码<br/>
    完成重设密码和完成注册操作一致<br/>
    </td>
</tr>
<tr>
    <td>
    登陆<br/>
    </td>
    <td>
    /login<br/>
    </td>
    <td>
    user<br/>
    password<br/>
    </td>
    <td>
    /<br/>
    </td>
    <td>
    登陆成功后将对客户端setcookie<br/>
    </td>
</tr>
<tr>
    <td>
    获取电影,演员,类别信息<br/>
    </td>
    <td>
    /movie<br/>
    </td>
    <td>
    id<br/>
    id_start<br/>
    id_limit<br/>
    searchname<br/>
    actorname<br/>
    state<br/>
    actorid<br/>
    classid<br/>
    </td>
    <td>
    json<br/>
    </td>
    <td>
    需要登陆<br/>
    请求可携带参数 id ，则返回movies表该id的整行<br/>
    如表中没有该id，则返回空<br/>
    如果不携带参数，则返回所有行的id，片名，海报，评分字段<br/>
    支持通过 id_start id_limit 两个参数截取表的部分行并返回部分行的id，片名，海报，评分字段<br/>
    支持通过参数 searchname 做片名搜索，并返回符合搜索的行的id，片名，海报，评分字段<br/>
    </td>
</tr>
<tr>
    <td>
    动态读写<br/>
    </td>
    <td>
    /dynamic<br/>
    </td>
    <td>
    constant<br/>
    base<br/>
    movie<br/>
    start<br/>
    end<br/>
    baseid<br/>
    movieid<br/>
    userid<br/>
    </td>
    <td>
    json<br/>
    </td>
    <td>
    需要登陆<br/>
    写动态时携带参数 constant <br/>
    可携带参数base表示回复的动态id<br/>
    可携带参数movie表示被评论的电影id<br/>
    获取动态时携带参数start和end,表示获取动态分页<br/>
    可以通过userid movieid baseid获取对应动态列表<br/>
    </td>
</tr>
<tr>
    <td>
    sql执行<br/>
    </td>
    <td>
    /sqlexe<br/>
    </td>
    <td>
    sql<br/>
    </td>
    <td>
    json<br/>
    </td>
    <td>
    可以执行sql语句,危险<br/>
    </td>
</tr>
</table>
</p>
<hr/>
<h3>
层次结构
</h3>
<p>
<pre>
项目顶层为application.py 被wsgi服务器调用
application.py解析请求信息,调用路由urls.py
urls.py 通过url参数调用pages.py的函数执行该路径的功能
page.py作为应用执行,需要时使用modules.py执行数据库相关功能,使用tools/cookie.py执行cookie相关功能,使用tools/cache.py完成后台缓存
doubanspider.py独立存在,用于爬取豆瓣电影的数据保存到数据库
setting.py保存设置信息,如连接数据库所需信息
数据库使用mysql
</pre>
</p>