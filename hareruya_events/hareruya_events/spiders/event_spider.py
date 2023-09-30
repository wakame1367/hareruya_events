import scrapy
from enum import Enum
from datetime import datetime
from hareruya_events.items import HareruyaEventItem
from urllib.parse import urlencode, urlunparse


class Shop(Enum):
    Kichijoji = "17"

    @property
    def name(self):
        return self.name.lower()

    @property
    def code(self):
        return self.value



class EventSpider(scrapy.Spider):
    name = 'event'
    http_schema = "https"
    netloc = "www.hareruyamtg.com"
    event_path = "/ja/events"
    fragment = ""
    base_url = "https://www.hareruyamtg.com/ja/events"
    start_urls = [base_url]

    def start_requests(self):
        # 晴れる屋のイベントは当月もののみしか掲載しない
        now = datetime.now()
        year_month = now.strftime('%Y%m')

        for shop in Shop:
            year_month = f'{year}{month:02d}'
            params = {
                "shop": f"{shop.code}" ,
                "date": year_month,
            }
            query = urlencode(params)
            # 例: https://www.hareruyamtg.com/ja/events/?shop=17&date=202310
            url = urlunparse((self.http_schema, self.netloc, self.path, '', query, self.fragment))
            # 生成したURLでリクエストを作成
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 各イベントの詳細ページへのリンクを取得
        event_links = response.xpath('XPATH_FOR_EVENT_LINKS').extract()

        for link in event_links:
            # 各イベントの詳細ページにリクエストを送る
            yield scrapy.Request(url=link, callback=self.parse_event_detail)

    def parse_event_detail(self, response):
        item = HareruyaEventItem()
        item['shop'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[1]/div[2]').get()
        item['event_name'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[2]/div[2]').get()
        item["event_date_time"] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[2]/div[2]').get()
        item['registration_time'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[3]/div[2]').get()
        item['format'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[5]/div[2]').get()
        item['capacity'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[6]/div[2]').get()
        item['participation_fee'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[7]/div[2]').get()
        item['prize'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[8]/div[2]').get()
        item['remarks'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[9]/div[2]').get()
        # item['pre_registration_info'] = response.xpath('//*[@id="main_middle"]/div/div/div[1]/ul/li[2]/div[2]').get()

        yield item
