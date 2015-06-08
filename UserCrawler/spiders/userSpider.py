# -*- coding: utf-8 -*-

__author__ = 'abstractcat'

import chardet
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy import Selector

from abstractcat.login import entry
from UserCrawler.items import UsercrawlerItem
from abstractcat.db import postgres

class UserSpider(Spider):
    '''
    Crawl user info given user id list.
    '''
    name = "user"
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def __init__(self, uid_list):
        self.uid_list = uid_list
        self.entry_manager = entry.EntryManager()
        self.db=postgres.PostgresConn()

    def start_requests(self):
        for uid in self.uid_list:

            sql='SELECT * FROM "user" WHERE uid=\'%s\' AND pid!=\'\''
            if self.db.query(sql%uid):
                continue
            print(uid)
            (uname, address, cookie) = self.entry_manager.get_random_entry()

            cookie = eval(cookie)
            url = 'http://weibo.com/u/%s' % uid
            proxy = 'http://%s' % address
            if proxy=='http://localhost':
                yield Request(url=url, cookies=cookie, callback=self.parse_user_page)
            else:
                yield Request(url=url, cookies=cookie, callback=self.parse_user_page, meta={'proxy': proxy})

    def parse_user_page(self, response):
        html = response.body

        #f=open('E:/PyCharm/CatPackages/resources/doc/user.html','w')
        #f.write(response.body)
        #f.close()

        html = html.decode('utf-8')

        sel = Selector(text=html)
        uid = sel.xpath('//script').re("\$CONFIG\['oid'\]='(\d+?)';")[0]
        pid = sel.xpath('//script').re("\$CONFIG\['page_id'\]='(\d+?)';")[0]
        name = sel.xpath('//script').re("\$CONFIG\['onick'\]='(.*?)';")[0]
        print(uid)
        print(pid)
        print(name)
        #import pdb
        #pdb.set_trace()

        #(follow_num, fan_num, post_num) = sel.xpath('//script').re("<strong.*?>(\d+)<.*?/strong>")
        #follow_num = int(follow_num)
        #fan_num = int(fan_num)
        #post_num = int(post_num)

        #verify = sel.xpath('//script').re("W_icon icon_verify_(v|club)") is not None

        yield UsercrawlerItem(uid=uid, pid=pid, name=name)
