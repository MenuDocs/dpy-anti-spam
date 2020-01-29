import discord
from discord.ext import commands

import cogs._json
import cogs.util_functions

class SpamChecks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Spam Checks Cog has been loaded\n-----")

    @commands.command()
    async def cm(self, ctx, *, args):
        t = await UserSpamMessageMinimumCharacterLengthCheck(self.bot, ctx.guild, ctx.author, ctx.channel, args)
        await ctx.send(t)

    @commands.command()
    @commands.is_owner()
    async def setguilddefault(self, ctx):
        await cogs.util_functions.SetupGuildDefaultConfig(ctx.guild)

async def UserSpamMessageMinimumCharacterLengthCheck(bot, guild, user, channel, message):
    """
    A funtion used to check the message in question meets the requirments for minimum
    character lengths for spam in the guild in question.
    This function is essentially step one in any mute function where a check may be run.
    *May not be used to check spam when using timestamps rather than actual message content
    """
    data = cogs._json.read_json('config')
    if isinstance(channel, discord.DMChannel):
        return
    await cogs.util_functions.CheckGuildHasSettings(guild)
    guildSetting = data['configs'][str(guild.id)]['userMessagesMinThresholdForSpam']
    if len(message) >= guildSetting:
        return True
    else:
        return False


async def GroupSpamMessageMinimumCharacterLength(bot, guild, user, message, channel):
    data = cogs._json.read_json('config')
    if isinstance(channel, discord.DMChannel):
        return
    await cogs.util_functions.CheckGuildHasSettings(guild)
    guildSetting = data['configs'][str(guild.id)]['groupMessagesMinThresholdForSpam']
    if len(message) >= guildSetting:
        return True
    else:
        return False

async def UserSpamTimer(bot, guild, user, message, channel);
    data = cogs._json.read_json('config')
     if isinstance(channel, discord.DMChannel):
        return
    await


def setup(bot):
    bot.add_cog(SpamChecks(bot))
