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
    def process_item(self, item, spider):
        if '.' in item['file_name']:
            file_name = item['file_name'].split('.')[0]
        with open(file_name + '.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['website', 'hometype', 'price', 'city', 'state', 'country', 'bedroom', 'bed', 'guest'
                                   , 'bathroom', 'review', 'review_date', 'hostname', 'jointime'])

            row = [item['website'],item['home']['hometype'],item['price'],item['location']['city'],
                   item['location']['state'],item['location']['country'],item['home']['bedroom'],
                   item['home']['bed'],item['home']['guest'],item['home']['bathroom'],item['home']['review'],
                   '',item['host']['hostname'],item['host']['jointime']]
            csvwriter.writerow(row)

        return item
