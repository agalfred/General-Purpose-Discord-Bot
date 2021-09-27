import os
import discord
import json
from discord.ext import commands
from pretty_help import PrettyHelp
from MemeGenerator import RedditCollector
from jsonHandler import jsonHandler

# Create an instance of jsonHandler class
config = jsonHandler()

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

# List cogs to be loaded
initial_extensions = ["memes",
                      "music"
                      ]

# Create instance of Discord bot class
bot = commands.Bot(command_prefix=determine_prefix, description='The Bestest of Bois!')

# Initiate local bot class variables
bot.memes_shown = 0
bot.recent_meme = ""
bot.recent_location = ""

# Create better looking help command using PrettyHelp
bot.help_command = PrettyHelp(color = discord.Color.dark_gold(), show_index = False, no_category = "Commands", sort_commands = True)

# Load our extensions(cogs) listed above
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# Create message that is sent to default server channel upon joining
@bot.event
async def on_guild_join(guild):
    if guild.system_channel:
        await guild.system_channel.send("WOW! Thanks for the invite. \nMy default prefix is '" + str(default_prefix) + "'. Type " + str(default_prefix) + "help to get started.")

# Create bot command that allows user to define a new prefix
@bot.command(name="prefix", help="The prefix that Doge uses to get stuff")
async def prefix(ctx, *, prefix=""):
    config.prefixes["{}".format(ctx.guild.id)] = "{}".format(prefix)
    # Write Discord server id and defined prefix to prefixes.json
    config.write_prefixes(config.prefixes)
    await ctx.channel.send("Prefix changed! Such Wow")

# Run the bot using the Discord token provided
bot.run(DISCORD_TOKEN)