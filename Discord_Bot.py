import os
import discord
import json
from discord.ext import commands
from pretty_help import PrettyHelp
from MemeGenerator import RedditCollector

with open('setup.json', 'r') as data:
    config = json.load(data)

discord_info = config['discord-bot']['discord']
reddit_info = config['discord-bot']['reddit']

subreddits=[]
for x in reddit_info['subreddits']:
    subreddits.append(x)

meme_collector = RedditCollector(client_id=reddit_info['id'], 
                                client_secret=reddit_info['secret'], 
                                user_agent=reddit_info['ua'], 
                                subreddits_list=subreddits, 
                                limit=50,
                                username='',
                                password='',
                                meme='')

DISCORD_TOKEN = discord_info['token']

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