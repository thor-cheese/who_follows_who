# testing
 # http://localhost:8888/notebooks/Twitter%20scrape/Untitled.ipynb?kernel_name=python3
 # http://localhost:8888/notebooks/Twitter%20scrape/NFT%20Chads%20.ipynb#
import scrapy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from scrapy.loader import ItemLoader
from nft_chads.items import NftChadsItem, NftChadsFollowsItem
import numpy as np
import math
import json
import requests

from nft_chads.models import db_connect, create_table, NftChadsFollowsT, NftChads


class NftChadsSpider(scrapy.Spider):
    name = 'nft_chads'
    header_data = {'Authorization':'Bearer AAAAAAAAAAAAAAAAAAAAAG%2FlXgEAAAAA19gXsS0QHhVWVOB%2BmrSkYn1VdYo%3DdTpC3RJ9ppaCv7ZL0zvgSoUW7hkHlKiQZBjSVM8SOGvEKxqr1c',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        print()
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)






    def start_requests(self):
        # top_projects =['BoredApeYC','OthersideMeta','cryptopunksnfts','RealMutantApeYC','RTFKT','moonbirds','AzukiOfficial','doodles','TownStarGame','GoGalaGames','MeebitsDAO','veefriends','TheSandboxGame']
        top_projects =['moonbirds']
        # top_projects =['I_have_adhd_']



        #Get ids for all accounts
        def find_id(name):

            url1 = f'https://api.twitter.com/2/users/by?usernames={name}&user.fields=created_at&expansions=pinned_tweet_id&tweet.fields=author_id,created_at'

            response1 = requests.get(url1, headers=self.header_data)

            return {'id':response1.json()['data'][0]['id'],'name':name}

        ids_ = list(map(find_id, top_projects))

        # print(ids_)




        # loop through each
        #send out start for each project
        print(ids_)
        for id in ids_:
            print(id)
            print('loop through IDs')

            # response = requests.get(f'https://api.twitter.com/1.1/friends/list.json?&screen_name={user}&skip_status=true&include_user_entities=false&count=200&cursor={cursor_num1}', headers=self.header_data)
            #
            # cursor_num1 = r['next_cursor']

            r = scrapy.Request( f'https://api.twitter.com/2/users/{id["id"]}/followers?max_results=1000&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld',
                              headers=self.header_data,
                              callback=self.get_chads_requests,
                              meta={'project':id})

            yield r


    def get_chads_requests(self,response):
        print('get_chads_requests')

        re = json.loads(response.text)
        id = response.meta.get('project')
        #send list of chads to get looped through and parsed
        print('project name:')
        print(id)
        print('len(ren[data])')
        print(len(re['data']))
        yield from self.parse_nft_chad(re, id)



        if "next_token" in re['meta']:

            print('next token:')
            print(re["meta"]["next_token"])
            r = scrapy.Request( f'https://api.twitter.com/2/users/{id["id"]}/followers?max_results=1000&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&pagination_token={re["meta"]["next_token"]}',
                              headers=self.header_data,
                              callback=self.get_chads_requests,
                              meta={'project':id} )
            yield r







    def parse_nft_chad(self, re, project):
        print('self.parse_nft_chad')
        print('project :',project)

        #loop through chads
        print('len(re[data])')
        print(len(re['data']))
        print('loop through users')
        for user in re['data']:

            # print(user)

            # session = self.Session()
            #
            # chad_exists = session.query(exists().where( NftChadsFollows.parent_nft_chad_id==user['id'])).scalar()
            # session.close()

            # if chad exists update recods with up-to-date-startingTimestampsUni

            # print('chad_exists: ',chad_exists )
            # print('project name: ', project['name'])
            NftChadsI= NftChadsItem()

            NftChadsI['parent_nft_account_id']=project['id']
            NftChadsI['twitter_id']=user['id']
            NftChadsI['name']=user['name']
            NftChadsI['screen_name']=user['username']
            loc = user['location'] if "location" in user else None
            NftChadsI['location']= loc
            NftChadsI['description']=user['description']
            NftChadsI['protected']=user['protected']
            NftChadsI['followers_count']=user['public_metrics']['followers_count']
            NftChadsI['following_count']=user['public_metrics']['following_count']
            NftChadsI['listed_count']=user['public_metrics']['listed_count']
            NftChadsI['tweet_count']=user['public_metrics']['tweet_count']
            # NftChadsI['url']=user['url']
            NftChadsI['created_at']=user['created_at']
            # NftChadsI['withheld']=user['withheld']
            NftChadsI['verified']=user['verified']
            en = user['entities'] if "entities" in user else None
            NftChadsI['entities']=en
            pin = user['pinned_tweet_id'] if "pinned_tweet_id" in user else None
            NftChadsI['pinned_tweet_id']=pin
            # NftChadsI['profile_image_url']=user['profile_image_url']

            # print('nft chad: ',user['id'])
            #save parent chades
            yield NftChadsI

            # check to see if this account has the same number of follows as last time


                                 # "https://api.twitter.com/2/users/2244994945/following?max_results=10"
            r = scrapy.Request( f'https://api.twitter.com/2/users/{user["id"]}/following?max_results=1000&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld',
                              headers=self.header_data,
                              callback=self.save_nft_chad_friends,
                              meta={'chad_id':user['id']} )

            # print('yeild following')
            yield r





    def save_nft_chad_friends(self, response):

        re = json.loads(response.text)
        print('save_nft_chad_friends')

        #maybe check here to see if total follows count in database matches api total follows


        chad_id = response.meta.get('chad_id')
        #save all firends of chands to see who the chads follow
        print('re[data] len save_nft_chad_friends :', len(re['data']))
        for user in re['data']:

            #check to see if chadd and follow combination already exists
            #since follows are in order of existnance, if it does exist that means we don't need to get the rest
            session = self.Session()
            chad_follow_exists = session.query(exists().where( NftChadsFollowsT.parent_nft_chad_id==chad_id and NftChadsFollowsT.twitter_id==user['id'] )).scalar()
            session.close()

            if chad_follow_exists:
                print('chad_follow_exists')
                return


            NftChadsFollowsI= NftChadsFollowsItem()
            NftChadsFollowsI['parent_nft_chad_id']=chad_id
            NftChadsFollowsI['twitter_id']=user['id']
            NftChadsFollowsI['name']=user['name']
            NftChadsFollowsI['screen_name']=user['username']
            loc = user['location'] if "location" in user else None
            NftChadsFollowsI['location']=loc
            NftChadsFollowsI['description']=user['description']
            NftChadsFollowsI['protected']=user['protected']
            NftChadsFollowsI['followers_count']=user['public_metrics']['followers_count']
            NftChadsFollowsI['following_count']=user['public_metrics']['following_count']
            NftChadsFollowsI['listed_count']=user['public_metrics']['listed_count']
            NftChadsFollowsI['tweet_count']=user['public_metrics']['tweet_count']
            # NftChadsFollows['url']=user['url']
            NftChadsFollowsI['created_at']=user['created_at']
            # NftChadsFollows['withheld']=user['withheld']
            NftChadsFollowsI['verified']=user['verified']
            en = user['entities'] if "entities" in user else None
            NftChadsFollowsI['entities']=en
            pin = user['pinned_tweet_id'] if "pinned_tweet_id" in user else None
            NftChadsFollowsI['pinned_tweet_id']=pin
            # NftChadsFollows['profile_image_url']=user['profile_image_url']


            yield NftChadsFollowsI

            #pagginate through all gets to get thier followers\


        if "next_token" in re['meta']:
            print("next_token True")

            r = scrapy.Request( f'https://api.twitter.com/2/users/{chad_id}/following?max_results=1000&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld&pagination_token={re["meta"]["next_token"]}',
                headers=self.header_data,
                callback=self.save_nft_chad_friends,
                meta={'chad_id':chad_id } )

            yield r
