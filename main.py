from scrapy.cmdline import execute
import os
import sys


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'eastmoney'])
    # execute('scrapy crawl st_crawl_spider -a source=console -a app_ids=["1-1641486558"]'.split(' '))
    # print(IosInfoService.exists(1))