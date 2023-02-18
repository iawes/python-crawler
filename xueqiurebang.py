# -*-coding:utf-8-*-
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests
from bs4 import BeautifulSoup as bs
import os


headers = {
    'Host': 'stock.xueqiu.com',
    'Referer': 'https://xueqiu.com/',
    'X-Application-Context': 'xueqiu-stock-api-rpc:production',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Cookie': 's=d51140p2x7; xq_a_token=6702b19c0b6d4d2d59430b9183f50ff6f6765df0; xq_r_token=8a297928044afcb3a5ae17b718b8d769452e7259; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjMyOTc5MDIyMTYsImlzcyI6InVjIiwiZXhwIjoxNjc4MzY3ODQ3LCJjdG0iOjE2NzU3NzU4NDczMjEsImNpZCI6ImQ5ZDBuNEFadXAifQ.O1qBbi4BSeTf74jFXJlD2f5-KzIkZiLI3DvvDOM0bBQRc-CFI7fuZoQXLy0CtSuYvSNuJM_SU9pAiMMe2rf44weok392aeI_UG2-KwhbJ4_YMjNRwL_ihrG-2usxCF1oFiuGmHC53yFVS-3H9Zq-tROhE9wyi8SlpNOue3SeOCwf1ZoqniSi0JWeC9ZY3gck-RCdjbbii5Qyv0HILVZDgH-vy66gZxkxAAx_qN_elgyS5IkNcbfaHwjG3XCrjLNmYK_sfzLkXeitTzjfRN27VAfc2TZbZBiD1ZrGDTswaX2Gth8sRMDlDT_uCaSlNjIw7M7SfxulnQRRguxfi2ByyA; u=3297902216; device_id=e0af2150664c2495dbb52e2c56dad6c8; xqat=6702b19c0b6d4d2d59430b9183f50ff6f6765df0; xq_is_login=1; snbim_minify=true; bid=0625ebb550437a0c62af9a7579c66f43_ldu9pawj'
}
base_url = 'https://stock.xueqiu.com/v5/stock/hot_stock/list.json?'


def get_stock_list():
    params = {
        'size': 200,
        '_type': 12,
        'type': 12
    }
    url = base_url + urlencode(params)
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_info(json):
    if json:
        items = json.get('data').get('items')
        for i in items:
            info = {}
            info['code'] = i.get('code')
            info['name'] = i.get('name')
            info['value'] = i.get('value')
            yield info


json = get_stock_list()
results = parse_info(json)
for result in results:
    print(result)