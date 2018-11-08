import urls
from urllib import parse
def application(env, res):
    def requestsdecoder():
        def urldecoder(s):
            result = {}
            if '=' not in s:
                return None
            try:
                s = s.split('&')
            except:
                s = [s]
            for i in s:
                i_splited = i.split('=')
                i_splited[1]=parse.unquote(i_splited[1],'utf-8')
                result[i_splited[0]] = i_splited[1]
            return result

        method = env['REQUEST_METHOD']
        url = env['PATH_INFO']
        params = env['QUERY_STRING']
        params=urldecoder(params)
        ip = env['REMOTE_ADDR']
        clientname = env['uwsgi.node']
        clientname = str(clientname, encoding='utf-8')
        data = env['wsgi.input'].read()
        data = str(data, encoding='utf-8')
        data=urldecoder(data)

        result = dict(
            url=url,
            method=method,
            params=params,
            ip=ip,
            clientname=clientname,
            data=data,
            cookie=env['HTTP_COOKIE'] if 'HTTP_COOKIE' in env else None
        )
        return result

    reqdata=requestsdecoder()
    baseurls=urls.urls()
    result=baseurls.run(reqdata,res)
    yield result
