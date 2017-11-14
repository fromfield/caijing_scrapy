# -*- coding: utf-8 -*-

#
#     雪球头条 评论/话题型文章抓取
#     by wooght 2017-10
#
import scrapy
import re
import time
from caijing_scrapy.items import TopicItem
import caijing_scrapy.providers.wfunc as wfunc

import caijing_scrapy.Db as T

#以下两项 是spider拥有链接管理和追踪功能
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class TopicsSpider(CrawlSpider):
    name = 'topics'
    allowed_domains = ['xueqiu.com']
    start_urls = [
                    'https://xueqiu.com',
                 ]
    rules = (
        #雪球头条文章
        Rule(LinkExtractor(allow=('\/\d+\/\d+',),deny=('.*\.sina.*','.*\.htm',',*\.qq.*')),callback='parse_xueqiu',follow=True,process_links='link_screen'),
        Rule(LinkExtractor(allow=('\/\d+\/column',)),callback='parse',follow=True,process_links='link_screen'),
    )
    old_link = []

    #动态修改配置内容
    custom_settings = {
        'LOG_LEVEL':'WARNING'
    }

    def __init__(self,*args,**kwargs):
        #调用父类沟站函数
        super(TopicsSpider,self).__init__(*args, **kwargs)

        #查询已经存在的地址
        s = T.select([T.topic.c.url])
        r = T.conn.execute(s)
        arr = r.fetchall()
        for one in arr:
            self.old_link.append(one[0])

    def parse_start_url(self,response):
        pass

    #地址去重/过滤
    def link_screen(self,links):
        new_links = []
        for i in links:
            if(i.url not in self.old_link):
                new_links.append(i)
                self.old_link.append(i.url)
        print('新页面:',len(new_links),'个-=-=-==-旧地址:',len(links)-len(new_links),'个')
        return new_links

    #雪球头条
    def parse_xueqiu(self,response):
        items = TopicItem()
        items['title'] = response.xpath('//title/text()').extract()[0].strip()
        thetime = response.xpath('//a[@class="time"]/@data-created_at').extract()
        if(len(thetime)<1):
            thetime = response.xpath('//a[@class="edit-time"]/@data-created_at').extract()
        # thetime = wfunc.search_time(thetime)
        items['put_time'] = thetime[0][0:10].strip()                                             #截取长度   不包括后边界
        url_re = re.search(r'.*\/(\d+)\/(\d+)$',response.url,re.I)
        items['url'] = response.url
        items['only_id'] = url_re.group(1)+url_re.group(2)
        items['body'] = response.xpath('//div[@class="article__bd__detail"]').extract()[0].strip()
        yield items