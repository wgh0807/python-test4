#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2018/12/25 3:09 PM
# @Author : wgh0807@qq.com
# @FileName : product.py
# @Github : https://www.github.com/wgh0807/python-test4

# [[]]

import json
from pathlib import Path

import pandas as pd
import requests as req

link = 'http://you.163.com/xhr/globalinfo//queryTop.json'

cateList = req.get(link).json()['data']['cateList']

sup_ids = []

for cate in cateList:
    sup_ids.append(cate['id'])


def get_csv(sup_id):
    '''
    每个商品 存储为一个csv文件，方便之后多线程处理
    :param sup_id:
    :return:
    '''
    url = 'http://you.163.com/item/list?categoryId=' + str(sup_id)
    ids = []
    for line in req.get(url).iter_lines():
        line = line.decode("utf-8")
        line = str(line)
        categoryItemList = None
        if line.startswith('var json_Data='):
            line = line[line.index('=') + 1:-1]
            json_data = json.loads(line)
            # print(json_data['categoryItemList'])
            categoryItemList = json_data['categoryItemList']

            for item in categoryItemList:
                itemList = item['itemList']
                category = item['category']

                for product in itemList:
                    product_id = product['id']
                    sub_id = category['id']
                    ids.append([sup_id, sub_id, product_id])
            # print(ids)
            # sub_id
            # product_id
            # ids.append([sup_id,sub_id,product_id])

            # pandas -> csv
            columns = ['sup_id', 'sub_id', 'product_id']
            ids_pd = pd.DataFrame(ids, columns=columns)
            file = Path(__file__).parents[1].joinpath('data', 'csv', 'product', str(sup_id) + '.csv')
            ids_pd.to_csv(file, index=False)
            print('%d.csv saved.' % sup_id)

            pass


# get_csv('1005000')
for sup_id in sup_ids:
    get_csv(sup_id)

'''
csv:
sup_id, sub_id, product_id
1005000,123456,1000001

JavaEE
static/slides/sup_id/sub_id/product_id/
static/detailss/sup_id/sub_id/product_id/

'''
