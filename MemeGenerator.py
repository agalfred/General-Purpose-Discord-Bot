import praw
import urllib
import os
import datetime
import random
from math import floor
from jsonHandler import jsonHandler

# Create an instance of jsonHandler class
handler = jsonHandler()

# Create random seed 
random.seed()

# Create class that can be called that will grab meme from list of subreddits provided
class RedditCollector:

    def __init__(self, client_id, client_secret, user_agent, subreddits_list, limit, username, password):
    
        # Initialize variables for RedditCollector Class
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.subreddits_list = subreddits_list
        self.limit = limit
        self.username = username
        self.password = password

        # Create reddit connection using praw and the information provided in initialization
        self.reddit = praw.Reddit(client_id = self.client_id, client_secret = self.client_secret, user_agent = self.user_agent, username=username, password=password, check_for_async=False)

    # Method that will select random subreddit and call future methods
    def collect_meme(self):
        
        # Select random subreddit from array
        ran_subreddit = random.randint(0, (len(self.subreddits_list)-1))
        subreddit_name = self.subreddits_list[ran_subreddit]
        self.memelocation = subreddit_name
        # Call grab_meme method with selected subreddit as input
        self.grab_meme(subreddit_name)

    # Method that will grab a random image url from reddit
    def grab_meme(self, subreddit):

        # Specify what image extensions we want to allow
        allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.gifv']

        # Initialize arrays for urls
        self.meme_urls = []
        self.posts = []

        # Grab number of images from the subreddit based on the limit provided
        # It grabs more than one image to improve randomness of the bot
        subreddit = self.reddit.subreddit(subreddit)  
        posts = subreddit.hot(limit=self.limit)
        for post in posts:
            _, ext = os.path.splitext(post.url)
            # Check to see if the image has an allowed extension
            if ext in allowed_image_extensions:
                self.meme_urls.append(post.url.encode('utf-8'))

        # Call method to return a random url that was pulled
        self.return_url()

    # Method that will return random url from the array of urls pulled from reddit
    # This is primarily to improve the randomness of the output from the bot
    def return_url(self):
        meme_num = (len(self.meme_urls)-1)
        meme_out = random.randint(0,meme_num)
        self.meme=self.meme_urls[meme_out].decode('utf-8')
        # Check to see if the url is blacklisted
        check = handler.badmemes.get(str(self.meme), "False")
        while check == "Bad Meme":
            meme_out = random.randint(0,meme_num)
            check = handler.badmemes.get(str(self.meme), "False")
        self.meme=self.meme_urls[meme_out].decode('utf-8')