import json
import csv


def main():
    f = open('data/json_files/data.json', 'r', encoding='utf-8')
    data = json.load(f)
    f.close()

    f = open('data/json_files/data_link.json', 'r', encoding='utf-8')
    data_link = json.load(f)
    f.close()

    with open('data/json_files/cast.json', 'r', encoding='utf-8') as f:
        new_cast = json.load(f)

    stuff_params_list = [
        '原作', '导演', '脚本', '分镜', '演出', '原画', '音乐', '人物设定', '系列构成',
        '美术监督', '色彩设计', '总作画监督', '作画监督', '摄影监督', '动画制作', '总导演'
    ]
    path = './data/csv_files/'

    # stuff - anime关系
    # f = open(path + 'stuff_anime.csv', 'w', encoding='utf-8', newline='')
    # writer = csv.writer(f)
    # writer.writerow(['anime', 'stuff', 'job'])
    # for anime_name in data.keys():
    #     anime_info = data[anime_name]
    #     for stuff_job in stuff_params_list:
    #         stuff_list = anime_info[stuff_job]
    #         if stuff_list == 'none':
    #             continue
    #         else:
    #             for stuff in stuff_list:
    #                 stuff_link = stuff[0]
    #                 writer.writerow([anime_name, stuff_link, stuff_job])
    # f.close()

    # cast - anime关系
    # f = open(path + 'cast_anime.csv', 'w', encoding='utf-8', newline='')
    # writer = csv.writer(f)
    # writer.writerow(['anime', 'cast'])
    # for anime_name in data.keys():
    #     anime_info = data[anime_name]
    #     cast_info = anime_info['cast']
    #     if cast_info == 'none':
    #         continue
    #     for cast_name in cast_info.keys():
    #         link = cast_info[cast_name]['link']
    #         for cast in new_cast.keys():
    #             if new_cast[cast]['link'] == link:
    #                 writer.writerow([anime_name, new_cast[cast]['link']])
    #                 break
    #
    # f.close()

    # cast - charactor关系
    # f = open(path + 'cast_charactor.csv', 'w', encoding='utf-8', newline='')
    # writer = csv.writer(f)
    # writer.writerow(['cast', 'charactor', 'type'])
    # for anime_name in data.keys():
    #     anime_info = data[anime_name]
    #     cast_info = anime_info['cast']
    #
    #     for cast_name in cast_info.keys():
    #         link = cast_info[cast_name]['link']
    #
    #         charactor_list = cast_info[cast_name]["饰演角色"]
    #         for cast in new_cast.keys():
    #             if new_cast[cast]['link'] == link:
    #                 cast_link = new_cast[cast]['link']
    #                 break
    #
    #         for charactor_name in charactor_list:
    #             charactor_type, charactor_name = charactor_name.split(':', 1)
    #             charactor_name = charactor_name.split('/')
    #             if len(charactor_name) == 1:
    #                 charactor_name = charactor_name[0]
    #             else:
    #                 charactor_name = charactor_name[1].strip()
    #             writer.writerow([cast_link, charactor_name, charactor_type])
    # f.close()

    # anime - charactor关系
    # f = open(path + 'anime_charactor.csv', 'w', encoding='utf-8', newline='')
    # writer = csv.writer(f)
    # writer.writerow(['anime', 'charactor'])
    # for anime_name in data.keys():
    #     anime_info = data[anime_name]
    #     if 'charactors' not in anime_info.keys():
    #         continue
    #     charactor_list = anime_info['charactors']
    #     for charactor_name in charactor_list.keys():
    #         charactor_link = charactor_list[charactor_name]['link']
    #         writer.writerow([anime_name, charactor_link])
    # f.close()

    # anime - anime关系
    f = open(path + 'anime_anime_2.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)
    writer.writerow(['anime1', 'anime2', 'relation'])
    related_list = ['番外篇', '前传', '续集', '总集篇', '不同演绎', '动画', ]
    for anime_name in data.keys():
        anime_info = data[anime_name]
        if 'related works' not in anime_info.keys():
            continue
        related_works = anime_info['related works']
        for relation in related_works.keys():
            if relation in related_list:
                related_work = related_works[relation]
                for work in related_work:
                    (work_link, work_name) = work
                    work_link = 'https://bgm.tv' + work_link

                    if work_link in data_link.keys():
                        work_name = data_link[work_link]
                        writer.writerow([work_name, anime_name, relation])
                        pass_relation(writer, data, data_link, work_name, anime_name, relation)

    f.close()


def pass_relation(writer, data, data_link, work_name, anime_name, relation_1):
    work = data[work_name]

    if work_name == '伪物语':
        print(anime_name)
        print(data[anime_name]['related works'], '\n')
        print(relation_1)
        print(work_name)
        print(work['related works'])
    if 'related works' not in work.keys():
        return
    else:
        related_works = work['related works']
        for relation in related_works.keys():
            if relation == '续集' and relation_1 == '续集':
                r = '续集'

            elif relation == '前传' and relation_1 == '前传':
                r = '前传'

            else:
                continue

            related_work = related_works[relation][0]
            link, name = related_work
            link = 'https://bgm.tv' + link
            # print(name)
            if link in data_link.keys():
                name = data_link[link]
                # print(name)
                writer.writerow([name, anime_name, r])
            return


if __name__ == '__main__':
    main()