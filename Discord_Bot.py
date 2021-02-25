import os
import discord
import json
from discord.ext import commands
from pretty_help import PrettyHelp
from MemeGenerator import RedditCollector
from jsonHandler import jsonHandler

config = jsonHandler()

meme_collector = RedditCollector(client_id=config.reddit['id'], 
                                client_secret=config.reddit['secret'], 
                                user_agent=config.reddit['ua'], 
                                subreddits_list=config.subreddits, 
                                limit=50,
                                username='',
                                password='',
                                meme='')

DISCORD_TOKEN = config.discord['token']

default_prefix = "!"

async def determine_prefix(bot,message):
    guild = message.guild
    if guild:
        x = config.prefixes.get(str(guild.id), default_prefix)
        return x
    else:
        return default_prefix

bot = commands.Bot(command_prefix=determine_prefix)

bot.help_command = PrettyHelp(color = discord.Color.dark_gold(), show_index = False, no_category = "Commands", sort_commands = True)
print(bot.command_prefix)

bot.memes_shown = 0
bot.recent_meme = ""
bot.bad_memes = []

@bot.command(name="prefix", help="The prefix that Doge uses to get stuff")
async def prefix(ctx, *, prefix=""):
    config.prefixes["{}".format(ctx.guild.id)] = "{}".format(prefix)
    config.write_prefixes(config.prefixes)
    await ctx.channel.send("Prefix changed! Such Wow")

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