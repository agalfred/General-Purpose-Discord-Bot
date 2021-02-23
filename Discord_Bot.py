import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from MemeGenerator import RedditCollector

load_dotenv()

meme_collector = RedditCollector(client_id=os.getenv("REDDIT_ID"), 
                                client_secret=os.getenv("REDDIT_SECRET"), 
                                user_agent=os.getenv("REDDIT_UA"), 
                                subreddits_list=['MemeEconomy','memes','dankmemes','PrequelMemes','terriblefacebookmemes','wholesomememes', 'CollegeMemes', 'ComedyCemetery', 'retailmemes', 'Memes_Of_The_Dank', 'Animemes', 'marvelmemes'], 
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