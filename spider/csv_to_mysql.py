#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2019/1/2 4:18 PM
# @Author : wgh0807@qq.com
# @FileName : csv_to_mysql.py
# @Github : https://www.github.com/wgh0807/python-test4

import mysql.connector
from pathlib import Path

connection = mysql.connector.connect(
    user='root',
    password='960807'
)
cursor = connection.cursor()
dataPath = Path(__file__).parents[1].joinpath('data', 'csv')


def category_csv_to_mysql():
    cursor.execute('set foreign_key_checks = 0;')
    cursor.execute('truncate table db_a.category;')
    cursor.execute('set foreign_key_checks = 1;')
    sql = '''
load data local infile '/Users/wangguanhua/WorkSpace/PycharmProjects/python-test4/data/csv/categories.csv'
into table db_a.category
character set utf8
fields terminated by ','
ignore 1 lines
(id, title, @v_group, @v_icon, @v_desc, @v_categoryId)
set
  `group` = nullif(@v_group, ''),
  icon    = nullif(@v_icon, ''),
  `desc`  = nullif(@v_desc, ''),
  categoryId = nullif(@v_categoryId,'');
'''
    cursor.execute(sql)
    connection.commit()
    print('categories.csv import success')


def product_csv_to_mysql():
    cursor.execute('set foreign_key_checks = 0;')
    cursor.execute('truncate table db_a.product;')
    cursor.execute('set foreign_key_checks = 1;')
    sql = '''
load data local infile '/Users/wangguanhua/WorkSpace/PycharmProjects/python-test4/data/csv/detail.csv'
into table db_a.product
character set utf8
fields terminated by '|'
ignore 1 lines
(productId, title, @v_desc, @v_coverPicture, @v_price, @v_originPrice, @v_slidePictures, @v_detailPictures, @v_mp4, @v_webm, categoryId)
set
  `desc`         = nullif(@v_desc, ''),
  coverPicture   = nullif(@v_coverPicture, ''),
  price          = nullif(@v_price, 0.00),
  originalPrice  = nullif(@v_originPrice, 0.00),
  slidePictures  = nullif(@v_slidePictures, ''),
  detailPictures = nullif(@v_detailPictures,''),
  mp4            = nullif(@v_mp4, ''),
  webm           = nullif(@v_webm, '');
'''
    cursor.execute(sql)
    connection.commit()
    print('detail.csv import success')


category_csv_to_mysql()
product_csv_to_mysql()
