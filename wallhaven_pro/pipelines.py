# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class WallhavenImagePipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        """发送下载请求，并将 item 传递给 meta"""
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        """
        自定义保存的文件名
        """
        # 获取 meta 中的 item
        item = request.meta['item']
        
        image_guid = item['wall_id']
        suffix = request.url.split('.')[-1] # 获取后缀
        
        filename = f"wallhaven-{image_guid}.{suffix}"
        
        return filename

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item