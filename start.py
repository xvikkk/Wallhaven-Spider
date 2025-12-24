# start.py
from scrapy.cmdline import execute
import getpass  # 用于隐藏密码输入

def run():
    print("=" * 30)
    print("   Wallhaven 爬虫启动器")
    print("=" * 30)
    
    # 1. 选择榜单
    print("请选择你要爬取的榜单：")
    print("1. Toplist (排行榜)")
    print("2. Hot (热门)")
    print("3. Latest (最新)")
    print("4. Random (随机)")
    category_map = {'1': 'toplist', '2': 'hot', '3': 'latest', '4': 'random'}
    choice = input("请输入序号 (1-4): ").strip()
    target_category = category_map.get(choice, 'toplist')

    # 2. 登录选项
    print("-" * 30)
    need_login = input("是否需要登录? (y/n): ").strip().lower()
    
    username = ""
    password = ""
    
    if need_login == 'y':
        username = input("请输入用户名: ")
        # 如果报错改成 input()
        try:
            password = getpass.getpass("请输入密码: ")
        except:
            password = input("请输入密码: ")

    print(f"\n>>> 正在启动爬虫，目标: [{target_category}] ...\n")

    # 构建命令
    cmd = ["scrapy", "crawl", "wallpapers", "-a", f"category={target_category}"]
    
    # 如果用户输入了账号，则追加参数
    if username and password:
        cmd.extend(["-a", f"username={username}", "-a", f"password={password}"])
    
    execute(cmd)

if __name__ == '__main__':
    run()