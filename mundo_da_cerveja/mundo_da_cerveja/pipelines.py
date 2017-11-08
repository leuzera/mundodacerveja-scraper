# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import gridfs
import logging
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
        if not item['images']:
            raise DropItem("{0} sem imagem!".format(item['name']))

        image_path = settings['IMAGES_STORE']
        image = open(image_path + item['images'][0]['path'], "rb")
        image_id = self.fs.put(image)

        self.collection.update({'url': item['images'][0]['url']},
                               {'name': item['name'],
                                'image': image_id,
                                'url': item['images'][0]['url']},
                               upsert=True)

        logging.info('{} salva no MongoDB'.format(item['name']))
        return item

    def close_spider(self, spider):
        self.connection.close()
