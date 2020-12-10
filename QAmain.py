from question_classifier import *
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

    def question_classify(self, question):
        # ask_flag为True表示需要反问
        Qtype, set_anime, ask_flag = self.classifier.classify(question)
        return Qtype, set_anime, ask_flag
        
    def continue_answer(self, Qtype, set_anime):
        ans = '自己百度'
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