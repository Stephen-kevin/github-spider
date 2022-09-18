import requests

import csv

f=open('meituan.csv','a',encoding='utf-8',newline='')
csv_writer=csv.DictWriter(f,fieldnames=['商店id','标题','类型','评分','地区','商店链接'])

csv_writer.writeheader()#写入标头

url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/1?'
#美团的每一页网址不会变更，但变更的是offect,步值是32，没加一页，offect的值就加32
for page in range(0,332,32): #爬取多少页就写32的几倍
    data = {
        'uuid': '69993ecb60c34a978f20.1663341050.1.0.0',
        'userid': '2972418893',
        'limit': '32',
        'offset': page,#页数
        'cateId': '-1',
        'q': '足疗',#搜索的关键字
        'token': 'sHWfu0LekJSUnsVaf1cBfSnAwk4FAAAACRQAAOTup0xOGn8_w7gug8Me8qdd7JjaZnK0L_ATmecAwqwdpm5yxJ_0w1Rkg5A-JZCeHg',
    }

    headers = {
        'Referer': 'https://bj.meituan.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }

    resp = requests.get(url, params=data, headers=headers)
    # print(resp.text)
    # pprint.pprint(resp.json())
    searchresult = resp.json()['data']['searchResult']
    for item in searchresult:
        # pprint.pprint(item)
        shop_id = item['id']
        shop_url = f'https://www.meituan.com/xiuxianyule/{shop_id}'
        dict = {
            '商店id': item['id'],
            '标题': item['title'],
            '类型': item['backCateName'],
            '评分': item['avgscore'],
            '地区': item['areaname'],
            '商店链接': shop_url
        }
        csv_writer.writerow(dict)
        print(dict)
