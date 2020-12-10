# Description: 原有的问答主程序，配合question_classifier-old可用于问答功能测试
from question_classifier_old import *
from question_parser import *
from answer_searcher import *

class BangumiGraph:
    def __init__(self):
        self.classifier = QClassifier()
        # print("classifier initiate succeessfully!")
        self.parser = QParser()
        # print("parser initiate succeessfully!")
        self.searcher = ASearcher()
        # print("searcher initiate succeessfully!")

    def answer_main(self, question):
        ans = '自己百度'
        Qtype, set_anime = self.classifier.classify(question)
        # print("classify done!")
        if not Qtype:
            return ans
        Qsql = self.parser.parser_main(Qtype)
        # print("parser done!")
        fin_ans = self.searcher.search_main(Qsql, set_anime)
        if not fin_ans:
            return ans
        else:
            return '\n'.join(fin_ans)

if __name__ == '__main__':
    g = BangumiGraph()
    quit = "不看了"
    while True:
        question = input('你都喜欢看什么冻鳗啊：')
        if(question==quit):
            break
        print("我想想啊。。。")
        ans = g.answer_main(question)
        print(ans)