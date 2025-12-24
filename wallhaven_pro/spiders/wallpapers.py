import scrapy
from wallhaven_pro.items import WallhavenProItem

class WallpapersSpider(scrapy.Spider):
    name = "wallpapers"
    allowed_domains = ["wallhaven.cc"]

    # 重写构造函数，接收外部参数
    def __init__(self, category='toplist', *args, **kwargs):
        """
        构造函数：接收外部传递的 category 参数
        :param category: 从 start.py 传来的榜单名称
        """
        super(WallpapersSpider, self).__init__(*args, **kwargs)
        
        # 动态构建 URL
        self.start_urls = [f"https://wallhaven.cc/{category}"]
        
        # 记录当前爬取的类别，方便调试
        self.category = category

    def parse(self, response):
        """
        第一层：解析列表页
        """
        # 打印当前正在解析的榜单
        print(f"--- 正在爬取榜单: {self.category} ---")

        # 提取所有壁纸的详情页链接
        detail_links = response.xpath('//a[@class="preview"]/@href').getall()
        
        for link in detail_links:
            # 请求详情页，进入第二层解析
            yield scrapy.Request(url=link, callback=self.parse_detail)

        # 翻页逻辑
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        """
        第二层：解析详情页，提取高清原图
        """
        item = WallhavenProItem()

        # 提取高清原图链接
        full_image_url = response.xpath('//img[@id="wallpaper"]/@src').get()
        
        # 提取壁纸 ID
        wall_id = response.xpath('//img[@id="wallpaper"]/@data-wallpaper-id').get()
        
        # 提取分辨率
        width = response.xpath('//img[@id="wallpaper"]/@data-wallpaper-width').get()
        height = response.xpath('//img[@id="wallpaper"]/@data-wallpaper-height').get()
        resolution = f"{width}x{height}" if width and height else "unknown"

        # 提取标签 (清洗数据)
        tags = response.xpath('//ul[@id="tags"]/li/a/text()').getall()

        # 装载数据
        item['wall_id'] = wall_id
        item['image_urls'] = [full_image_url]
        item['resolution'] = resolution
        item['tags'] = tags

        yield item
