# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime


class NftChadsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parent_nft_account_id = scrapy.Field()
    created_at = scrapy.Field()
    description = scrapy.Field()
    entities = scrapy.Field() ## this is new
    twitter_id = scrapy.Field()
    location = scrapy.Field()
    name = scrapy.Field()
    pinned_tweet_id= scrapy.Field() ## this is new
    profile_image_url= scrapy.Field() ## this is new
    protected = scrapy.Field()
    # public_metrics = scrapy.Field() ## this is new
    followers_count = scrapy.Field()
    following_count = scrapy.Field()## this is new
    tweet_count = scrapy.Field()
    listed_count = scrapy.Field()
    url = scrapy.Field()
    screen_name = scrapy.Field()
    verified= scrapy.Field()
    withheld= scrapy.Field()## this is new




class NftChadsFollowsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    parent_nft_chad_id = scrapy.Field()
    description = scrapy.Field()
    created_at = scrapy.Field()
    entities = scrapy.Field() ## this is new
    twitter_id = scrapy.Field()
    location = scrapy.Field()
    name = scrapy.Field()
    pinned_tweet_id= scrapy.Field() ## this is new
    profile_image_url= scrapy.Field() ## this is new
    protected = scrapy.Field()
    # public_metrics = scrapy.Field() ## this is new
    followers_count = scrapy.Field()
    following_count = scrapy.Field()## this is new
    tweet_count = scrapy.Field()## this is new
    listed_count = scrapy.Field()
    url = scrapy.Field()
    screen_name = scrapy.Field()
    verified= scrapy.Field()
    withheld= scrapy.Field()## this is new
