import os
import discord
from discord.ext import commands
from pretty_help import PrettyHelp
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

global memes_shown

bot = commands.Bot(command_prefix=bot_prefix)

bot.help_command = PrettyHelp(color = discord.Color.dark_gold(), show_index = False, no_category = "Commands", sort_commands = True)

bot.memes_shown = 0
bot.recent_meme = ""
bot.bad_memes = []

@bot.command(name="meme", help="Grabs a random meme from a list of subreddits")
async def meme(ctx):
    new_meme = meme_collector
    new_meme.collect_meme()
    bot.recent_meme = new_meme.meme
    await ctx.channel.send(new_meme.meme)
    print("A new meme was displayed\n")
    bot.memes_shown+=1

@bot.command(name="count", help="Displays how many memes have been shown by me")
async def count(ctx):
    await ctx.channel.send("Very Cool!\nI have shown a total of " + str(bot.memes_shown) + " memes since doing doge things!\n Such Wow!")

@bot.command(name="badmeme", help="Adds the last meme shown to a blacklist of memes")
async def badmeme(ctx):
    await ctx.channel.send("Such sad :cry: \n I will not show bad meme again")
    bot.bad_memes.append(bot.recent_meme)

@bot.command(name="badlist", help="Displays the number of memes that have been blacklisted")
async def badlist(ctx):
    await ctx.channel.send(":sob: There are " + str(len(bot.bad_memes)) + " on my bad memes list \n Better memes for you though :grinning:")

bot.run(DISCORD_TOKEN)