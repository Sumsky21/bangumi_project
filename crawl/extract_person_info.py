import csv
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def main():
    # for job in ['stuff', 'cast', 'charactors']:
    for job in ['charactors']:
        print('getting {} info:'.format(job))
        path = './data/csv_files/'
        stuff_links = []
        stuff_info = []
        with open(path + job + '.csv', 'r', encoding='utf-8') as f:
            csv_file = csv.reader(f)
            header = next(csv_file)
            for row in csv_file:
                stuff_info.append(row)
                if job == 'charactors':
                    stuff_link = row[3]
                else:
                    stuff_link = row[2]
                stuff_links.append(stuff_link)

        for i, link in enumerate(stuff_links):
            if job == 'stuff':
                other_name_list, collections = search_for_stuff(link, job='stuff')
                stuff_info[i].append(other_name_list)
                stuff_info[i].append(collections)
                print(i, ' ', stuff_info[i][1], ': ', other_name_list)
                print('收藏数：{}\n'.format(collections))
            else:
                other_name_list = search_for_stuff(link)
                stuff_info[i].append(other_name_list)
                print(i, ' ', stuff_info[i][1], ': ', other_name_list)

        with open(path + job + '.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            if job == 'stuff':
                writer.writerow(['id', '中文名', '外文名', 'link', 'other names', '收藏'])
            else:
                writer.writerow(['id', '中文名', '外文名', 'link', 'other names'])
            for stuff in stuff_info:
                writer.writerow(stuff)
        print('get {} info over\n\n'.format(job))


def search_for_stuff(link, job=None):
    search_url = link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers).content
    soup = BeautifulSoup(response, 'lxml')
    info = soup.select('#infobox > li')

    other_name_list = []
    for d in info:
        r = 'tip".*?>(.*?): </span>'
        params = re.findall(r, str(d))
        for param in params:
            if param == '别名':
                r = '.*</span>(.*?)<'
                other_name = re.findall(r, str(d))[0]
                other_name = other_name.replace('\u3000', ' ')
                other_name_list.append(other_name)

    if job == 'stuff':
        collection_link = link + '/collections'
        response = requests.get(collection_link, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        pages = soup.select('.page_inner > a')
        if len(pages) == 0:
            collect_num = len(soup.select('#memberUserList > li'))
        else:
            max_page_code = pages[-2]
            # max_page_sig = re.findall('>(.*?)</a>', str(max_page_code))[0]
            # if max_page_sig == '››':
            #     max_page_code = pages[-2]

            max_page = re.findall('page=(.*?)"', str(max_page_code))[0]
            last_page_link = 'https://bgm.tv/' + re.findall('href="(.*?)"', str(max_page_code))[0]
            soup = BeautifulSoup(requests.get(last_page_link, headers=headers).content, 'lxml')
            last_page_num = len(soup.select('#memberUserList > li'))
            collect_num = (int(max_page) - 1) * 21 + last_page_num

    if len(other_name_list) == 0:
        other_name_list = 'none'
    elif len(other_name_list) == 1:
        other_name_list = other_name_list[0]

    if job == 'stuff':
        return other_name_list, collect_num
    else:
        return other_name_list


if __name__ == "__main__":
    main()
