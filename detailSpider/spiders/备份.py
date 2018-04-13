# #-*- coding: utf-8 -*-
# import scrapy
# import time
# import codecs
# # import 要改为items.py中定义的类名
# from detailSpider.items import detailItem
# import dataProcessing
# import loaddata
# from bs4 import BeautifulSoup
# from scrapy.http import Request
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
#
# class spriderDemo(scrapy.spiders.Spider):
#     # -name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
#     # 命令行中 scrapy crawl + name
#     name = "spider"
#     def __init__(self):
#         self.browser = webdriver.Chrome(executable_path="D:/MyCode/Python/chromedriver.exe")
#         self.browser.set_page_load_timeout(300)
#         # self.browser.get('https://www.airbnb.com/')
#         # s1 = Select(self.browser.find_element_by_id('language-selector'))
#         # s1.select_by_index(5)
#
#     def closed(self,spider):
#         print("spider closed")
#         # self.browser.close()
#
#     def start_requests(self):
#         start_urls = []
#         # start_urls = dataProcessing.getUrl()
#         start_urls = loaddata.getUrl()
#         # start_urls.append('https://www.airbnb.com/rooms/5694880')  # 测试用5116533
#         # start_urls.append('https://www.airbnb.com/rooms/select/16046471')
#         for url in start_urls:
#             newwUrl = url + "?locale=en"
#             yield Request(url=newwUrl, callback=self.parse)
#
#
#     # 这里是分页的每个url
#     custom_settings = {
# 		'ITEM_PIPELINES' : {
#             # settings.py中BOT_NAME的名字..pipelines.JsonWithEncodingPipeline
# 			'detailSpider.pipelines.JsonWithEncodingPipeline':100,	# 开通CrawlerStorePipeline
# 			},
# 	}
#     def parse(self, response):
#         try:
#             hasSelect = True if "select" in response.url else False
#             item = detailItem()
#             item['website'] = response.url
#             if not hasSelect:
#                 # //*[@id="host-profile"]/div/div/section/div[1]/div[1]/div/div[1]
#                 item['review'] = response.xpath('//h4[@class="_vy3ibx"]'
#                                                 '/span[@class="_1vbkutid"]/span/text()').extract()[0]
#                 # 房间信息
#                 for index, site in enumerate(response.xpath('//div[@id="summary"]')):
#                     item['hometype'] = site.xpath('.//span[@class="_bt56vz6"]/span/text()').extract()[0]
#                     for i,data in enumerate(site.xpath('.//span[@class="_y8ard79"]')):
#                         if i == 0:
#                             item['guest'] = data.xpath('text()').extract()[0]
#                         elif i == 1:
#                             item['bedroom'] = data.xpath('text()').extract()[0]
#                         elif i == 2:
#                             item['bed'] = data.xpath('text()').extract()[0]
#                         elif i == 3:
#                             item['bathroom'] = data.xpath('text()').extract()[0]
#
#                 # 主人信息
#                 for index, site in enumerate(response.xpath('//div[@class="_10ejfg4u"]')):
#                     item['hostname'] = site.xpath('//h2[@class="_1xu9tpch"]/span/text()').extract()[0]
#                     if index==1:
#                         # print site.extract()
#                         item['isPlus'] = hasSelect
#                         hostdata = site.xpath('.//div[@class="_m7iebup"]')
#                         if hostdata.xpath('.//span[2]/text()').extract():
#                             location = hostdata.xpath('.//span[1]/text()').extract()[0].split(',')
#                             if len(location) == 3:
#                                 item['hostcity'] = location[0]
#                                 item['hoststate'] = location[1]
#                                 item['hostcountry'] = location[2]
#                             elif len(location) == 2:
#                                 item['hostcity'] = location[0]
#                                 item['hostcountry'] = location[1]
#                             else:
#                                 item['hostcountry'] = location[0]
#                             item['jointime'] = hostdata.xpath('.//span[2]/text()').extract()[0]
#                 # Location
#
#                 for index, site in enumerate(response.xpath('//div[@id="neighborhood"]')):
#                     if site.xpath('.//span[@class="listing-location"]'):
#                         location = site.xpath('.//span[@class="listing-location"]/a/span/text()').extract()
#                         if len(location)==2:
#                             item['city'] = item['state'] = location[0]
#                             item['country'] = location[1]
#                         else:
#                             item['city'] = location[0]
#                             item['state'] = location[1]
#                             item['country'] = location[2]
#                     elif site.xpath('.//div[@class="_ew0cqip"]'):
#                         location =  site.xpath('.//div[@class="_ew0cqip"]/text()').extract()[0].split(', ')
#                         item['city'] = location[0]
#                         item['state'] = location[1]
#                         item['country'] = location[2]
#                 item['price'] = response.xpath('//span[@class="_up0n8v6"]/span/text()').extract()[0]
#                 return item
#             else:
#                 # room data
#                 roomdiv = response.xpath('//div[@class="_9qwh472"]')
#                 room = roomdiv.xpath('.//div[@class="_g86r3e"]/span/text()').extract()
#                 item['guest'] = room[0]
#                 item['bedroom'] = room[1]
#                 item['bed'] = room[2]
#                 item['bathroom'] = room[3]
#                 item['hometype'] = response.xpath('//div[@class="_4efw5a"]/small/text()').extract()[0]
#                 # 主人信息
#                 item['isPlus'] = hasSelect
#                 hostdata = response.xpath('//div[@class="_2h22gn"]')
#                 name = hostdata.xpath('.//div[@class="_669l32"]/span/text()').extract()[0].split(" ")[2:]
#                 item['hostname'] = " ".join([i for i in name])
#                 # following-sibling::div[1]
#                 item['jointime'] = hostdata.xpath('.//div[@class="_669l32"]/following-sibling::div[1]/div[1]/text()').extract()[0]
#                 # location
#                 location = response.xpath('//div[@class="_qv0wkw1"]/text()').extract()[0].split(', ')
#                 item['address'] = location[0]
#                 item['city'] = location[1]
#                 item['state'] = location[2]
#                 item['country'] = location[3]
#
#                 reviewDiv = response.xpath('//div[@class="_33hj8bi"]')
#                 review = reviewDiv.xpath('.//div[@class="_36rlri"]/button/span/text()').extract()[0].split(" ")[2:]
#                 item['review'] = " ".join([i for i in review])
#
#                 price = response.xpath('//div[@class="_12cv0xt"]')
#                 item['price'] = price.xpath('.//span[@class="_up0n8v6"]/span/text()').extract()[0]
#
#                 # item['review'] = response.xpath('')  _33hj8bi
#
#                 return item
#         except:
#             return
#             # else:
#         #     for index, site in enumerate(response.xpath('//div[@class="_uy08umt"]')):
#         #         item['type'] = site.xpath('.//span[@class="_bt56vz6"]/span/text()').extract()[0]
#         #         print site.xpath('.//div[@class="_36rlri"]').extract()
#         #         for i, data in enumerate(site.xpath('.//span[@class="_y8ard79"]')):
#         #             if i == 0:
#         #                 item['guest'] = data.xpath('text()').extract()[0]
#         #             elif i == 1:
#         #                 item['bedroom'] = data.xpath('text()').extract()[0]
#         #             elif i == 2:
#         #                 item['bed'] = data.xpath('text()').extract()[0]
#         #             elif i == 3:
#         #                 item['bathroom'] = data.xpath('text()').extract()[0]
#         #             print data.extract()
#         # hostname = site.find_all('_1vbkutid')
#         # for i in hostname:
#         #     item['hostname'] =  i.get_text()  # //*[@id="host-profile"]/div/div/section/div[1]/div[1]/div/div[1]/div[1]/span/h2/span
#         #     print(item['hostname'])
#
#
#         #     # count += 1
#         #     # if count == 21:
#         #     #     break
#         #     # item['name'] = site.xpath('LCONTENT/text()').extract()[0]
#         #     url = site.xpath('CONTENTLINK/text()')
#         #     if url.extract():
#         #         item['url'] = url.extract()[0]
#         #         items.append(item)
#         # for item in items:
#             # 如果不是嵌套 直接 yield  item
#             # scrapy 在不同的抓取级别的Request之间传递参数的办法，
#             # 下面的范例中，parse()通过meat传递给了parse_more()参数item，
#             # 这样就可以再parse_more()抓取完成所有的数据后一次返回
#             # yield Request(item['url'],meta={'item':item}, callback=self.parse_more,dont_filter=True)
#
#
#     # def parse_more(self,response):
#     #     item = response.meta['item']
#     #     name = response.xpath('//CONTENT[1]/text()')
#     #     author = response.xpath('//LCONTENT/text()')
#     #     item['name'] = name.extract()[0]
#     #     # 判断HTML标签内容为空，跳过空的
#     #     if author.extract():
#     #         item['author'] =  author.extract()[0]
#     #     # item["url_id"] = response.xpath('//div[@class="main"]/div[@class="info"]/table[@class="table-1"]/tr[2]/td/text()').extract()[0]
#     #     # site = response.xpath('//div[@class="detail"]/div[@class="info"]/table[@class="table-1"]')
#     #     # item["url_name"] = site.xpath('tr[1]/td/text()').extract()[0]
#     #     # item['url_enterprise'] = site.xpath('tr[2]/td/a[1]/text()').extract()[0]
#     #     # item['url_function'] = site.xpath('tr[3]/td/text()').extract()[0]
#     #     # item['url_usage'] = site.xpath('tr[4]/td/text()').extract()[0]
#     #
#     #     yield item