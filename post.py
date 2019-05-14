#! /usr/bin/python3
import requests

sess = requests.Session()

print(sess.get('http://127.0.0.1:8000/login', params={'user': '18285734822', 'password': 12345}).text)
print(sess.get('http://127.0.0.1:8000/collection', params={}).text)
