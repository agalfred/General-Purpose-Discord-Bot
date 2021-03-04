import os
import discord
import json
import random
from discord.ext import commands
from pretty_help import PrettyHelp
from MemeGenerator import RedditCollector
from jsonHandler import jsonHandler

# Create an instance of jsonHandler class
config = jsonHandler()

# Create instance of RedditCollector class and initite it
meme_collector = RedditCollector(client_id=config.reddit['id'], 
                                client_secret=config.reddit['secret'], 
                                user_agent=config.reddit['ua'], 
                                subreddits_list=config.subreddits, 
                                limit=50,
                                username='',
                                password='',
                                meme='')

# Assign local variable for Dicord Token
DISCORD_TOKEN = config.discord['token']

# Assign default prefix
default_prefix = "!"

# Check to see if the discord server has a defined prefix in prefixes.json
async def determine_prefix(bot,message):
    guild = message.guild
    if guild:
        # If the server has a defined prefix, return it otherwise return the default prefix
        x = config.prefixes.get(str(guild.id), default_prefix)
        return x
    else:
        return default_prefix

# Create instance of Discord bot class
bot = commands.Bot(command_prefix=determine_prefix)

# Create better looking help command using PrettyHelp
bot.help_command = PrettyHelp(color = discord.Color.dark_gold(), show_index = False, no_category = "Commands", sort_commands = True)

# Initiate local bot class variables
bot.memes_shown = 0
bot.recent_meme = ""

# Create bot command that allows user to define a new prefix
@bot.command(name="prefix", help="The prefix that Doge uses to get stuff")
async def prefix(ctx, *, prefix=""):
    config.prefixes["{}".format(ctx.guild.id)] = "{}".format(prefix)
    # Write Discord server id and defined prefix to prefixes.json
    config.write_prefixes(config.prefixes)
    await ctx.channel.send("Prefix changed! Such Wow")

# Create bot command to grab an image from the subreddit list
@bot.command(name="meme", help="Grabs a random meme from a list of subreddits")
async def meme(ctx):
    # Initialize variables and call collect_meme method
    new_meme = meme_collector
    new_meme.collect_meme()
    # Set recent_meme equal to the grabbed url for use in badmeme command
    bot.recent_meme = new_meme.meme
    await ctx.channel.send(new_meme.meme)
    # Iterate memes_shown for use in count command
    bot.memes_shown+=1

# Create bot command to output the number of memes that have been shown by the bot
@bot.command(name="count", help="Displays how many memes have been shown by me")
async def count(ctx):
    await ctx.channel.send("Very Cool!\nI have shown a total of " + str(bot.memes_shown) + " memes since doing doge things!\n Such Wow!")

# Create bot command to flag a bad meme and add it to a blacklist
@bot.command(name="badmeme", help="Adds the last meme shown to a blacklist of memes")
async def badmeme(ctx):
    await ctx.channel.send("Such sad :cry: \n I will not show bad meme again")
    config.badmemes["{}".format(bot.recent_meme)] = "Bad Meme"
    config.write_badmemes(config.badmemes)

# Create bot command to display the number of elements in the bad memes array
@bot.command(name="badlist", help="Displays the number of memes that have been blacklisted")
async def badlist(ctx):
    await ctx.channel.send(":sob: There are " + str(len(config.badmemes)) + " on my bad memes list \n Better memes for you though :grinning:")

# Create bot command to display a blacklisted meme
@bot.command(name="givebadmeme", help="Displays a meme that has been blacklisted")
async def givebadmeme(ctx):
    bad = []
    for x in config.badmemes:
        bad.append(x)
    rannum = random.randint(0, len(config.badmemes))
    if (len(bad) != 0):
        await ctx.channel.send(bad[rannum])
    else:
        await ctx.channel.send("Congrats, you have not seen any bad memes!\n Amaze :grinning:")

# Run the bot using the Discord token provided
bot.run(DISCORD_TOKEN)