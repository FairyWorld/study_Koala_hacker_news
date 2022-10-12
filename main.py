import os
import json
import requests

os.environ["NO_PROXY"] = "bilibili.com"

headers = {
    'authority': 'api.bilibili.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://space.bilibili.com',
    'referer': 'https://space.bilibili.com/489667127/channel/collectiondetail?sid=249279',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37',
}

def get_data() -> list[object]:
    page_num = 0
    while True:
        page_num += 1
        bv_list = []
        params = {
            'mid': '489667127',
            'season_id': '249279',
            'sort_reverse': 'false',
            'page_num': str(page_num),
            'page_size': '30',
        }

        response = requests.get('https://api.bilibili.com/x/polymer/space/seasons_archives_list', params=params, headers=headers)
        data = response.json()
        if len(data['data']['archives']) == 0:
            break

        print(len(data['data']['archives']))
        for obj in data['data']['archives']:
            bv_list.append(obj)

        yield bv_list


def get_commont_data() -> None:
    base_url = 'http://api.bilibili.com/x/v2/reply/main'
    for urls in get_data():
        for url in urls:
            data = json.loads(json.dumps(url))
            params = {
                'type': 1,
                'oid': data['aid']
            }
            commont_data = requests.get(url=base_url, params=params, headers=headers)
            commont_data = commont_data.json()
            with open('data.json', 'a', encoding='utf-8') as f:
                if commont_data['data']['top']['upper'] is not None:
                    f.write(json.dumps(commont_data['data']['top']['upper']['content'], ensure_ascii=False))
                else:
                    f.write(str(data['aid']))
                f.write(',')
                f.write('\n')

get_commont_data()

