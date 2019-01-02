#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2018/12/27 1:55 PM
# @Author : wgh0807@qq.com
# @FileName : detail_static.py
# @Github : https://www.github.com/wgh0807/python-test4

# [[]]

'''

爬去商品详情静态资源
保存到本地

'''
import json
import os
import re
import threading
import time

import pandas as pd
import requests as req

from spider import *

logger = get_logger('detail_static.log')
logger.setLevel(logging.WARNING)

counter = 0


def download(file_type, sup_id, sub_id, product_id, url):
    '''
    make direction
    data/
        static/
            cover_picture/
                sup_id/sub_id/product_id/file
            slide_picture/
                sup_id/sub_id/product_id/file
    '''
    Path(__file__).parents[1].joinpath('data', 'static', file_type, sup_id, sub_id, product_id).mkdir(parents=True,
                                                                                                      exist_ok=True)
    directory = Path(__file__).parents[1].joinpath('data', 'static', file_type, sup_id, sub_id, product_id)
    filename = extract_filename(url)
    # print('download start')
    try:
        if os.path.exists(os.path.join(str(directory), filename)):
            logger.warning('%s exists, pass ' % filename)

        else:
            with open(str(Path.joinpath(directory, filename)), mode='wb') as f:
                f.write(req.get(url).content)
                logger.warning('%s download finish ' % filename)
    except:
        logger.exception('download error ! product_id = %s, url = %s ' % (str(product_id), url))

    pass


def parse(sup_id, sub_id, product_id):
    '''
    解析json数据
    获取资源信息
    下载资源文件
    :param sup_id:
    :param sub_id:
    :param product_id:
    :return:
    '''
    url = 'http://you.163.com/item/detail?id=' + str(product_id)
    # print(url)

    for line in req.get(url).iter_lines():
        line = line.decode('utf-8')
        # print(line)

        if line.startswith('"item":'):
            data = json.loads(line[len('"item":'):-1])
            global counter
            counter = counter + 1
            logger.warning('%d - %s ' % (counter, product_id))

            # 1. coverPicture
            coverPicture_url = data['primaryPicUrl']
            # logger.debug(coverPicture)
            download('cover_picture', sup_id, sub_id, product_id, coverPicture_url)

            # 2. slidePictures
            item = data['itemDetail']
            slidePictures = [
                item.get("picUrl1"),
                item.get("picUrl2"),
                item.get("picUrl3"),
                item.get("picUrl4")
            ]
            for spic in slidePictures:
                if spic:
                    download('slide_pictures', sup_id, sub_id, product_id, spic)

            # slidePictures = json.dumps(slidePictures)  # parse python list to json array
            # logger.debug(slidePictures)

            # 3. detailPictures
            html = item.get('detailHtml')
            imgs = re.findall(r'http[a-zA-Z0-9.:/\[\]]+\.[jpegn]+g', html)
            # imgs = re.findall(r'http.+\.[jpegn]+g', html)
            imgs = set(imgs)
            imgs = list(imgs)
            for img in imgs:
                # detailPictures.append(extract_filename(img))
                download('detail_pictures', sup_id, sub_id, product_id, img)

            # 4. mp4
            mp4 = ''
            if item.get('videoInfo'):
                mp4 = item.get('videoInfo').get('mp4VideoUrl')
                if mp4:
                    download('mp4', sup_id, sub_id, product_id, mp4)
                pass

            # 5. webm
            webm = ''
            if item.get('videoInfo'):
                webm = item.get('videoInfo').get('webmVideoUrl')
                if webm:
                    download('webm', sup_id, sub_id, product_id, webm)

            logger.warning('%s finish' % product_id)
            pass


def download_single_csv(csv):
    '''
    下载一个csv中所有的资源
    '''
    data = pd.read_csv(Path(__file__).parents[1].joinpath('data', 'csv', 'product', csv))
    for i in data.values:
        sup_id = str(i[0])
        sub_id = str(i[1])
        product_id = str(i[2])
        parse(sup_id, sub_id, product_id)


def multiple_threading_download():
    '''
    多线程下载
    每个线程下载一个csv文件
    :return:
    '''
    path = Path(__file__).parents[1].joinpath('data', 'csv', 'product')
    csv_list = [f for f in os.listdir(str(path))]
    threads = []
    for csv1 in csv_list:
        thread = threading.Thread(
            target=download_single_csv,
            args=(csv1,)
        )
        threads.append(thread)
        pass
    print('thread build success')
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start_time = time.time()
    multiple_threading_download()
    logger.warning('total time %d' % (time.time() - start_time))
