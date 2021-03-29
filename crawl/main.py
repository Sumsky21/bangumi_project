import requests
from bs4 import BeautifulSoup
import re
import json
import csv
from crawl import extract_data


def main():
    url = 'https://bgm.tv/anime/browser?sort=rank&page='
    base_url = 'https://bgm.tv'
    pages = 210
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }

    params_list = [
        '中文名', '原作', '导演', '脚本', '分镜', '演出', '原画', '音乐', '人物设定', '系列构成',
        '美术监督', '色彩设计', '总作画监督', '作画监督', '摄影监督', '动画制作', '别名', '放送开始'
    ]

    stuff_params_list = [
        '原作', '导演', '脚本', '分镜', '演出', '原画', '音乐', '人物设定', '系列构成',
        '美术监督', '色彩设计', '总作画监督', '作画监督', '摄影监督', '动画制作'
    ]

    # 完整的动画信息记录
    anime_lists = {}
    stuff_lists = {}
    cast_lists = {}
    charactor_lists = {}
    rank = 0
    link_lists = {}
    for p in range(1, pages + 1):
        anime_url = url + str(p)
        res = requests.get(url=anime_url, headers=headers).content
        soup = BeautifulSoup(res, 'lxml')
        anime_list = soup.select('li > div > h3')

        r = '.*href="(.*)">(.*)</a>.*'
        for a in anime_list:
            rank += 1
            link_and_name = re.findall(r, str(a))
            link = base_url + link_and_name[0][0]
            name = link_and_name[0][1]
            data = extract_data(link, headers, params_list)
            if data == -1:
                continue
            for k in params_list:
                if k not in data.keys():
                    data[k] = 'none'
            data['rank'] = rank
            anime_lists[name] = data
            link_lists[link] = name
            print(name)
        print('page {} over\n\n'.format(p))
        if p % 10 == 0:
            sl_json_file(path='./data/json_files/data.json', mode='w', data=anime_lists)
            sl_json_file(path='./data/json_files/data_link.json', mode='w', data=link_lists)
            print('saved at page:{}'.format(p))

    sl_json_file(path='./data/json_files/data.json', mode='w', data=anime_lists)
    sl_json_file(path='./data/json_files/data_link.json', mode='w', data=link_lists)

    # anime_lists = sl_json_file(path='./data/json_files/data.json', mode='r')
    # link_lists = sl_json_file(path='./data/json_files/data_link.json', mode='r')

    # 生成节点csv文件
    for anime in anime_lists.keys():
        log = anime_lists[anime]
        for p in stuff_params_list:
            if p in log.keys():
                stuffs = log[p]
                if stuffs == 'none':
                    continue
                for stuff in stuffs:
                    link, name = stuff
                    if link in stuff_lists.keys():
                        continue
                    else:
                        stuff_lists[link] = name

        casts = log['cast']
        for cast_name in casts.keys():
            cast_info = casts[cast_name]
            link = cast_info['link']
            if link in cast_lists.keys():
                continue
            else:
                cast_lists[link] = cast_name

        if 'charactors' not in log.keys():
            continue
        charactors = log['charactors']
        for charactor_name in charactors.keys():
            charactor_info = charactors[charactor_name]
            charactor_link = charactor_info['link']
            if charactor_link in charactor_lists.keys():
                continue
            else:
                charactor_lists[charactor_link] = charactor_info

    print('get stuff & cast & charactors info over !')

    full_data_list = {'anime': anime_lists, 'stuff': stuff_lists, 'cast': cast_lists, 'charactors': charactor_lists}
    save_data(full_data_list)


def save_data(data):
    node_list = ['anime', 'stuff', 'cast', 'charactors']
    for phase in node_list:
        writeCSV(data=data[phase], phase=phase, path='./data/csv_files/')
    return


def writeCSV(data, phase, path):
    f = open(path + phase + '.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)

    if phase == 'anime':
        writer.writerow(['id', 'name', 'time', 'other names', 'type', 'tags', 'rank'])
        for i, name in enumerate(data.keys()):
            d = data[name]
            writer.writerow(['A' + str(i + 1), name, d['放送开始'],  d['别名'], d['type'], d['tags'], d['rank']])

    elif phase == 'stuff':
        writer.writerow(['id', 'name', 'link'])
        for i, stuff_link in enumerate(data.keys()):
            writer.writerow(['P' + str(i+1), data[stuff_link], stuff_link])
    elif phase == 'cast':
        writer.writerow(['id', 'name', 'link'])
        for i, cast_link in enumerate(data.keys()):
            writer.writerow(['CA' + str(i+1), data[cast_link], cast_link])
    else:
        writer.writerow(['id', '中文名', '外文名', 'link'])
        for i, charactor_link in enumerate(data.keys()):
            charactor_info = data[charactor_link]
            cn_name = charactor_info['中文名']
            fr_name = charactor_info['外文名']
            writer.writerow(['CH' + str(i+1), cn_name, fr_name, charactor_link])
    f.close()
    return


def sl_json_file(path, mode, data=None):
    with open(path, mode, encoding='utf-8') as f:
        if mode == 'w':
            json_data = json.dumps(data, ensure_ascii=False, indent=2, separators=(',', ':'))
            f.write(json_data)
            return
        else:
            data = json.load(f)
            return data


if __name__ == '__main__':
    main()