import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from MemeGenerator import RedditCollector

load_dotenv()

subreddits_file = open('subreddits.txt','r')
subreddits_listed = subreddits_file.read()
subreddits_split = subreddits_listed.splitlines()
subreddits_file.close()

meme_collector = RedditCollector(client_id=os.getenv("REDDIT_ID"), 
                                client_secret=os.getenv("REDDIT_SECRET"), 
                                user_agent=os.getenv("REDDIT_UA"), 
                                subreddits_list=subreddits_split, 
                                limit=50,
                                username='',
                                password='',
                                meme='')

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot_prefix = "!"

bot = commands.Bot(command_prefix=bot_prefix)

@bot.command(name="meme")
async def meme(ctx):
    new_meme = meme_collector
    new_meme.collect_meme()
    await ctx.channel.send(new_meme.meme)

bot.run(DISCORD_TOKEN)