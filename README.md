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
├── massagesend.py
├── modules.py
├── pages.py
├── post.py
├── setting.py
├── sql
│   ├── create_movie.sql
│   ├── create_user.sql
│   ├── movie_movies.sql
│   └── movie_user.sql
├── tools
│   ├── cookie.py
│   └── __init__.py
├── try.py
├── urls.py
└── uwsgi.ini
</pre>
<hr/>
<h3>
API文档
</h3>
<p>
这是一个wsgi规范的服务器应用,提供的接口有
<table>
<tr>
    <td>
    功能
    </td>
    <td>
    路径
    </td>
    <td>
    请求参赛
    </td>
    <td>
    响应
    </td>
    <td>
    注释
    </td>
</tr>
<tr>
    <td>
    注册和重设密码
    </td>
    <td>
    /signup
    </td>
    <td>
    number
    password
    key
    </td>
    <td>
    /
    </td>
    <td>
    完成注册操作需要请求两次,
    第一次发送电话号码,
    第二次发送电话号码,要设置的密码和验证码
    完成重设密码和完成注册操作一致
    </td>
</tr>
<tr>
    <td>
    登陆
    </td>
    <td>
    /login
    </td>
    <td>
    num
    password
    </td>
    <td>
    /
    </td>
    <td>
    登陆成功后将对客户端setcookie
    </td>
</tr>
<tr>
    <td>
    获取电影信息
    </td>
    <td>
    /movie
    </td>
    <td>
    id
    id_start
    id_limit
    searchname
    </td>
    <td>
    json
    </td>
    <td>
    需要登陆
    请求可携带参数 id ，则返回movies表该id的整行
    如表中没有该id，则返回空
    如果不携带参数，则返回所有行的id，片名，海报，评分字段
    支持通过 id_start id_limit 两个参数截取表的部分行并返回部分行的id，片名，海报，评分字段
    支持通过参数 searchname 做片名搜索，并返回符合搜索的行的id，片名，海报，评分字段
    </td>
</tr>
</table>
</p>
<hr/>