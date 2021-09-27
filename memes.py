import discord
from discord.ext import commands
import json
import random
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
                                )

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Create bot command to grab an image from the subreddit list
    @commands.command(name="meme", help="Grabs a random meme from a list of subreddits")
    async def meme(self, ctx):
        # Initialize variables and call collect_meme method
        new_meme = meme_collector
        new_meme.collect_meme()
        # Set recent_meme equal to the grabbed url for use in badmeme command
        self.bot.recent_location = new_meme.memelocation
        self.bot.recent_meme = new_meme.meme
        await ctx.channel.send(new_meme.meme + "\n r/" + str(new_meme.memelocation))
        # Iterate memes_shown for use in count command
        self.bot.memes_shown+=1

    # Create bot command to output the number of memes that have been shown by the bot
    @commands.command(name="count", help="Displays how many memes have been shown by me")
    async def count(self, ctx):
        await ctx.channel.send("Very Cool!\nI have shown a total of " + str(self.bot.memes_shown) + " memes since doing doge things!\n Such Wow!")

    # Create bot command to flag a bad meme and add it to a blacklist
    @commands.command(name="badmeme", help="Adds the last meme shown to a blacklist of memes")
    async def badmeme(self, ctx):
        await ctx.channel.send("Such sad :cry: \n I will remember bad meme")
        config.badmemes["{}".format(self.bot.recent_meme)] = "Bad Meme"
        config.write_badmemes(config.badmemes)

    # Create bot command to flag a meme as a favorite and add it to a favorite list
    @commands.command(name="favorite", help="Adds the last meme shown to a favorite list of memes")
    async def favorite(self, ctx):
        await ctx.channel.send("Such wow :yum: \n I will remeber this exceptional meme")
        config.favorite["{}".format(self.bot.recent_meme)] = "Favorite"
        config.write_favorite(config.favorite)

    # Create bot command to display the number of elements in the bad memes array
    @commands.command(name="badlist", help="Displays the number of memes that have been blacklisted")
    async def badlist(self, ctx):
        await ctx.channel.send(":sob: There are " + str(len(config.badmemes)) + " on my bad memes list \n Better memes for you though :grinning:")

    # Create bot command to display a favorite meme
    @commands.command(name="givefavorite", help="Displays a meme that has been favorited")
    async def givefavorite(self, ctx, index: int = None):
        good = []
        for x in config.favorite:
            good.append(x)
        if index is not None:
            if (len(good) != 0):
                await ctx.channel.send(good[index-1])
            else:
                await ctx.channel.send("Sorry, you have not seen any amazing memes!\n Such sad :cry:")
        else:
            rannum = random.randint(0, len(config.favorite)-1)
            if (len(good) != 0):
                await ctx.channel.send(good[rannum])
            else:
                await ctx.channel.send("Sorry, you have not seen any amazing memes!\n Such sad :cry:")

def setup(bot):
    bot.add_cog(Memes(bot))