import os
import discord

from dotenv import load_dotenv

load_dotenv()

from RedditCollector import RedditCollector


data_collector = RedditCollector(client_id=os.getenv("REDDIT_ID"), 
                                client_secret=os.getenv("REDDIT_SECRET"), 
                                user_agent=os.getenv("REDDIT_UA"), 
                                subreddits_list=['memes'], 
                                limit=10,
                                username='',
                                password='')
data_collector.collect_data()
