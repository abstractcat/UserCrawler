# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from abstractcat.db import postgres


class UsercrawlerPipeline(object):
    def __init__(self):
        self.db = postgres.PostgresConn()

    def process_item(self, item, spider):
        sql = 'UPDATE "user" set pid=\'%s\', name=\'%s\' WHERE uid=\'%s\';'
        uid = item['uid']
        pid = item['pid']
        name = item['name']
        # follow_num = item['follow_num']
        # fan_num = item['fan_num']
        # post_num = item['post_num']
        # verify = item['verify']

        self.db.execute(sql % (pid, name, uid))
