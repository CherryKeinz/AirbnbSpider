# -*- coding: utf-8 -*-
import codecs
from scrapy.exporters import JsonItemExporter
import csv
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 使用内置JsonItemExporter
class JsonWithEncodingPipeline(object):
    # 调用scrapy提供的json export导出json文件
    def __init__(self):
        #打开一个json文件
        self.file = codecs.open('result/1.json', 'w+', encoding='utf-8')
        #创建一个exporter实例,入参分别是下面三个，类似前面的自定义导出json
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        #开始导出
        self.exporter.start_exporting()
    def close_spider(self,spider):
        #完成导出
        self.exporter.finish_exporting()
        #关闭文件
        self.file.close()
    #最后也需要调用process_item返回item
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class Pipeline_ToCSV(object):

    def __init__(self):
        # csv文件的位置,无需事先创建
        # store_file = os.path.dirname(__file__) + '/spiders/qtw.csv'
        # # 打开(创建)文件
        # self.file = open(store_file, 'wb')
        self.file = codecs.open('demo.csv', 'wb', encoding='utf-8')
        # csv写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        if item['image_name']:
            self.writer.writerow((item['image_name'].encode('utf8', 'ignore'), item['image_urls']))
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()