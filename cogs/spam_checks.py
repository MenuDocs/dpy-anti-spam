import discord
from discord.ext import commands

import cogs._json
import cogs.util_functions

class SpamChecks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def checkmessage(self, ctx, *, args):
        await UserMessageMeetsThreshold(self.bot, ctx.guild, ctx.author, args)

async def UserMessageMeetsThreshold(bot, guild, user, message):
    data = cogs._json.read_json('config')
    if not str(guild.id) in data['configs']:
        guildSetting = data['configs']['default']['userMessagesMinThresholdForSpam']
        await cogs.util_functions.SetupGuildDefaultConfig(guild)
    else:
        guildSetting = data['configs'][str(guild.id)]['userMessagesMinThresholdForSpam']
    messageContent = message
    if len(messageContent) > guildSetting:
        #do stuff
        pass


async def groupSpamMessageMinimumCharacterLength(bot, guild, user, message):






def setup(bot):
    bot.add_cog(SpamChecks(bot))
