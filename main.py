from flask import Flask, jsonify, request
from QAmain import *
import json
from logging.handlers import RotatingFileHandler
import logging
import time
import os

app = Flask(__name__)
g = BangumiGraph()

'''handler = RotatingFileHandler(os.path.join(app.root_path, 'logs', 'error_log.log'), maxBytes=102400, backupCount=10)
logging_format = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

handler.setFormatter(logging_format)
app.logger.addHandler(handler)'''

@app.route('/api', methods=['get', 'post'])
def hello_world():
    '''
    task=0：用户正常提问；
            先进行问题分类，根据statue判断是否需要反问
                statue=true: 返回待选列表和qtype，response_type为1
                statue=false: 不需要反问，直接进入continue_answer
    task=1：反问并选择后回答；
            正常返回答案的response_type为0
    '''
    r = json.loads(request.get_json())      # 本地测试需要在表达式右侧外面套一层json.loads()
    task = r["task"]
    if task == 0:
        question = r["q"]
        qtype, choosen, statue = g.question_classify(question)
        if statue:      # 代表需要反问
            response = {'rtype': 1, 'qtype': qtype, 'anime_set': list(choosen)}
            return jsonify(response)
    else:
        qtype = r["qtype"]
        choosen = set(r["anime_list"])
    ans = g.continue_answer(qtype, choosen)
    response = {'rtype': 0, 'answer': ans}
    return jsonify(response)

@app.route('/api/seeErrorlog', methods=['get', 'post'])
def printErrorlog():
    return send_from_directory('./logs', 'error_log.log', as_attachment=True)

'''@app.errorhandler(500)
def special_exception_handler(error):
    app.logger.error(error)
    return '500 error', 500'''


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)