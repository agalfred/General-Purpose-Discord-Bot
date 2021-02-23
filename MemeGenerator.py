import praw
import urllib
import os
import datetime
import random
from math import floor

random.seed()

class RedditCollector:

    def __init__(self, client_id, client_secret, user_agent, subreddits_list, limit, username, password, meme):
    
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.subreddits_list = subreddits_list
        self.limit = limit
        self.username = username
        self.password = password
        self.meme = meme
        self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret, user_agent = self.user_agent, username=username, password=password)

    def collect_meme(self):

        ran_subreddit = random.randint(0, (len(self.subreddits_list)-1))
        print("Random subreddit number " + str(ran_subreddit) + "\n")
        subreddit_name = self.subreddits_list[ran_subreddit]
        self.grab_meme(subreddit_name)


    def grab_meme(self, subreddit):

        allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.gifv']

        self.meme_urls = []
        self.posts = []
        self.post_urls = []

        subreddit = self.reddit.subreddit(subreddit)  
        posts = subreddit.hot(limit=self.limit)
        for post in posts:
            _, ext = os.path.splitext(post.url)
            if ext in allowed_image_extensions:
                self.meme_urls.append(post.url.encode('utf-8'))

        self.return_url()

    def return_url(self):
        meme_num = (len(self.meme_urls)-1)
        print("Number of possible memes " + str(meme_num) + "\n")
        meme_out = random.randint(0,meme_num)
        self.meme=self.meme_urls[meme_out].decode('utf-8')
        print("Meme number to be output " + str(meme_out) + "\n")