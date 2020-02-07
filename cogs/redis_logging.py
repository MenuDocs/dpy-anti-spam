import discord
from discord.ext import commands
import redis
import time
import difflib

import cogs.util_functions

r = redis.Redis(host='localhost', port=6379, db=0)

class RedisLogging(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Redis Logging Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):
        payload = f'{message.content}:{await cogs.util_functions.TimeSinceEpoch()}:{message.channel.id}:{message.guild.id}'
        if not r.get(f'{message.author.id} LastMessage'):
            r.set(f'{message.author.id} LastMessage', payload, px=9000)
        else:
            #Maybe move to Levenshtein distance due to big O changes?
            oldMessage = r.getset(f'{message.author.id} LastMessage', payload)
            oldMessage = oldMessage.decode("utf-8")
            ratio = await CheckSimilar(oldMessage, message.content)
            print(ratio)
            if ratio <= 90:
                if not r.get(f'{message.author.id} LastMessageSpamCount'):
                    r.set(f'{message.author.id} LastMessageSpamCount', 2, px=9000)
                else:
                    r.incr(f'{message.author.id} LastMessageSpamCount')


    @commands.command()
    async def getallkeys(self, ctx):
        await ctx.send(f'Redis Keys:\n{r.keys()}')

    @commands.command()
    async def viewkey(self, ctx, *, key):
        await ctx.send(f'Result for key `{key}`:\n```{r.get(key)}```')

async def CheckSimilar(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def setup(bot):
    bot.add_cog(RedisLogging(bot))
