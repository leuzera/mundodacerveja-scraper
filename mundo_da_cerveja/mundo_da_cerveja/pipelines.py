# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import gridfs
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class MundoDaCervejaPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )

    def open_spider(self, spider):
        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
        self.fs = gridfs.GridFS(self.db, settings['MONGODB_COLLECTION'])

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        image = open("./images/" + item['images'][0]['path'], "rb")
        item['images'][0]['image_id'] = self.fs.put(image)

        if valid:
            self.collection.insert(dict(item))

        return item

    def close_spider(self, spider):
        self.connection.close()
