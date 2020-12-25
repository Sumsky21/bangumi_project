from bs4 import BeautifulSoup
import requests
import re


def extract_data(link, headers, params_list):
    response = requests.get(url=link, headers=headers).content
    soup = BeautifulSoup(response, 'lxml')

    if len(re.findall('呜咕，出错了', str(soup))) != 0:
        print('爬取里番失败2333')
        return -1

    data_dic = {}
    # data = soup.select('.nameSingle > a')
    # r = '<a.*?>(.*?)</a>'
    # data_dic['作品名称'] = re.findall(r, str(data[0]))

    # get stuff info
    data = soup.select('#infobox > li')
    for d in data:
        r = 'tip">(.*?): </span>'
        params = re.findall(r, str(d))
        for param in params:
            if param in params_list:
                data_dic[param] = []
                if param in ['中文名', '放送开始', '别名']:
                    r = '.*</span>(.*)<'
                    content = re.findall(r, str(d))
                else:
                    r = 'href="(.*?)".*?>(.*?)</a>'
                    contents = re.findall(r, str(d))
                    stuffs = []
                    for content in contents:
                        link, stuff_name = content
                        link = 'https://bgm.tv/' + link
                        content = [link, stuff_name]
                        stuffs.append(content)
                    content = stuffs
                data_dic[param] = content
    # get type
    type_list = [
        '搞笑', '百合', '治愈', '后宫', '校园', '恋爱', '科幻', '日常', '热血',
        '奇幻', '战斗', '萌', '青春', '悬疑', '机战', '催泪', '3D', '猎奇', '纯爱',
        '乙女', 'BL', '穿越', '励志', '运动', '爱情', '致郁', '耽美', '冒险', '欢乐',
        '友情', '血腥', '惊悚', '动作', '恐怖', '职场', '美食', '子供向'
    ]
    anime_type = []
    data = soup.select('.subject_tag_section > .inner > a')
    for d in data:
        r = '<span>(.*?)</span>'
        tag = re.findall(r, str(d))[0]
        if tag in type_list:
            anime_type.append(tag)
    data_dic['type'] = anime_type

    # get cast and charactors
    cast_dict = {}
    charactors = {}
    if len(soup.select('#browserItemList')) == 0:
        data_dic['cast'] = {}
        data_dic['charactors'] = {}
    else:
        charactor_names = []
        charactor_types = []
        cast_infos = []
        cast_data = soup.select('#browserItemList > li > .userContainer')
        for d in cast_data:
            charactor_link, charactor_name = re.findall('href="(.*?)" title=.(.*?).>', str(d))[0]
            charactor_link = 'https://bgm.tv' + charactor_link
            charactor_type = re.findall('class="badge_job_tip">(.*?)</span>', str(d))[0]
            cast_info = re.findall('href="(.*?)".*?>(.*?)</a>', str(d))

            charactor_names.append(charactor_name)
            charactor_types.append(charactor_type)
            cast_infos.append(cast_info)

            charactor_name_ = charactor_name.split('/')
            if len(charactor_name_) == 1:
                cn_name = charactor_name_[0].strip()
                fr_name = cn_name
            else:
                cn_name = charactor_name_[1].strip()
                fr_name = charactor_name_[0].strip()
            charactors[charactor_name] = {'中文名': cn_name, '外文名': fr_name, 'link': charactor_link}

        for i in range(len(cast_infos)):
            charactor_name = charactor_names[i]
            charactor_type = charactor_types[i]
            for cast in cast_infos[i]:
                cast_link, cast_name = cast
                cast_link = 'https://bgm.tv' + cast_link
                if cast_name in cast_dict.keys():
                    cast_dict[cast_name]['饰演角色'].append(charactor_type + ':' + charactor_name)
                else:
                    cast_dict[cast_name] = {
                        '饰演角色': [charactor_type + ':' + charactor_name],
                        'link': cast_link
                    }

        data_dic['cast'] = cast_dict
        data_dic['charactors'] = charactors

    # get related work
    related_work = {}
    data = soup.select('.content_inner > .browserCoverMedium > li')
    for d in data:
        key_word = re.findall('class="sub">(.+?)</span>', str(d))
        if len(key_word) == 1:
            now_key = key_word[0]
            related_work[now_key] = []

        work = re.findall('class="title" href="(.*?)">(.*?)</a>', str(d))[0]
        related_work[now_key].append(work)
    data_dic['related works'] = related_work

    # get tags
    tags = soup.select('.subject_tag_section > .inner > a')
    tag_list = []
    for tag_text in tags:
        tag = re.findall('<span>(.*?)</span>', str(tag_text))[0]
        tag_list.append(tag)
    data_dic['tags'] = tag_list

    return data_dic








