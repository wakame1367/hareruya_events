# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HareruyaEventItem(scrapy.Item):
    """
    晴れる屋イベントの基本情報
    """
    shop = scrapy.Field()
    event_name = scrapy.Field()         
    event_date_time = scrapy.Field()    
    registration_time = scrapy.Field()  
    format = scrapy.Field()             
    capacity = scrapy.Field()           
    participation_fee = scrapy.Field()
    prize = scrapy.Field()
    remarks = scrapy.Field()
    pre_registration_info = scrapy.Field()