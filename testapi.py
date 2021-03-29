# 用于测试flaskAPI接口
import requests
import json
import time

data = {
    "task": 0,
    "q": '我喜欢jojo，它的画风很棒！'
    # 'qtype': {'args': {'JOJO的奇妙冒险 星尘斗士 埃及篇': ['anime'], 'Joao': ['staff']}, 'feature_types': ['others']},
    # 'anime_list': ['JOJO的奇妙冒险 星尘斗士 埃及篇']
}
r = requests.post(
    url='https://sumsky.top:5000/api',
    json=data
)
print(json.loads(r.text))   # 响应内容
print(r.elapsed.total_seconds())    # 响应时间