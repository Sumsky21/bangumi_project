import os
import jieba
import jieba.analyse
from rapidfuzz import fuzz
from rapidfuzz import process
from opencc import OpenCC

cc = OpenCC('t2s')
class QClassifier:
    def __init__(self):
        jieba.load_userdict("data/anime_dict.txt")
        jieba.load_userdict("data/staff_dict.txt")
        this_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        data_dir = os.path.join(this_dir, 'data')
        # 实体名词路径
        self.anime_path = os.path.join(data_dir, 'anime.txt')
        self.staff_path = os.path.join(data_dir, 'staff.txt')
        self.cast_path = os.path.join(data_dir, 'cast.txt')
        self.character_path = os.path.join(data_dir, 'character.txt')
        # 加载名词列表
        self.anime_list = [i.strip() for i in open(self.anime_path, encoding="utf-8") if i.strip()]
        self.staff_list = [i.strip() for i in open(self.staff_path, encoding="utf-8") if i.strip()]
        self.cast_list = [i.strip() for i in open(self.cast_path, encoding="utf-8") if i.strip()]
        
        self.total_list = set(self.anime_list+self.staff_list+self.cast_list)
        self.wdtype_dict = self.build_wdtype_dict()
        #疑问词
        self.painting_qwds = ['画风', '画面', '人物', '设定']
        self.plot_qwds = ['剧情', '主旨', '题材', '立意', '主题', '情节', '催泪', '设定']
        self.music_qwds = ['音乐', '配乐', 'BGM', 'bgm', '插曲', 'OP', 'ED']
        self.sakuga_qwds = ['作画', '打戏', '马戏', '动作', '帧数', '张数']
        self.effect_qwds = ['特效', '酷炫', '经费']
        self.casting_qwds = ['配音', '声优']
        self.tempo_qwds = ['节奏']

        print('---------words loaded----------')

        return
    
    def classify(self, question):
        data = {}
        flag = False        # 表示是否需要反问
        region_dict, selected_anime, flag = self.check_dict(question)
        set_anime = set(selected_anime)
        if not region_dict:
            return {}, {}, False    # 此处处理方式待定
        data['args'] = region_dict
        types = []
        for type_ in region_dict.values():
            types += type_
        feature_type = 'others'
        feature_types = []

        if self.check_words(self.painting_qwds, question):
            feature_type = 'painting'
            feature_types.append(feature_type)
        if self.check_words(self.plot_qwds, question):
            feature_type = 'plot'
            feature_types.append(feature_type)
        if self.check_words(self.music_qwds, question):
            feature_type = 'music'
            feature_types.append(feature_type)
        if self.check_words(self.sakuga_qwds, question):
            feature_type = 'sakuga'
            feature_types.append(feature_type)
        if self.check_words(self.effect_qwds, question):
            feature_type = 'effct'
            feature_types.append(feature_type)
        if self.check_words(self.casting_qwds, question):
            feature_type = 'casting'
            feature_types.append(feature_type)
        if self.check_words(self.tempo_qwds, question):
            feature_type = 'tempo'
            feature_types.append(feature_type)
        if feature_type == 'others':
            feature_types.append(feature_type)
        data['feature_types'] = feature_types
        return data, set_anime, flag

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.total_list:
            wd_dict[wd] = []
            if wd in self.anime_list:
                wd_dict[wd].append('anime')
            if wd in self.staff_list:
                wd_dict[wd].append('staff')
        return wd_dict
    
    def check_dict(self, question):
        txt_cut = "/".join(jieba.cut(cc.convert(question)))
        askFlag = False
        top = int(len(txt_cut)/3)
        keywords = jieba.analyse.extract_tags(question, topK=top)
        selected_anime = []
        selected_staff = []
        maybe = []
        for keyword in keywords:
            p_anime_list = process.extractOne(keyword, self.anime_list)
            p_staff_list = process.extractOne(keyword, self.staff_list)
            #print(p_anime_list)
            if p_anime_list[1] >= 70:
                maybe.append(p_anime_list[0])
                #print(p_anime_list, fuzz.partial_ratio(p_anime_list[0], question))
                if fuzz.partial_ratio(p_anime_list[0], question) > 50:
                    selected_anime.append(p_anime_list[0])
            if p_staff_list[1] >= 70:
                maybe.append(p_staff_list[0])
                if fuzz.partial_ratio(p_staff_list[0], question) > 50:
                    selected_staff.append(p_staff_list[0])
        if not (selected_anime or selected_staff):
            check = []
            # 如果需要反问则直接将待选列表maybe和askFlag返回
            askFlag = True
            '''for i in maybe:
                ask = "请问您说的是{0}吗？(是/否）\n".format(i)
                check = input(ask)
                if check=='否':
                    maybe.remove(i)'''
            selected = maybe
        else:
            selected = selected_anime+selected_staff
        region_dict = {i:self.wdtype_dict.get(i) for i in selected}
        return region_dict, selected, askFlag

    def check_words(self, wds, question):
        for wd in wds:
            if wd in question:
                return True
        return False

if __name__ == '__main__':
    handler = QClassifier()
    while True:
        question = "我喜欢银之匙"
        ret_type, set_anime = handler.classify(question)
        print(ret_type, set_anime)
        break
