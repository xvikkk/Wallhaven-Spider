import scrapy
from wallpaper_pro.items import WallpaperProItem
import re

class NetbianSpider(scrapy.Spider):
    name = "netbian"
    allowed_domains = ["pic.netbian.com"]
    
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://pic.netbian.com/", 
        }
    }

    def __init__(self, category='index', *args, **kwargs):
        """
        category 参数映射：
        index -> 首页
        4kdongman -> 动漫
        4kfengjing -> 风景
        4kmeinv -> 美女
        4kyouxi -> 游戏
        """
        super(NetbianSpider, self).__init__(*args, **kwargs)
        if category == 'index':
            self.start_urls = ["https://pic.netbian.com/"]
        else:
            self.start_urls = [f"https://pic.netbian.com/{category}/"]

    def parse(self, response):
        """解析列表页"""
        print(f"--- 正在爬取 Netbian: {response.url} ---")
        
        # 提取详情页链接
        detail_links = response.xpath('//div[@class="slist"]//a/@href').getall()
        
        for link in detail_links:
            # 过滤掉非详情页链接
            if "/tupian/" in link:
                # 拼接完整 URL
                full_url = response.urljoin(link)
                yield scrapy.Request(url=full_url, callback=self.parse_detail)

        # 翻页逻辑
        next_page_href = response.xpath('//div[@class="page"]/a[contains(text(), "下一页") or contains(text(), ">")]/@href').get()
        if next_page_href:
            yield response.follow(next_page_href, callback=self.parse)

    def parse_detail(self, response):
        """解析详情页"""
        item = WallhavenProItem()

        # 提取 ID
        try:
            wall_id = re.search(r'(\d+)\.html', response.url).group(1)
            # 防止和 Wallhaven ID 冲突
            item['wall_id'] = f"netbian-{wall_id}"
        except:
            item['wall_id'] = f"netbian-unknown"

        # 提取高清大图
        img_url_suffix = response.xpath('//div[@class="photo-pic"]//img/@data-pic').get()
        if not img_url_suffix:
            img_url_suffix = response.xpath('//div[@class="photo-pic"]//img/@src').get()
        
        if img_url_suffix:
            item['image_urls'] = [response.urljoin(img_url_suffix)]
        else:
            return # 没有图片则放弃该 Item

        # 提取分辨率
        resolution = response.xpath('//div[@class="infor"]/p[contains(text(), "尺寸")]/span/text()').get()
        item['resolution'] = resolution if resolution else "unknown"

        # 提取标签
        tags = response.xpath('//div[@class="photo-tags"]/a/text()').getall()
        item['tags'] = tags

        yield item