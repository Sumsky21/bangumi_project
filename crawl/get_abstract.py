import requests
import re
from bs4 import BeautifulSoup


def get_content(name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    url = 'https://search.bilibili.com/bangumi?keyword=' + name
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, 'lxml')
    bangumi_list = soup.select('div.bangumi-item-wrap')

    if len(bangumi_list) == 0:
        print('自己百度')
        return -1
    else:
        # bangumi = bangumi_list[0]
        bangumi = soup.select('div.desc')[0]
        bangumi = str(bangumi).replace('\n', '').replace(' ', '')
        content = re.findall('简介：(.*)</div>', bangumi)[0]
        return content


if __name__ == '__main__':
    x = ['滑头鬼之孙', '三月的狮子', '银之匙', '犬夜叉']
    for anime in x:
        desc = get_content(anime)
        print(desc, '\n')