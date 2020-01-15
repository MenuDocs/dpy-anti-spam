import discord
from discord.ext  import commands
import copy
import datetime
from datetime import datetime, timezone
import random

import cogs._json

class UtilFunctions(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Utility Functions Cog has been loaded\n-----")

async def SendGlobalLog(bot, event, timestamp=None, author=None):
    """
    Essentially a function that will take the passed args, and then send the message to our global log channel in our support discord
    If a timestamp is not passed in, the bot will send a message to the log channel, get the dynamic timestamp from that message and use that
    If an author is not passed in, the bot will assume it is the author
    """
    if not timestamp:
        e = discord.Embed()
        try:
            msg = await bot.global_log_channel_object.send(embed=e)
        except:
            channel = bot.get_channel(int(bot.global_log_channel_id))
            msg = await channel.send(embed=e)

        embed = discord.Embed(title="Action Log:", description=event, timestamp=msg.created_at)
        if author:
            embed.set_author(name=author.name,icon_url=str(author.avatar_url))
        else:
            embed.set_author(name=bot.user.name,icon_url=str(bot.user.avatar_url))
        await msg.edit(embed=embed)
    else:
        embed = discord.Embed(title="Action Log:", description=event, timestamp=timestamp)
        if author:
            embed.set_author(name=author.name,icon_url=str(author.avatar_url))
        else:
            embed.set_author(name=bot.user.name,icon_url=str(bot.user.avatar_url))

        try:
            await bot.global_log_channel_object.send(embed=embed)
        except:
            channel = bot.get_channel(int(bot.global_log_channel_id))
            await channel.send(embed=embed)

async def SetupGuildDefaultConfig(guild):
    """
    Using the default settings in the config file, create and store settings for the guild while also adding some per guild settings into the mix
    """
    data = cogs._json.read_json('config')
    if not str(guild.id) in data['configs']:
        data['configs'][str(guild.id)] = {}

    data['configs'][str(guild.id)] = copy.deepcopy(data['configs']['default'])

    #Per guild only settings being added
    data['configs'][str(guild.id)]['logChannelID'] = None
    data['configs'][str(guild.id)]['guildBlacklistedUserIds'] = []
    data['configs'][str(guild.id)]['muteRoleId'] = None
    data['configs'][str(guild.id)]['welcomer'] = False
    data['configs'][str(guild.id)]['welcomeChannelId'] = None
    data['configs'][str(guild.id)]['welcomeMessage'] = "Hey MENTIONUSER! Welcome to GUILDNAME, enjoy your time here!\nJoin position: LENGUILDMEMBERS"
    data['configs'][str(guild.id)]['auditChannelId'] = None
    data['configs'][str(guild.id)]['discordContactPersonId'] = None

    cogs._json.write_json(data, 'config')

    return True

async def DeleteGuildSettings(guildId):
    """
    Removes the guilds data and settings from the dataset
    """
    data = cogs._json.read_json('config')
    if not guildId in data['configs']:
        return True

    data['configs'].pop(guildId)
    cogs._json.write_json(data, 'config')
    return True

async def CheckGuildHasSettings(guild):
    """
    A function used to check if a guild exists in the config
    file and if it doesnt, create the settings. This should be
    used before every function that uses guild settings basically
    """
    data = cogs._json.read_json('config')
    if not str(guild.id) in data['configs']:
        await SetupGuildDefaultConfig(guild)
    return True

async def RandomEmbedColor(self):
    return random.choice(self.bot.colorList)

async def StringReplaceConfigMessages(string, guild, member=None):
    """
    Essentially a function to check every end case we have for subsitution to save
    us writing loads of code everytime we need to sub something

    Things that still need to be added and handled that arent rn:
    DISCORDINVITE
    PUNISHMENTID
    OURDISCORDGUILDPREFIX
    """
    if member:
        if 'MENTIONUSER' in string:
            string = string.replace('MENTIONUSER', member.mention)
        if 'USERNAME' in string:
            string = string.replace('USERNAME', member.name)

    if guild:
        if 'LENGUILDMEMBERS' in string:
            string = string.replace('LENGUILDMEMBERS', str(len(guild.members)))
        if 'DISCORDNAME' in string:
            string = string.replace('DISCORDNAME', guild.name)
        if 'DISCORDID' in string:
            string = string.replace('DISCORDID', guild.id)
        if 'GUILDNAME' in string:
            string = string.replace('GUILDNAME', guild.name)

    list = ['DISCORDCONTACTPERSONINFO', 'OURDISCORDINVITE']
    trip = False
    for item in list:
        if item in string:
            trip = True
    if trip == True:
        data = cogs._json.read_json('config')
        if 'DISCORDCONTACTPERSONINFO' in string:
            if data['config'][str(guild.id)]['discordContactPersonId']:
                string = string.replace('DISCORDCONTACTPERSONINFO', data['config'][str(guild.id)]['discordContactPersonId'])
        if 'OURDISCORDINVITE' in string:
            string = string.replace('OURDISCORDINVITE', data['config'][str(guild.id)]['ourDiscordInvite'])

    return string

def setup(bot):
    bot.add_cog(UtilFunctions(bot))
