#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2018/12/25 10:57 AM
# @Author : wgh0807@qq.com
# @FileName : test1.py
# @Github : https://www.github.com/wgh0807/python-test4

# [[]]

from pathlib import Path

import mysql.connector
import pandas as pd
# 抓取网易严选的商品数据
import requests as req

dataPath = (Path(__file__)).parents[1].joinpath('data')
path = dataPath
url = 'http://you.163.com/xhr/globalinfo//queryTop.json'
r = req.get(url=url)
json_data = r.json()
cateList = json_data['data']['cateList']
icon_urls = []
categories = []  # 类别集合

for cate in cateList:
    # 一集类目
    categories.append([cate['id'], cate['name']])
    for group in cate['subCateGroupList']:
        for sub in group['categoryList']:
            # 二级类目
            icon_urls.append(sub['bannerUrl'])
            categories.append([sub['id'], sub['name'], group['name'], sub['bannerUrl'].split('/')[-1], sub['frontName'],
                               str(sub['superCategoryId'])])

cate_columns = ['id', 'title', 'group', 'icon', 'desc', 'categoryId']
# 将list转存为一个csv文件
cate_pd = pd.DataFrame(categories, columns=cate_columns)
cate_pd.to_csv(path.joinpath('csv', 'categories.csv'), index=False, encoding='utf-8')

'''
id,title,group,icon,desc,categoryId
1005000,居家,,,,
'''

connection = mysql.connector.connect(
    user='java',
    password='java'
)
cursor = connection.cursor()

cursor.execute('set foreign_key_checks = 0')
cursor.execute('truncate table db_a.category')
cursor.execute('set foreign_key_checks = 1')

sql = '''
load data local infile '/Users/wangguanhua/WorkSpace/PycharmProjects/test4/data/csv/categories.csv'
into table db_a.category
fields terminated by ','
# fields terminated by '|'
ignore 1 lines
# (id, title, `group`, icon, `desc`, categoryId)
(id, title, @v_group, @v_icon, @v_desc, @v_categoryId)
set
  `group`    = nullif(@v_group, ''),
  icon       = nullif(@v_icon, ''),
  `desc`     = nullif(@v_desc, ''),
  categoryId = nullif(@v_categoryId, '');
'''
cursor.execute(sql)
connection.commit()


def download(url):
    filename = url.split('/')[-1]
    file = dataPath.joinpath('static', 'category_icons', filename)
    with open(file=str(file), mode='wb') as f:
        f.write(req.get(url).content)


for icon_url in icon_urls:
    download(icon_url)
