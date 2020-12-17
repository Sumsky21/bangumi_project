import py2neo
from py2neo import Graph
import collections

class ASearcher:
    def __init__(self):
        self.g = py2neo.Graph(
            host = "sumsky.xyz",
            http_port = 7474,
            user = "neo4j",
            password = "bangumi-buaa"
        )
        self.num_limit = 7

    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls, set_anime):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['feature_type']
            queries = sql_['sql']
            staff_find = []
            favor = {}
            for query in queries:
                # print(query)
                ress = self.g.run(query).data()
                for pair in ress:
                    # print(pair)
                    if not 's.收藏数' in pair:
                        pair['s.收藏数'] = 1
                    staff_find.append(pair['s.name'])
                    favor[pair['s.name']] = pair['s.收藏数']   # if int(pair['s.收藏数']) < 150 else '150'
            # print(favor)
            ress = []
            anime_re = {}
            for i in staff_find:
                if '\'' in i:
                    i.replace("\'", "\\\'")
                sql = "match (s)-[r]->(a:anime) where s.name=\'{0}\' return a.name".format(i)
                ress = self.g.run(sql).data()
                for pair in ress:
                    a_name = pair['a.name']
                    if a_name in set_anime:
                        continue
                    if a_name in anime_re:
                        anime_re[a_name] += int(favor[i])
                    else:
                        anime_re[a_name] = int(favor[i])
            anime_dict = dict(collections.Counter(anime_re))
            anime_dict = sorted(anime_dict.items(), key=lambda d: (d[1], d[0]), reverse=True)
#             print(anime_dict)
            final_answer = self.answer_prettify(question_type, anime_dict[:self.num_limit])
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, feature_type, answers):
        final_answer = []
        if not answers:
            return ''
        if feature_type == 'painting':
            # print(answers)
            desc = [i[0] for i in answers]
            final_answer = '我推荐的类似画风的动画有：{0}'.format('\n'.join(list(desc)))
        if feature_type == 'plot':
            # print(answers)
            desc = [i[0] for i in answers]
            final_answer = '我推荐的类似剧情的动画有：{0}'.format('\n'.join(list(desc)))
        if feature_type == 'music':
            # print(answers)
            desc = [i[0] for i in answers]
            final_answer = '我推荐的配乐也很赞的动画有：{0}'.format('\n'.join(list(desc)))
        if feature_type == 'effect':
            # print(answers)
            desc = [i[0] for i in answers]
            final_answer = '我推荐的特效也很酷的动画有：{0}'.format('\n'.join(list(desc)))
        if feature_type == 'sakuga':
            # print(answers)
            desc = [i[0] for i in answers]
            final_answer = '我推荐的作画也很爆炸的动画有：{0}'.format('\n'.join(list(desc)))
        if feature_type == 'casting':
            # print(answers)
            desc = [i[0] for i in answers]
            final_answer = '我推荐的配音也很精彩的动画有：{0}'.format('\n'.join(list(desc)))
        if feature_type == 'others':
            desc = [i[0] for i in answers]
            final_answer = '我推荐类似动画有：{0}'.format('\n'.join(list(desc)))
        return final_answer


if __name__ == '__main__':
    searcher = ASearcher()
    sql = [{'feature_type': 'others', 'sql': ["match (s:staff)-[r]->(a:anime) where a.name='小魔女学园' and (r.job='原作' or r.job='监督') return s.name, s.收藏数"]}]
    set_anime = {'小魔女学园'}
    ret = searcher.search_main(sql, set_anime)
    print(ret)
