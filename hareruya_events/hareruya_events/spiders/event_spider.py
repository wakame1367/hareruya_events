import scrapy
from hareruya_events.items import HareruyaEventItem

class EventSpider(scrapy.Spider):
    name = 'event'
    start_urls = ['https://www.hareruyamtg.com/ja/events']

    def parse(self, response):
        # 各イベントの詳細ページへのリンクを取得
        event_links = response.xpath('XPATH_FOR_EVENT_LINKS').extract()

        for link in event_links:
            # 各イベントの詳細ページにリクエストを送る
            yield scrapy.Request(url=link, callback=self.parse_event_detail)

    def parse_event_detail(self, response):
        item = HareruyaEventItem()
        item['shop'] = response.xpath('XPATH_FOR_SHOP').get()
        item['event_name'] = response.xpath('XPATH_FOR_EVENT_NAME').get()
        # ... 他のデータも同様に取得 ...

        yield item
