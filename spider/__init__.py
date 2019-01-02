#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
# @Time : 2018/12/26 3:07 PM
# @Author : wgh0807@qq.com
# @FileName : __init__.py
# @Github : https://www.github.com/wgh0807/test4

# [[]]
import logging
from pathlib import Path


def extract_filename(url):
    return url.split('/')[-1]


def get_logger(filename):
    logger = logging.getLogger(filename)

    sh = logging.StreamHandler()
    fh = logging.FileHandler(str(Path(__file__).parents[1].joinpath('data', 'log', filename)), encoding='utf-8')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(threadName)s - %(lineno)s: %(message)s')

    sh.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger
