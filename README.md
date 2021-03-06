# Bangumi Project

Group-work Assignment of *Knowledge Graph* (B3I062220)  
By: @xinobu, @Braini-X and @Sumsky21

# 项目介绍

本项目从[bangumi](bangumi.tv)网站获取信息，构建了一个关于日本动画的知识图谱，并实现了基于该知识图谱的简单问答系统，能够完成简单的动画推荐任务。

项目文件主要包括：

1、基于动画论坛网站bangumi.tv的知识图谱构建

2、基于知识图谱的问答系统构建并封装flask API

3、“Bangumi_KG Bot”问答小程序

# 项目环境需求

python3, jieba, rapidfuzz, py2neo, OpenCC

小程序需使用[微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)进行开发和调试。

# 项目使用方式

## 命令行问答
QAmain.py文件是问答系统的入口，直接python运行即可进入交互式问答界面。

```python QAmain-old.py```

目前只支持根据动画名和动画特点的推荐，例如：

```python
python QAmain-old.py
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

## 小程序问答
![rDJrKH.png](https://s3.ax1x.com/2020/12/22/rDJrKH.png)

# 项目结构

`/KG-QA`：小程序源码

`/crawl`：爬虫部分源码

`main.py`：API入口（需要安装flask以运行API）

`QAmain.py`：问答系统总入口，接收用户输入，返回推荐

`Question_classifier.py`：对问题进行关键词提取和分类

`Question_parser.py`：对不同类问题进行分类转换，生成对应的查询语句

`Answer_searcher.py`：对知识图谱进行查询，并对返回结果进行处理

`Preprocess.py`：对知识图谱中的信息进行处理，生成领域特定字典，用于问答系统中进行匹配

`testapi.py`：本地测试API程序
