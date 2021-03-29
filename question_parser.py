
class QParser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        feature_types = res_classify['feature_types']
        sqls = []
        for feature_type in feature_types:
            sql_ = {}
            sql_['feature_type'] = feature_type
            sql = self.sql_transfer(feature_type, entity_dict.get('anime'))
            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, feature_type, entities):
        if not entities:
            return []
        # 查询语句
        sql = []
        if feature_type == 'painting':
            sql = ["match (s:stuff)-[r]->(a:anime) where a.name='{0}' and (r.job='人物设定' or r.job='原作' or r.job='美术监督') return s.name, s.收藏数".format(i) for i in entities]
        elif feature_type == 'plot':
            sql = ["match (s:stuff)-[r]->(a:anime) where a.name='{0}' and (r.job='原作') return s.name, s.收藏数".format(i) for i in entities]
        elif feature_type == 'music':
            sql = ["match (s:stuff)-[r]->(a:anime) where a.name='{0}' and r.job='音乐' return s.name, s.收藏数".format(i) for i in entities]
        elif feature_type == 'sakuga':
            sql = ["match (s:stuff)-[r]->(a:anime) where a.name='{0}' and (r.job='原画' or r.job='作画监督') return s.name, s.收藏数".format(i) for i in entities]
        elif feature_type == 'effect':
            sql = ["match (s:stuff)-[r]->(a:anime) where a.name='{0}' and r.job='摄影监督' return s.name, s.收藏数".format(i) for i in entities]
        elif feature_type == 'tempo':
            sql = ["match (s:stuff)-[r]->(a:anime) where a.name='{0}' and (r.job='系列构成' or r.job='监督') return s.name, s.收藏数".format(i) for i in entities]
        elif feature_type == 'casting':
            sql = ["match (s:cast)-[r]->(a:anime) where a.name='{0}' return s.name, s.收藏数".format(i) for i in entities]
        elif feature_type == 'others':
            sql = ["match (s:stuff)-[r]->(a:anime) where a.name='{0}' and (r.job='原作' or r.job='监督') return s.name, s.收藏数".format(i) for i in entities]
        return sql

if __name__ == '__main__':
    handler = QParser()
    res_classify = {'args': {'银之匙 Silver Spoon': ['anime']}, 'feature_types': ['others']}
    ret = handler.parser_main(res_classify)
    print(ret)
