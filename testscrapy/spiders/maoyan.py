# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request,Spider
from testscrapy.items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=1&offset=0']
    # base_url = 'https://maoyan.com/'

    # def start_requests(self):
    #     yield Request(url=self.base_url,callback=self.parse,dont_filter=True)

    def parse(self, response):

        movie_list = response.css(".movie-list dd")

        for movie in movie_list:
            maoyan_item = MaoyanItem()
            maoyan_item["title"] = movie.css(".movie-item-title a::text").get()
            maoyan_item["score"] = str(movie.css(".channel-detail-orange .integer::text").get()) + str(movie.css(".channel-detail-orange .fraction::text").get())
            maoyan_item["image"] = movie.css(".movie-poster img:last-of-type::attr(data-src)").get()
            yield maoyan_item
        next = response.css("ul.list-pager li:last-of-type>a::attr(href)").get()
        url = response.urljoin(next)
        yield scrapy.Request(url=url,callback=self.parse)

        # response.xpath("//div/img")