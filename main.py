from flask import Flask, jsonify, request
from QAmain import *

app = Flask(__name__)


@app.route('/api', methods=['get', 'post'])
def hello_world():
    question = request.args.get('q')
    ans = g.answer_main(question)
    return ans


if __name__ == '__main__':
    g = BangumiGraph()
    app.run(host='0.0.0.0', port=5000, debug=True)