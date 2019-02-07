from http import cookies, cookiejar


class mycookie(cookies.SimpleCookie):
    def __init__(self, cookie=None, user=None, id=None):
        super(mycookie, self).__init__()
        cookie and self.load(cookie)
        self.user = user
        self.id = id

    def outputtuple(self, attrs=None):
        baseoutput = self.output(attrs=attrs)
        return [tuple(i.split(': ')) for i in baseoutput.split('\r\n')]


def searchobjbyuser(ittr, key):
    return ittr[key]


def searchobjbycookie(ittr, key, value):
    for i in ittr.keys():
        j = ittr[i]
        if key in j and j.get(key).value == value:
            return j


def logined(cookiec,req):
    try:
        cookie = searchobjbycookie(cookiec, 'token', mycookie(req['cookie']).get('token').value)
    except Exception as e:
        print(e)
        cookie = None
    return cookie