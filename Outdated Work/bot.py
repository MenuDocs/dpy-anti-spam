import discord
from discord.ext import commands
import pathlib
from pathlib import Path
import json
import re # regex
import platform
import os
import asyncio

import cogs._json
import cogs.util_functions

#Printing the current working directory just cos
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(cwd)

def get_prefix(bot, message):
    data = cogs._json.read_json('config')
    if not message.guild or str(message.guild.id) not in data['configs']:
        return commands.when_mentioned_or(data['configs']['default']['prefix'])(bot, message)
    return commands.when_mentioned_or(data['configs'][str(message.guild.id)]['prefix'])(bot, message)

bot = commands.Bot(command_prefix=get_prefix, case_insensitve=True, owner_id=271612318947868673)
bot.remove_command('help')

secret_file = json.load(open(cwd+'/bot_config/token.json'))
bot.config_token = secret_file['token']

bot.Version = "0.0.3"

colors = {
  'WHITE': 0xFFFFFF,
  'AQUA': 0x1ABC9C,
  'GREEN': 0x2ECC71,
  'BLUE': 0x3498DB,
  'PURPLE': 0x9B59B6,
  'LUMINOUS_VIVID_PINK': 0xE91E63,
  'GOLD': 0xF1C40F,
  'ORANGE': 0xE67E22,
  'RED': 0xE74C3C,
  'NAVY': 0x34495E,
  'DARK_AQUA': 0x11806A,
  'DARK_GREEN': 0x1F8B4C,
  'DARK_BLUE': 0x206694,
  'DARK_PURPLE': 0x71368A,
  'DARK_VIVID_PINK': 0xAD1457,
  'DARK_GOLD': 0xC27C0E,
  'DARK_ORANGE': 0xA84300,
  'DARK_RED': 0x992D22,
  'DARK_NAVY': 0x2C3E50
}
bot.colorList = [c for c in colors.values()]

@bot.event
async def on_ready():
    data = cogs._json.read_json('config')
    bot.delete_guild_data_on_remove = data['configs']['deleteGuildDataOnRemove']
    bot.global_log_channel_id = data['configs']['default']['globalLogChannelId']
    bot.global_log_channel_object = bot.get_channel(int(bot.global_log_channel_id))

    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----")
    await bot.change_presence(activity=discord.Game(name="Playing with dpy anti spam"))

