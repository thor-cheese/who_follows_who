# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem

from nft_chads.models import db_connect, create_table, NftChadsFollows, NftChads
from nft_chads.items import NftChadsItem, NftChadsFollowsItem


import logging

class NftChadsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        print('create_table')
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):

        """Save quotes in the database
        This method is called for every item pipeline component
        """

        # print(type(item).__name__)
        # print(item)
        if type(item).__name__ == 'NftChadsItem':

            nft_chads = NftChads()

            nft_chads.parent_nft_account_id= item['parent_nft_account_id']
            nft_chads.created_at = item['created_at']
            nft_chads.description= item['description']
            nft_chads.entities= item['entities']
            nft_chads.twitter_id= item['twitter_id']
            nft_chads.location= item['location']
            nft_chads.name= item['name']
            nft_chads.pinned_tweet_id= item['pinned_tweet_id']
            # nft_chads.profile_image_url= item['profile_image_url']
            nft_chads.protected= item['protected']
            nft_chads.followers_count= item['followers_count']
            nft_chads.following_count= item['following_count']
            nft_chads.tweet_count= item['tweet_count']
            nft_chads.listed_count= item['listed_count']
            # nft_chads.url= item['url']
            nft_chads.screen_name= item['screen_name']
            nft_chads.verified= item['verified']
            # nft_chads.withheld= item['nft_chads']

            return self.save_item(nft_chads)

        elif type(item).__name__ == 'NftChadsFollowsItem':
            print('got NftChadsFollowsItem')
            nft_chads_follows = NftChadsFollows()
            nft_chads_follows.parent_nft_chad_id =item['parent_nft_chad_id']
            nft_chads_follows.created_at = item['created_at']
            nft_chads_follows.description= item['description']
            nft_chads_follows.entities= item['entities']
            nft_chads_follows.twitter_id= item['twitter_id']
            nft_chads_follows.location= item['location']
            nft_chads_follows.name= item['name']
            nft_chads_follows.pinned_tweet_id= item['pinned_tweet_id']
            # nft_chads_follows.profile_image_url= item['profile_image_url']
            nft_chads_follows.protected= item['protected']
            nft_chads_follows.followers_count= item['followers_count']
            nft_chads_follows.following_count= item['following_count']
            nft_chads_follows.tweet_count= item['tweet_count']
            nft_chads_follows.listed_count= item['listed_count']
            # nft_chads_follows.url= item['url']
            nft_chads_follows.screen_name= item['screen_name']
            nft_chads_follows.verified= item['verified']
            # nft_chads_follows.withheld= item['nft_chads']

            return self.save_item(nft_chads_follows)


    def save_item(self, data):

        session = self.Session()

        try:
            session.add(data)

            session.commit()


        except:
            session.rollback()
            raise

        finally:
            session.close()

        # return item
