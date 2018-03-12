# -*- coding: utf-8 -*-
import scrapy
from tmshop.items import TmshopItem

class TmspiderSpider(scrapy.Spider):
    name = 'tmspider'
    allowed_domains = ['tmall.com']
    start_urls = ['https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.4.3a655c21LhJx6R&q=%C5%AE%D7%B0&sort=d&style=g&from=mallfp..pc_1_searchbutton&active=2#J_Filter']

    count = 0



    def parse(self, response):
        TmspiderSpider.count +=1



        divs = response.xpath("//div[@id='J_ItemList']/div[@class='product']/div")
        if not divs:
            self.log("List Page error --%s"%response.url)
        for div in divs:
            item = TmshopItem()
            item['goods_name'] = response.xpath('//*[@id="J_ItemList"]/div[1]/div/p[1]/em').extract()
            item['goods_url'] = response.xpath('//*[@id="J_ItemList"]/div[1]/div/p[1]/em').extract()
            item['goods_pirce'] = response.xpath('//*[@id="J_ItemList"]/div[1]/div/p[1]/em').extract()

            yield scrapy.Request(url=item['goods_url'],meta={'item':item},callback=self.parse_detail(),
                                 dont_filter=True)

    def parse_detail(self,response):
        div = response.xpath('')
        if not div:
            self.log("List Page error --%s"%response.url)

            #通过response接收转过来的数据

        item = response.meta['item']

        div=div[0]

        item['goods_pirce'] = response.xpath('//*[@id="J_ItemList"]/div[1]/div/p[1]/em').extract()
        item['goods_pirce'] = response.xpath('//*[@id="J_ItemList"]/div[1]/div/p[1]/em').extract()
        item['goods_pirce'] = response.xpath('//*[@id="J_ItemList"]/div[1]/div/p[1]/em').extract()

        yield item