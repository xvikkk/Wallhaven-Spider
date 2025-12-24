# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WallhavenProItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 壁纸唯一ID
    wall_id = scrapy.Field()
    # 原始高清图链接
    image_urls = scrapy.Field()
    # 分辨率
    resolution = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # Scrapy 图片管道下载后的结果存放字段
    images = scrapy.Field()
    pass
