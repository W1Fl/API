import requests
import json

url = 'http://v.juhe.cn/sms/send'
tpl_id = '106935'
key = '3adefdc32c23a808d9af76aecb78a6d1'


def send(phonenumber, tpl_value):
    params = {
        'mobile': phonenumber,
        'tpl_id': tpl_id,
        'tpl_value': '#code#=' + tpl_value,
        'key': key
    }
    result = requests.get(url=url, params=params)
    loadsresult = json.loads(result.text)
    return loadsresult


if __name__ == '__main__':
    print(send('18285734822', '23232323'))
