import scrapy
from wallpaper_pro.items import WallpaperProItem

class WallhavenSpider(scrapy.Spider):
    name = "wallhaven"
    allowed_domains = ["wallhaven.cc"]

    custom_settings = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://wallhaven.cc/",
    }
    
    def __init__(self, category='toplist', username=None, password=None, *args, **kwargs):
        super(WallhavenSpider, self).__init__(*args, **kwargs)
        self.category_url = f"https://wallhaven.cc/{category}"
        self.username = username
        self.password = password

    def start_requests(self):
        """
        爬虫入口：判断是否有账号密码
        """
        if self.username and self.password:
            print(f"--- 准备登录用户: {self.username} ---")
            yield scrapy.Request(
                url="https://wallhaven.cc/login",
                callback=self.login_step_1
            )
        else:
            print("--- 未提供账号，以游客身份爬取 ---")
            yield scrapy.Request(url=self.category_url, callback=self.parse)

    def login_step_1(self, response):
        """
        接收登录页 HTML，自动提交表单
        """
        print("--- 正在提交登录表单 ---")
        
        yield scrapy.FormRequest.from_response(
            response,
            formid="login",
            formdata={
                'username': self.username,
                'password': self.password
            },
            callback=self.check_login_status
        )

    def check_login_status(self, response):
        """
        检查登录是否成功
        """
        if "logout" in response.text.lower() or "userpanel" in response.text.lower():
            print(f"--- 登录成功！开始爬取 {self.category_url} ---")
            
            # 登录成功后，带着 Cookie 跳转到原本想去的榜单页面
            yield scrapy.Request(url=self.category_url, callback=self.parse)
        else:
            self.logger.error("登录失败！请检查账号密码。正在尝试以游客身份继续...")
            yield scrapy.Request(url=self.category_url, callback=self.parse)

    def parse(self, response):
        """解析列表页"""
        print(f"--- 正在解析列表页: {response.url} ---")
        detail_links = response.xpath('//a[@class="preview"]/@href').getall()
        for link in detail_links:
            yield scrapy.Request(url=link, callback=self.parse_detail)

        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        """解析详情页"""
        item = WallpaperProItem()
        full_image_url = response.xpath('//img[@id="wallpaper"]/@src').get()
        wall_id = response.xpath('//img[@id="wallpaper"]/@data-wallpaper-id').get()
        width = response.xpath('//img[@id="wallpaper"]/@data-wallpaper-width').get()
        height = response.xpath('//img[@id="wallpaper"]/@data-wallpaper-height').get()
        resolution = f"{width}x{height}" if width and height else "unknown"
        tags = response.xpath('//ul[@id="tags"]/li/a/text()').getall()

        item['wall_id'] = wall_id
        item['image_urls'] = [full_image_url] if full_image_url else []
        item['resolution'] = resolution
        item['tags'] = tags
        yield item