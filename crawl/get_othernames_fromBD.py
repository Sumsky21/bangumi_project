import requests
import re
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd


def main():
    data_path = './data/csv_files/cast.csv'
    f = open(data_path, 'r', encoding='utf-8')
    csv_file = csv.reader(f)
    header = next(csv_file)
    new_data = {}
    count = 0
    for row in csv_file:
        cast_id = row[0]
        cast_name = row[1]
        cast_link = row[2]
        other_name = row[3]

        if other_name != 'none':
            other_name = other_name[1:-1].replace("'", '')
            other_name = re.split('[,、=＝/]', other_name)
        else:
            other_name = []

        search_result = search_cast(cast_name)
        if search_result == -1:
            search_result = {
                '中文名': cast_name,
                '外文名': cast_name,
                '别名': []
            }

        count += 1
        print(count, ' ', search_result)
        search_result['id'] = cast_id
        search_result['link'] = cast_link
        for n in other_name:
            n = n.strip()
            n = n.replace(r'\\t', '')
            if re.search(n, search_result['外文名']) is None:
                flag = True
                for new_n in search_result['别名']:
                    if re.search(n, new_n) is not None:
                        flag = False
                        break
            if flag:
                search_result['别名'].append(n)

        if len(search_result['别名']) == 0:
            search_result['别名'] = 'none'
        print(search_result['别名'], '\n')
        new_data[search_result['中文名']] = search_result
    f.close()

    json_data = json.dumps(new_data, ensure_ascii=False, indent=2, separators=(',', ':'))
    with open('./data/json_files/cast.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

    # with open('./data/json_files/cast.json', 'r', encoding='utf-8') as f:
    #     new_data = json.load(f)
    f = open('./data/csv_files/cast.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)
    writer.writerow(['id', '中文名', '外文名', '别名', 'link'])
    for k in new_data.keys():
        info = new_data[k]
        other_names = info['别名']
        fr_name = info['外文名']

        s1 = re.search('(\\u3000)', fr_name)
        s2 = re.search('(<.+>)', fr_name)

        if s1 is not None:
            fr_name = fr_name.replace(r'\\u3000', ' ')
        if s2 is not None:
            for s in s2.groups():
                fr_name = fr_name.replace(s, '')

        if other_names != 'none':
            for i, other_name in enumerate(other_names):
                other_names[i] = other_names[i].replace(r'\\t', '')
                other_names[i] = other_names[i].replace(r'\\u3000', ' ')
                other_names[i] = other_names[i].replace(r'\xa0', '')
                s2 = re.search('(<.+>)', other_name)

                if s2 is not None:
                    print(info['中文名'])
                    for s in s2.groups():
                        other_names[i] = other_names[i].replace(s, '')

        writer.writerow([info['id'], info['中文名'], fr_name, other_names, info['link']])
    f.close()


def search_cast(name):
    search_url = 'https://baike.baidu.com/item/' + name
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    info_key = soup.select('.basicInfo-block.basicInfo-left > .basicInfo-item.name')
    info_value = soup.select('.basicInfo-block.basicInfo-left > .basicInfo-item.value')

    if len(info_key) == 0:
        return -1

    fr_flag = False
    cn_flag = False
    ot_flag = False

    for index, x in enumerate(info_key):
        key = re.findall('<dt.*?>(.*?)</dt>', str(x))[0]
        info = re.findall('<dd.*>\n(.*?)\n.*', str(info_value[index]))
        if key == '中文名':
            cn_name = info[0].replace(' ', '').split('<')[0]
            cn_flag = True
        elif key == '外文名':
            fr_name = info[0].split('（')[0]
            fr_name = fr_name.split('、')[0].replace(' ', '')
            fr_flag = True

        elif len(re.findall('别.*?名', str(x))) != 0:
            other_name = info[0]
            other_name = re.split('[，、]', other_name)
            ot_flag = True

    if not cn_flag:
        cn_name = name
    if not fr_flag:
        fr_name = name
    if not ot_flag:
        other_name = []

    for i, x in enumerate(other_name):
        x = x.replace(r'\\u3000', '')
        x = x.replace(r'\xa0', '')
        x = x.replace(r'\\', '')
        s = re.search('(<.+>)', x)
        if s is not None:
            for s_ in s.groups():
                x = x.replace(s_, '')
        other_name[i] = x

    dic = {
        '中文名': cn_name,
        '外文名': fr_name,
        '别名': other_name
    }
    return dic


if __name__ == '__main__':
    main()