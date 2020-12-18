# Bangumi Project

Assignment of Knowledge Graph (B3I062220)

# 项目介绍

本项目从bangumi网站获取信息，构建了一个关于日本动画的知识图谱，并实现了基于该知识图谱的简单问答系统，能够完成简单的动画推荐任务。

项目文件主要包括：

1、基于动画论坛网站bangumi.tv的知识图谱构建

2、基于知识图谱的问答系统构建

# 项目环境需求

python3, jieba, fuzzywuzzy, py2neo, OpenCC, collections

# 项目使用方式

QAmain.py文件是问答系统的入口，直接python运行即可进入交互式问答界面。

```python QAmain.py```

目前只支持根据动画名和动画特点的推荐，例如：

```python
python QAmain.py
Building prefix dict from the default dictionary ...
Loading model from cache /var/folders/25/18x6nkyn7g115gdsjybdg3rr0000gp/T/jieba.cache
Loading model cost 0.988 seconds.
Prefix dict has been built successfully.
---------words loaded----------
你都喜欢看什么冻鳗啊：我喜欢三月的狮子这种剧情向的
我想想啊。。。
我推荐的类似剧情的动画有：蜂蜜与四叶草、3月的狮子 第二季、蜂蜜与四叶草II
你都喜欢看什么冻鳗啊：那有没有像灵能百分百这样作画特别炫酷的呢
我想想啊。。。
我推荐的作画也很爆炸的动画有：AMON 恶魔人默示录、星际牛仔、血界战线 王者餐厅的王者、老人Z、巴哈姆特之怒 GENESIS、Daicon4 开幕动画、东京喰种 JACK
```

# 项目结构

QAmain.py：问答系统总入口，接收用户输入，返回推荐

Question_classifier.py：对问题进行关键词提取和分类

Question_parser.py：对不同类问题进行分类转换，生成对应的查询语句

Answer_searcher.py：对知识图谱进行查询，并对返回结果进行处理

Preprocess.py：对知识图谱中的信息进行处理，生成领域特定字典，用于问答系统中进行匹配

# testapi.py本地测试接口
* 运行main.py，观察到控制台出现如下输出，代表flask应用在本地启动成功：
  ```
  ...
   * Debugger is active!
   * Debugger PIN: 283-755-850
   * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
  ```
* 新开一个终端，修改testapi.py中发送的数据，运行testapi.py，等待控制台输出结果
* 如果testapi.py终端报错，可以前往运行main.py的终端，查看接口端的报错信息和位置
