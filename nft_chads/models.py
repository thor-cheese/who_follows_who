from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData, exists
from sqlalchemy.orm import relationship
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text, BigInteger)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import database_exists, create_database
from scrapy.utils.project import get_project_settings


from datetime import datetime

from nft_chads import settings

# datetime object containing current date and time
now = datetime.now()

print("now =", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y")

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    "postgres://postgres@/postgres"
    URL(**settings.DATABASE)

    database_vars = get_project_settings().get("DATABASE")

    connection_string = f'postgresql+psycopg2://{database_vars["username"]}:{database_vars["password"]}@{database_vars["host"]}/{database_vars["database"]}'

    engine = create_engine(connection_string)
    if not database_exists(engine.url):
        create_database(engine.url)


    return engine


def create_table(engine):
    Base.metadata.create_all(engine)


# Association Table for One-To-Many relationship between Quote and Tag
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
class NftChads(Base):
    __tablename__ = f'NftChads'
    ID = Column(Integer, primary_key=True)
    parent_nft_account_id = Column('parent_nft_account_id', String(225), unique=False)
    created_at= Column('created_at', DateTime, unique=False)
    description= Column('description', String(225), unique=False)
    entities = Column('entities', JSONB, unique=False)
    twitter_id = Column('twitter_id', String(225), unique=False)
    location = Column('location', String(225), unique=False)
    name = Column('name', String(225), unique=False)
    pinned_tweet_id = Column('pinned_tweet_id', String(225), unique=False)
    profile_image_url = Column('profile_image_url', String(225), unique=False)
    protected= Column('protected', Boolean, unique=False)
    followers_count = Column('followers_count', Integer, unique=False)
    following_count= Column('following_count', Integer, unique=False)
    listed_count= Column('listed_count', Integer, unique=False)
    tweet_count= Column('tweet_count', Integer, unique=False)
    url = Column('url', JSONB, unique=False)
    screen_name= Column('screen_name', String(225), unique=False)
    withheld= Column('withheld', JSONB, unique=False)



class NftChadsFollowsT(Base):
    __tablename__ = f'NftChadsFollows'


    ID = Column(Integer, primary_key=True)
    parent_nft_chad_id = Column('parent_nft_chad_id', String(225), unique=False)
    date_scraped= Column('date_scraped', DateTime, unique=False)
    created_at= Column('created_at', DateTime, unique=False)
    description= Column('description', String(225), unique=False)
    entities = Column('entities', JSONB, unique=False)
    twitter_id = Column('twitter_id', String(225), unique=False)
    location = Column('location', String(225), unique=False)
    name = Column('name', String(225), unique=False)
    pinned_tweet_id = Column('pinned_tweet_id', String(225), unique=False)
    profile_image_url = Column('profile_image_url', String(225), unique=False)
    protected= Column('protected', Boolean, unique=False)
    followers_count = Column('followers_count', Integer, unique=False)
    following_count= Column('following_count', Integer, unique=False)
    listed_count= Column('listed_count', Integer, unique=False)
    tweet_count= Column('tweet_count', Integer, unique=False)
    url = Column('url', JSONB, unique=False)
    screen_name= Column('screen_name', String(225), unique=False)
    # follow_index= Column('follow_index', Integer, unique=False)
    withheld= Column('withheld', JSONB, unique=False)


# class account_counts(Base):
#     __tablename__ = f'account_counts'
#     ID = Column(Integer, primary_key=True)
#     date_scraped= Column('date_scraped', DateTime, unique=False)
#     count= Column('count', BigInteger, unique=False)
#     screen_name= Column('screen_name', String(225), unique=False)
