from pages import *
class urls():
    URLS={
        '/':test,
        '/signup':signup,
        '/login':login,
        '/movie':movie,
        '/newmovie':newmovie,
        '/sqlexe': sqlexe,
    }
    def run(self,req,res):
        try:
            return self.URLS[req['url']](req,res)
        except KeyError as e:
            print(e)
            return notfound(req,res)
