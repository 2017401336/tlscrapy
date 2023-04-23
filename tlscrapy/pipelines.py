import pymysql


class FundPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_settings=crawler.settings.get('MYSQL_INFO')
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(**self.db_settings)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def process_item(self, item, spider):
        keys = item.keys()
        fields_template = ', '.join(keys)
        values_template = ', '.join(['%s'] * len(keys))
        sql = f"INSERT INTO {spider.table_name} ({fields_template}) VALUES ({values_template})"
        values = tuple(item[key] for key in keys)
        self.cursor.execute(sql, values)
        self.conn.commit()
        return item
