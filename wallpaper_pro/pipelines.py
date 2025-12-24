# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class wallpaperImagePipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        """发送下载请求，并将 item 传递给 meta"""
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        image_guid = item['wall_id']
        
        # 动态获取后缀
        url = request.url
        suffix = url.split('.')[-1]
        # 清洗后缀，防止带参数
        if "?" in suffix:
            suffix = suffix.split('?')[0]

        if "netbian" not in image_guid:
             filename = f"wallhaven-{image_guid}.{suffix}"
        else:
             filename = f"{image_guid}.{suffix}"
        
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item