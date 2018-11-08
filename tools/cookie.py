from http import cookies,cookiejar

class mycookie(cookies.SimpleCookie):
    def __init__(self,cookie=None,user=None):
        super(mycookie, self).__init__()
        cookie and self.load(cookie)
        self.user=user
    def outputtuple(self,attrs=None):
        baseoutput=self.output(attrs=attrs)
        return [tuple (i.split(': '))for i in baseoutput.split('\r\n')]

def searchobjbyuser(ittr,key):
    for i in ittr:
        if i.user==key:return i

def searchobjbycookie(ittr,key,value):
    for i in ittr:
        if key in i and i.get(key).value==value:
            return i