import requests
from urllib.parse import urlencode
from hashlib import md5
import os
from multiprocessing.pool import Pool
import re
def get_page(offset):
    """offset是唯一变化的参数"""
    params={'offset': offset,
            'format': 'json',
            'keyword': '雪景',
            'autoload': 'true',
            'count': '20',
            'cur_tab': '1',
            'from': 'search_tab',
            'pd': 'synthesis'}
    base_url='https://www.toutiao.com/search_content/?'
    url=base_url+urlencode(params)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title=item.get('title')
            images=item.get('image_list')
            for image in images:
                yield{'image':'http:'+image.get('url'),
                      'title':title}

def save_image(item):
    img_path='img'+os.path.sep+item.get('title')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp=requests.get(item.get('image'))
        if resp.status_code==200:
            file_path=img_path+os.path.sep+'{file_name}.{file_suffix}'.format(file_name=md5(resp.content).hexdigest(),file_suffix='jpg')
            """hash.digest() 返回摘要，作为二进制数据字符串值
               hash.hexdigest() 返回摘要，作为十六进制数据字符串值"""
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded image path is %s' %file_path)
            else:
                print('already downloaded', file_path)
    except requests.ConnectionError:
        print('failed to save image,item %s' %item)

def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)

GROUP_START = 1
GROUP_END = 5

if __name__ == '__main__':
    pool = Pool()
    groups = ([x*20 for x in range(GROUP_START, GROUP_END+1)])
    pool.map(main, groups)
    pool.close()
    pool.join()




