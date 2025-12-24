from scrapy.cmdline import execute
import getpass
import sys

def run():
    # 第一层菜单：选择数据源
    print("请选择数据源:")
    print("1. Wallhaven")
    print("2. Netbian")
    site_choice = input("请输入数据源序号 (1-2): ").strip()

    cmd = []

    # 分支逻辑
    if site_choice == '2':
        # Netbian 逻辑
        print("\n[已选择彼岸图网]")
        print("请选择分类:")
        print("1. 动漫 (4kdongman)")
        print("2. 游戏 (4kyouxi)")
        print("3. 风景 (4kfengjing)")
        print("4. 美女 (4kmeinv)")
        print("5. 首页 (最新)")
        
        nb_map = {'1': '4kdongman', '2': '4kyouxi', '3': '4kfengjing', '4': '4kmeinv', '5': 'index'}
        choice = input("请输入分类序号: ").strip()
        category = nb_map.get(choice, 'index')
        
        print(f"\n>>> 正在启动 Netbian 爬虫，目标: [{category}] ...\n")
        cmd = ["scrapy", "crawl", "netbian", "-a", f"category={category}"]

    else:
        # Wallhaven 逻辑（默认）
        print("\n[已选择 Wallhaven]")
        print("请选择榜单:")
        print("1. Toplist (排行榜)")
        print("2. Hot (热门)")
        print("3. Latest (最新)")
        print("4. Random (随机)")
        wh_map = {'1': 'toplist', '2': 'hot', '3': 'latest', '4': 'random'}
        choice = input("请输入序号: ").strip()
        category = wh_map.get(choice, 'toplist')

        # 登录询问
        need_login = input("是否需要登录? (y/n): ").strip().lower()
        username, password = "", ""
        if need_login == 'y':
            username = input("用户名: ")
            try:
                password = getpass.getpass("密码: ")
            except:
                password = input("密码: ")
        
        print(f"\n>>> 正在启动 Wallhaven 爬虫，目标: [{category}] ...\n")
        cmd = ["scrapy", "crawl", "wallhaven", "-a", f"category={category}"]
        if username and password:
            cmd.extend(["-a", f"username={username}", "-a", f"password={password}"])

    # 执行最终构建的命令
    execute(cmd)

if __name__ == '__main__':
    run()