@bot.command(name='reload', description='Reload all cogs!')
@commands.is_owner()
async def reload_bot(ctx):
    async with ctx.typing():
        for file in os.listdir(cwd+"/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                try:
                    bot.unload_extension(f"cogs.{file[:-3]}")
                    bot.load_extension(f"cogs.{file[:-3]}")
                    await ctx.send(':white_check_mark: Reloaded: ``'+f"cogs.{file[:-3]}"+'``')
                except:
                    await ctx.send(':x: Failed: ``'+f"cogs.{file[:-3]}"+'``')

        data = cogs._json.read_json('config')
        bot.delete_guild_data_on_remove = data['configs']['deleteGuildDataOnRemove']

@bot.command()
@commands.is_owner()
async def savetest(ctx):
    print('starting')
    with open("tests/detecting spam messages testing/training2.txt","a") as f:
        for guild in bot.guilds:
            print(guild.name)
            for channel in guild.text_channels:
                print(channel.name)
                async for message in channel.history(limit=5000):
                    try:
                        f.write(f'{message.clean_content}\n')
                    except:
                        pass
                await asyncio.sleep(5)
            await asyncio.sleep(25)
    print('finished')

def SetupJsonDefaults():
    data = cogs._json.read_json('config')
    data['configs'] = {}

    data['configs']['deleteGuildDataOnRemove'] = True

    data['configs']['default'] = {}
    data['configs']['default']['prefix'] = '~~'
    data['configs']['default']['userSpamWarningMessage'] = "Stop spamming MENTIONAUTHOR, or I will be forced to take action!" #Captial letter words will be subbed out for there actual equvialant using regex
    data['configs']['default']['userSpamMuteMessage'] = "Hey MENTIONAUTHOR! I have muted you for spam, you will be unmuted at UNMUTETIME."
    data['configs']['default']['groupSpamWarningMessage'] = 'Hey! I need all of you to stop spamming before I punish everyone.'
    data['configs']['default']['groupSpamMuteMessage'] = 'Well, now you\'ve done it. I\'ve had to mute you all.'
    data['configs']['default']['spamAutoChannelLockMessage'] = 'Due to spam, I have locked down this channel!'
    data['configs']['default']['userFullChannelLockdownNewUserAutoMuteMessage'] = 'Hey, due to an ongoing full guild lockdown all new users are auto muted.\nPlease contact DISCORDCONTACTPERSONINFO or join our support discord to dispute the mute. ||OURDISCORDINVITE||'
    data['configs']['default']['auditFullChannelLockdownNewUserAutoMuteMessage'] = 'Due to an ongoing full guild lockdown, I have auto muted USERNAME. I have also provided information on how to get it removed.'
    data['configs']['default']['fullChannelLockdownNewUserAutoKickMessage'] = 'Hey, due to an ongoing full guild lockdown all new users are auto kicked. Here is an invite back to the discord, feel free to rejoin in around 15 minutes. ||DISCORDINVITE||\nIf this continues please contact DISCORDCONTACTPERSONINFO or join our support discord to dispute the kick. ||OURDISCORDINVITE||'
    data['configs']['default']['auditChannelLockdownNewUserAutoKickMessage'] = 'Due to an ongoing full guild lockdown, I have auto kicked USERNAME. I have also provided information on how to get it dealt with.'

    data['configs']['default']['muteLength'] = 18000 #In milli seconds - 18000 = 5 mins
    data['configs']['default']['timesWarnedBeforeMute'] = 3 #10th time the bot pulls u up is a ban
    data['configs']['default']['timesMutedBeforeKick'] = 3
    data['configs']['default']['timesKickedBeforeBan'] = 1

    data['configs']['default']['groupSpamTimer'] =  9000 # Essentially the maximum time between different users messages before it is not considered spam
    data['configs']['default']['userSpamTimer'] = 9000 # Same as above just for per user
    data['configs']['default']['channelSpamTimer'] = 9000 # Essentially the same as above but for per channel settings
    data['configs']['default']['singleChannelLockTime'] = 18000 # 5 mins
    data['configs']['default']['allGuildChannelLockTime'] = 36000 # 10 mins

    data['configs']['default']['userMessagesMinThresholdForSpam'] = 3
    data['configs']['default']['channelMessagesMinThresholdForSpam'] = 3
    data['configs']['default']['guildMessagesMinThresholdForSpam'] = 10
    data['configs']['default']['userSpamMessageMinimumCharacterLength'] = 3
    data['configs']['default']['groupSpamMessageMinimumCharacterLength'] = 3
    data['configs']['default']['maxMessageMentionsBeforePunishment'] = 5

    data['configs']['default']['bypassWarnMode'] = False
    data['configs']['default']['bypassMuteMode'] = False
    data['configs']['default']['bypassKickMode'] = False
    data['configs']['default']['bypassBanMode'] = False
    data['configs']['default']['onChannelSpamTripLockChannel'] = True
    data['configs']['default']['onGuildSpamTripLockAllChannels'] = True
    data['configs']['default']['duringFullLockdownAutoMuteNewUsers'] = True
    data['configs']['default']['duringFullLockdownAutoKickNewUsers'] = False
    data['configs']['default']['deleteDuplicateText'] = True

    data['configs']['default']['dmKickedUserMessage'] = 'Hey! Look, I have had to kick you from DISCORDNAME due to the amount of punishments you have received. If I have to punish you again I will ban you.\nHeres an invite back to the discord : DISCORDINVITE'
    data['configs']['default']['auditLogKickedUserMessage'] = 'I kicked USERNAME as they had excedded the punishment limit before receiving a kick. They have received an invite back however, with warnings agaisnt further misconduct.'
    data['configs']['default']['dmBanUserMessage'] = 'Hey I did warn you! Consider yourself banned from DISCORDNAME.\nTo dispute this please join our support server and in the disputes channel type OURDISCORDGUILDPREFIXdispute PUNISHMENTID\n||OURDISCORDINVITE||'
    data['configs']['default']['auditLogBanUserMessage'] = 'I banned USERNAME as they had excedded the punishment limit before receiving a ban. They have been issued details on how to dispute the punishment.'

    data['configs']['default']['globalLogKickMessage'] = '---\nI kicked USERNAME from DISCORDNAME (DISCORDID) for excedding defined limits. Punishment Id is PUNSIHMENTID\n---'
    data['configs']['default']['globalLogBanMessage'] = '---\nI banned USERNAME from DISCORDNAME (DISCORDID) for excedding defined limits. Punishment Id is PUNISHMENTID\n---'
    data['configs']['default']['ourDiscordId'] = 662277468983525376
    data['configs']['default']['globalSupportChannelId'] = None
    data['configs']['default']['globalLogChannelId'] = 664603812689870871
    data['configs']['default']['globalKickLogChannelId'] = None
    data['configs']['default']['globalBanLogChannelId'] = None

    data['configs']['default']['ourDiscordInvite'] = 'Null, Contact one of the devs since this is a placeholder atm'
    data['configs']['default']['enableUserBypassList'] = True
    data['configs']['default']['enableRoleBypassList'] = True
    data['configs']['default']['userBypassList'] = [271612318947868673, 387138288231907329]
    data['configs']['default']['roleBypassList'] = []
    data['configs']['default']['globalBlacklistedUserIds'] = []

    cogs._json.write_json(data, 'config')

    #print(len(data['configs']['default']))

#tests/detecting spam messages testing

if __name__ == '__main__':
    #SetupJsonDefaults()
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)
