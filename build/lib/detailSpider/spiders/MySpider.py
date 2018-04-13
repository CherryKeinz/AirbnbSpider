#-*- coding: utf-8 -*-
import scrapy
import re
import os
import json
import jsonSelect
import codecs
# import 要改为items.py中定义的类名
from detailSpider.items import detailItem
import dataProcessing
import loaddata
from scrapy.http import Request
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class spriderDemo(scrapy.spiders.Spider):
    # -name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
    # 命令行中 scrapy crawl + name
    name = "spider"
    # def __init__(self):
        # self.browser = webdriver.Chrome(executable_path="D:/MyCode/Python/chromedriver.exe")
        # self.browser.set_page_load_timeout(300)
        # self.browser.get('https://www.airbnb.com/')
        # s1 = Select(self.browser.find_element_by_id('language-selector'))
        # s1.select_by_index(5)

    def closed(self,spider):
        print("spider closed")
        # self.browser.close()

    def start_requests(self):
        start_urls = []
        # start_urls = dataProcessing.getUrl()
        # start_urls = loaddata.getUrl()  # 文件中
        # start_urls.append('https://www.airbnb.com/rooms/5694880')  # 测试用5116533
        # start_urls.append('https://www.airbnb.com/rooms/901882')

        path = 'url/'
        dir_list = os.listdir(path)
        for i in dir_list:
            with codecs.open(path + i, "r", encoding='utf-8')as file:
                for line in file.readlines():
                    # if "select" in line:
                    start_urls.append(line.strip('\n').split('?')[0])
            for url in start_urls:
                newUrl = url + "?locale=en"
                yield Request(url=newUrl,meta={'city': i}, callback=self.parse)


    # 这里是分页的每个url
    custom_settings = {
		'ITEM_PIPELINES' : {
            # settings.py中BOT_NAME的名字..pipelines.JsonWithEncodingPipeline
			'detailSpider.pipelines.JsonWithEncodingPipeline':100,	# 开通CrawlerStorePipeline
			},
	}
    def parse(self, response):
        try:
            city = response.meta['city']
            hasSelect = True if "select" in response.url else False
            item = detailItem()
            item['city'] = city
            item['website'] = response.url
            id_pattern = re.compile(r'\d+')
            item['id'] =  str(re.findall(id_pattern, str(response.url))[0])
            priceUrl = 'https://www.airbnb.com/api/v2/pdp_listing_booking_details?force_boost_unc_priority_message_type=&guests=1&listing_id='\
                       + item['id'] + '&non_refundable_policy_selected=0&show_smart_promotion=0&_format=for_web_dateless&_interaction_type=pageload' \
                                '&_intents=p3_book_it&number_of_adults=1&number_of_children=0&number_of_infants=0&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=en'

            if not hasSelect:
                regex = re.compile(r'<!--(.*)-->', re.DOTALL)
                jsonData = (response.xpath('//script[@data-hypernova-key="spaspabundlejs"]').re(regex)[0])
                encode_json = json.loads(jsonData)
                encode_json.pop('phrases')
                item['data'] = jsonSelect.select([{'json':encode_json}])

                yield Request(priceUrl, meta={'item': item}, callback=self.parse_more, dont_filter=True)
        except:
            return

    def parse_more(self, response):
        item = response.meta['item']
        encode_json = json.loads(response.body)
        item['price'] = jsonSelect.getPrice(encode_json)
        item['review_date'] = set('')
        url = 'https://www.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=en&listing_id=5694880&role=guest&_format=for_p3' \
              '&_limit=100&_offset=1&_order=language_country'
        yield Request(url, meta={'item': item,'index':1}, callback=self.parse_more_review, dont_filter=True)

    def parse_more_review(self, response):
        encode_json = json.loads(response.body)
        review_date = jsonSelect.getReviewDate(encode_json)
        item = response.meta['item']
        print review_date
        if len(review_date) is 0:
            review_date_set = item['review_date']
            item['review_date'] = ', '.join(review_date)
            yield item
        for i in review_date:
            item['review_date'].add(i)
        index = response.meta['index'] + 1
        url = 'https://www.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=en&listing_id='+ \
              item['id'] +'&role=guest&_format=for_p3' \
              '&_limit=100&_offset=' + str(index) + '&_order=language_country'

        yield Request(url, meta={'item': item, 'index': index}, callback=self.parse_more_review, dont_filter=True)

