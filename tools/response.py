def simpleresponse(res,header=None):
    if header:
        res('200 ok', [
            ('Content-Type', 'text/html;charset=UTF-8'),
            ('Server', 'yuyangServer v0.1'),
            *header
        ])
    else:
        res('200 ok', [
            ('Content-Type', 'text/html;charset=UTF-8'),
            ('Server', 'yuyangServer v0.1'),
        ])


def res500(res):
    res('500 erroe', [
        ('Content-Type', 'text/html;charset=UTF-8'),
        ('Server', 'yuyangServer v0.1'),
    ])
