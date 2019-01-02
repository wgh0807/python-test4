#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2018/12/26 2:20 PM
# @Author : wgh0807@qq.com
# @FileName : detail_text.py
# @Github : https://www.github.com/wgh0807/python-test4

# [[]]
'''
爬取商品详情文本信息，
存入csv文件
导入数据库product类
'''

import csv
import json
import os
import re
import time

import pandas as pd
import requests as req

from spider import *

logger = get_logger('detail_text.log')
logger.setLevel(logging.WARNING)
counter = 0


def get_detail_list(product_id):
    '''
    解析json数据
    获取相关信息
    存入csv文件

    :param product_id:
    :return:
    '''
    url = 'http://you.163.com/item/detail?id=' + str(product_id)

    for line in req.get(url).iter_lines():
        line = line.decode("utf-8")
        if line.startswith('"item":'):
            data = json.loads(line[len('"item":'):-1])
            # print(data)

            # 1. id
            id = data["id"]
            logger.debug(id)

            # 2. title
            title = data["name"]
            logger.debug(title)

            # 3. `desc`
            desc = re.sub(r'["\n]', '', data.get('simpleDesc'))
            desc = re.sub(r'[|]', ' ', desc)
            logger.debug(desc)

            # 4. coverPicture
            coverPicture = extract_filename(data['primaryPicUrl'])
            logger.debug(coverPicture)

            # 5. price
            price = data.get('retailPrice')
            logger.debug(price)

            # 6. originPrice
            originPrice = data.get('counterPrice')
            logger.debug(originPrice)

            # 7. slidePictures
            item = data['itemDetail']
            slidePictures = [
                extract_filename(item.get("picUrl1")),
                extract_filename(item.get("picUrl2")),
                extract_filename(item.get("picUrl3")),
                extract_filename(item.get("picUrl4"))
            ]
            slidePictures = json.dumps(slidePictures)  # parse python list to json array
            logger.debug(slidePictures)

            # 8. detailPictures
            detailPictures = []
            html = item.get('detailHtml')
            imgs = re.findall(r'http[a-zA-Z0-9.:/\[\]]+\.[jpegn]+g', html)
            # imgs = re.findall(r'http.+\.[jpegn]+g', html)
            for img in imgs:
                detailPictures.append(extract_filename(img))
            detailPictures = set(detailPictures)
            detailPictures = list(detailPictures)
            detailPictures = json.dumps(detailPictures)

            logger.debug(detailPictures)

            # 9. mp4
            mp4 = ''
            if item.get('videoInfo'):
                mp4 = extract_filename(item.get('videoInfo').get('mp4VideoUrl'))
            logger.debug(mp4)

            # 10. webm
            webm = ''
            if webm:
                webm = extract_filename(item.get('videoInfo').get('webmVideoUrl'))
            logger.debug(webm)

            # 11. categoryId
            categoryId = data.get('categoryList')[1].get('id')
            logger.debug(categoryId)

            global counter
            counter += 1
            logger.warning('%d - %d' % (counter, product_id))
            return [
                id,
                title,
                desc,
                coverPicture,
                price,
                originPrice,
                slidePictures,
                detailPictures,
                mp4,
                webm,
                categoryId
            ]

        # pandas -> csv
        # columns = ['id','title','`desc`','coverPicture',
        #            'price','originPrice','slidePictures','detailPictures','categoryId']
        # product_Pd = pd.DataFrame()


# logger.warning(get_detail_list(1680073))


# 拼合所有的product/csv
def get_csv():
    '''
    拼合所有的csv/product/*/csv
    读取拼合后的csv文件，
    调用get_detail_list方法
    生成detail.csv

    :return:
    '''
    # 1. list
    path = Path(__file__).parents[1].joinpath('data', 'csv', 'product')
    print(path)
    csv_list = [f for f in os.listdir(str(path))]
    df_total = pd.DataFrame()
    for csv1 in csv_list:
        # 2. read_csv1
        df = pd.read_csv(Path.joinpath(path, csv1))
        if df_total.empty:
            df_total = df
        else:
            df_total = df_total.append(df)

    # 3. to_csv
    df_total.to_csv(Path(__file__).parents[1].joinpath('data', 'csv', 'total.csv'), index=False)

    # 循环调用get_detail_list
    product_ids = pd.read_csv(Path(__file__).parents[1].joinpath('data', 'csv', 'total.csv')).get('product_id')

    detail_list = []
    for product_id in product_ids:
        detail_list.append(get_detail_list(product_id))

    columns = [
        'id',
        'title',
        'desc',
        'coverPicture',
        'price',
        'originPrice',
        'slidePictures',
        'detailPictures',
        'mp4',
        'webm',
        'categoryId'
    ]

    detail_list = pd.DataFrame(detail_list, columns=columns)
    detail_list.to_csv(Path(__file__).parents[1].joinpath('data', 'csv', 'detail.csv'),
                       index=False,
                       encoding='UTF-8',
                       sep='|',
                       quoting=csv.QUOTE_NONE,
                       quotechar="",
                       escapechar='\\'
                       )


# 循环调用gei_csv
if __name__ == '__main__':
    begin = time.time()
    get_csv()
    print('总用时：%d' % (time.time() - begin))
    # 把csv存入mysql
    pass
