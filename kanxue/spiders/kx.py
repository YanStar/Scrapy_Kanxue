# -*- coding: utf-8 -*-
import scrapy
from kanxue.items import KanxueItem
from scrapy.http import Request,FormRequest
import scrapy.exceptions

class KxSpider(scrapy.Spider):
    name = 'kx'
    allowed_domains = ['bbs.pediy.com']
    start_urls = ['http://bbs.pediy.com/']
    start_url = 'http://bbs.pediy.com/'

    def parse(self, response):  #获取首页所有版块链接
        try:
            urls = response.xpath('//a[@class="font-weight-bold"]/@href').extract()
            for i in range (0,len(urls)):
                last_url = self.start_url+urls[i]
                forum_num = urls[i].split('.')[0]
                yield FormRequest(url=last_url,meta={'forum_num':forum_num},callback=self.Every_Link)
        except scrapy.exceptions as e:
            print(e.reason)

    def Every_Link(self,response):    #获取版块下所有页数链接
        try:
            hrefs = response.xpath('//li[@class="page-item"]/a/@href').extract()[-2]
            forum_num = response.meta["forum_num"]
            max_num = hrefs.split('.')[0]
            max_num_last = max_num.split('-')[2]
            for i in range(1,int(max_num_last)):
                url = self.start_url+str(forum_num)+'-'+str(i)+'.htm?orderby=lastpid&digest=0'
                yield FormRequest(url=url,callback=self.Need_Data)
        except scrapy.exceptions as e:
            print(e.reason)

    def Need_Data(self,response):    #爬取所需的文章标题和对应链接
        try:
            item = KanxueItem()
            url_first = response.xpath('//div[@class="subject"]/a[@target="_blank"]/@href').extract()
            for i in range(0,len(url_first)):
                item['url'] = self.start_url+url_first[i]
                item['title'] = response.xpath('//a[@href="'+url_first[i]+'"]/text()').extract()[2]
                yield item
        except scrapy.exceptions as e:
            print(e.reason)