import re
from urllib.parse import urlencode

import scrapy

from tlscrapy.items import FundItem


class EastmoneySpider(scrapy.Spider):
    name = "eastmoney"
    allowed_domains = ["fund.eastmoney.com"]
    start_urls = ['http://api.fund.eastmoney.com/FundTradeRank/GetRankList?']

    table_name = 'fund'

    def __init__(self):
        super().__init__()
        # 定义请求参数
        self.params = {
            'ft': 'zs',
            'sc': '1n',
            'st': 'desc',
            'pi': '1',
            'pn': '100',
            'cp': '',
            'ct': '',
            'cd': '',
            'ms': '',
            'fr': '',
            'plevel': '',
            'fst': '',
            'ftype': '',
            'fr1': '',
            'fl': '0',
            'isab': '1',
            '_': '1681892529586'
        }
        # 定义字段映射
        self.mapping = {
            0: "code",
            1: "name",
            3: "nav_date",
            4: "nav",
            5: "daily_growth",
            6: "past_1_week",
            7: "past_1_month",
            8: "past_3_months",
            9: "past_6_months",
            10: "past_1_year",
            11: "past_2_years",
            12: "past_3_years",
            13: "ytd",
            14: "inception",
            26: "fee",
            24: "min_purchase",
        }
        # 需要百分化的字段
        self.percent_fields = [
            "daily_growth", "past_1_week", "past_1_month", "past_3_months", "past_6_months",
            "past_1_year", "past_2_years", "past_3_years", "ytd", "inception"
        ]
        self.cookies = {
            'qgqp_b_id': '1b8fbbe7614e3e2605cc5c17695ab910',
            'st_si': '35217534995753',
            'st_asi': 'delete',
            'EMFUND1': 'null',
            'EMFUND2': 'null',
            'EMFUND3': 'null',
            'EMFUND4': 'null',
            'EMFUND5': 'null',
            'EMFUND6': 'null',
            'EMFUND7': 'null',
            'EMFUND8': 'null',
            'EMFUND0': 'null',
            'FundWebTradeUserInfo': 'JTdCJTIyQ3VzdG9tZXJObyUyMjolMjIlMjIsJTIyQ3VzdG9tZXJOYW1lJTIyOiUyMiUyMiwlMjJWaXBMZXZlbCUyMjolMjIlMjIsJTIyTFRva2VuJTIyOiUyMiUyMiwlMjJJc1Zpc2l0b3IlMjI6JTIyJTIyLCUyMlJpc2slMjI6JTIyJTIyLCUyMlN1cnZleURheSUyMjowJTdE',
            'EMFUND9': '04-19 16:07:55@#$%u534E%u590F%u4E2D%u8BC1%u52A8%u6F2B%u6E38%u620FETF%u8054%u63A5A@%23%24012768',
            'st_pvi': '30228126672443',
            'st_sp': '2023-04-18%2013%3A40%3A09',
            'st_inirUrl': 'https%3A%2F%2Fwww.baidu.com%2Flink',
            'st_sn': '33',
            'st_psi': '20230419161959470-111000300841-5157932343',
        }

    def start_requests(self):
        for url in self.start_urls:
            url = url + urlencode(self.params)
            yield scrapy.Request(
                url,
                headers={
                    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cache-Control': 'no-cache',
                    'Connection': 'keep-alive',
                    'Pragma': 'no-cache',
                    'Referer': 'http://fund.eastmoney.com/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                },
                cookies=self.cookies,
                callback=self.parse,
            )

    def parse(self, response, **kwargs):
        all_pages = int(re.findall(r'allPages\\":(.*?)}"', response.text)[0])
        for i in range(all_pages):
            self.params['pi'] = str(i + 1)
            url = "http://api.fund.eastmoney.com/FundTradeRank/GetRankList?" + urlencode(self.params)
            print(url)
            yield scrapy.Request(
                url=url,
                headers=response.request.headers,
                cookies=self.cookies,
                callback=self.parse_call,
                dont_filter=True,
            )

    def parse_call(self, resp):
        item = FundItem()
        data_list = re.findall(r"\[.*?\]", resp.text)
        data = re.findall(r"\"(.*?)\"", data_list[0])
        for e in data:
            fields = e.split("|")
            for idx, value in enumerate(fields):
                key = self.mapping.get(idx)
                if not key:
                    continue

                if key in self.percent_fields:
                    if value:
                        value = value + "%"
                    else:
                        value = "---"
                item[key] = value
            yield item
        pass
