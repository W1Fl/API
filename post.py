#! /usr/bin/python3
import requests


print(requests.post('http://127.0.0.1:8000/url?asd=123&ss=11',{'wifi':'1234','aaa':32}).text)
