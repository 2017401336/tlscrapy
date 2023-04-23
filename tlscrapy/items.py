# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TlscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FundItem(scrapy.Item):
    # 基金代码
    code = scrapy.Field()
    # 基金名称
    name = scrapy.Field()
    # 单位净值
    nav = scrapy.Field()
    # 单位净值日期
    nav_date = scrapy.Field()
    # 日增长率
    daily_growth = scrapy.Field()
    # 近1周收益率
    past_1_week = scrapy.Field()
    # 近1月收益率
    past_1_month = scrapy.Field()
    # 近3月收益率
    past_3_months = scrapy.Field()
    # 近6月收益率
    past_6_months = scrapy.Field()
    # 近1年收益率
    past_1_year = scrapy.Field()
    # 近2年收益率
    past_2_years = scrapy.Field()
    # 近3年收益率
    past_3_years = scrapy.Field()
    # 今年以来收益率
    ytd = scrapy.Field()
    # 成立来收益率
    inception = scrapy.Field()
    # 手续费
    fee = scrapy.Field()
    # 起购金额
    min_purchase = scrapy.Field()
