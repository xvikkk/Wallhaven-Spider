# start.py
from scrapy.cmdline import execute
import sys

def run():
    print("=" * 30)
    print("   Wallhaven 爬虫启动器")
    print("=" * 30)
    print("请选择你要爬取的榜单：")
    print("1. Toplist (排行榜 - 默认)")
    print("2. Hot (热门)")
    print("3. Latest (最新)")
    print("4. Random (随机)")
    print("=" * 30)

    choice = input("请输入序号 (1-4): ").strip()

    # 建立序号到 URL 路径的映射
    category_map = {
        '1': 'toplist',
        '2': 'hot',
        '3': 'latest',
        '4': 'random'
    }

    # 获取用户选择，如果输入错误则默认 'toplist'
    target_category = category_map.get(choice, 'toplist')

    print(f"\n>>> 正在启动爬虫，目标榜单: [{target_category}] ...\n")

    # 构建 Scrapy 命令
    # 相当于在终端执行: scrapy crawl wallpapers -a category=hot
    cmd = ["scrapy", "crawl", "wallpapers", "-a", f"category={target_category}"]
    
    execute(cmd)

if __name__ == '__main__':
    run()