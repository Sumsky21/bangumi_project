import requests
from bs4 import BeautifulSoup
import re
import json


def main():
    with open('data/json_files/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open('data/json_files/data_link.json', 'r', encoding='utf-8') as f:
        data_link = json.load(f)

    new_data ={}
    for link in data_link.keys():
        anime_name = data_link[link]
        print(anime_name)
        if anime_name not in data.keys():
            continue

        anime_info = data[anime_name]
        anime_tags = get_tag(link)
        anime_info['tags'] = anime_tags
        new_data[anime_name] = anime_info

    json_data = json.dumps(new_data, ensure_ascii=False, indent=2, separators=(',', ':'))
    with open('data/json_files/new_data.json', 'w', encoding='utf-8') as f:
        f.write(json_data)


def get_tag(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    tags = soup.select('.subject_tag_section > .inner > a')
    tag_list = []
    for tag_text in tags:
        tag = re.findall('<span>(.*?)</span>', str(tag_text))[0]
        tag_list.append(tag)
    print(tag_list, '\n')
    return tag_list


if __name__ == '__main__':
    main()