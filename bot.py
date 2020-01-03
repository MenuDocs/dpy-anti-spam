import discord
from discord.ext import commands
import pathlib
from pathlib import Path
import json
import re # regex
import platform

#Printing the current working directory just cos
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(cwd)

def get_prefix(bot, message):
    data = read_json('config')
    if not message.guild or str(message.guild.id) not in data['configs']:
        return commands.when_mentioned_or(data['configs']['default']['prefix'])(bot, message)
    return commands.when_mentioned_or(data['configs'][str(message.guild.id)]['prefix'])(bot, message)

bot = commands.Bot(command_prefix=get_prefix, case_insensitve=True, owner_ids=[271612318947868673, 387138288231907329])

secret_file = json.load(open(cwd+'/bot_config/token.json'))
bot.config_token = secret_file['token']

botVersion = "0.0.2"

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----")
    await bot.change_presence(activity=discord.Game(name="Playing with dpy anti spam"))

@bot.event
async def on_message(message):
    data = read_json('config')
    if message.content == 'test1':
        msg = data['configs']['default']['userSpamWarningMessage']
        msg = msg.replace('MENTIONAUTHOR', message.author.mention)  #re.sub('MENTIONAUTHOR', message.author.mention, msg)
        await message.channel.send(content=msg)
    elif message.content == 'test2':
        msg = data['configs']['default']['userSpamMuteMessage']
        msg = msg.replace('MENTIONAUTHOR', message.author.mention) #re.sub('MENTIONAUTHOR', message.author.mention, msg)
        await message.channel.send(content=f'{msg}')

    await bot.process_commands(message)

@bot.command()
@commands.is_owner()
async def logout(ctx):
    """Log the bot out of discord"""
    await ctx.send("Logging out...")
    await bot.logout()

def read_json(filename):
    with open(cwd+'/bot_config/'+filename+'.json', 'r') as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(cwd+'/bot_config/'+filename+'.json', 'w') as file:
        json.dump(data, file, indent=4)

@bot.command()
async def stats(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))
    embed = discord.Embed(title=f'{bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour)
    embed.add_field(name='Bot Version:', value=botVersion)
    embed.add_field(name='Python Version:', value=pythonVersion)
    embed.add_field(name='Discord.Py Version', value=dpyVersion)
    embed.add_field(name='Total Guilds:', value=serverCount)
    embed.add_field(name='Total Users:', value=memberCount)
    embed.add_field(name='Bot Developers:', value="<@271612318947868673> and <@387138288231907329>")
    embed.set_footer(text=f"Carpe Noctem | {bot.user.name}")
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)

def SetupJsonDefaults():
    data = read_json('config')
    data['configs'] = {}
    data['configs']['default'] = {}
    data['configs']['default']['prefix'] = '--'
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

    data['configs']['default']['bypassWarnMode'] = False
    data['configs']['default']['bypassMuteMode'] = False
    data['configs']['default']['bypassKickMode'] = False
    data['configs']['default']['bypassBanMode'] = False
    data['configs']['default']['onChannelSpamTripLockChannel'] = True
    data['configs']['default']['onGuildSpamTripLockAllChannels'] = True
    data['configs']['default']['duringFullLockdownAutoMuteNewUsers'] = True
    data['configs']['default']['duringFullLockdownAutoKickNewUsers'] = False

    data['configs']['default']['dmKickedUserMessage'] = 'Hey! Look, I have had to kick you from DISCORDNAME due to the amount of punishments you have received. If I have to punish you again I will ban you.\nHeres an invite back to the discord : DISCORDINVITE'
    data['configs']['default']['auditLogKickedUserMessage'] = 'I kicked USERNAME as they had excedded the punishment limit before receiving a kick. They have received an invite back however, with warnings agaisnt further misconduct.'
    data['configs']['default']['dmBanUserMessage'] = 'Hey I did warn you! Consider yourself banned from DISCORDNAME.\nTo dispute this please join our support server and in the disputes channel type OURDISCORDGUILDPREFIXdispute PUNISHMENTID\n||OURDISCORDINVITE||'
    data['configs']['default']['auditLogBanUserMessage'] = 'I banned USERNAME as they had excedded the punishment limit before receiving a ban. They have been issued details on how to dispute the punishment.'

    data['configs']['default']['globalLogKickMessage'] = '---\nI kicked USERNAME from DISCORDNAME (DISCORDID) for excedding defined limits. Punishment Id is PUNSIHMENTID\n---'
    data['configs']['default']['globalLogBanMessage'] = '---\nI banned USERNAME from DISCORDNAME (DISCORDID) for excedding defined limits. Punishment Id is PUNISHMENTID\n---'
    data['configs']['default']['ourDiscordId'] = 662277468983525376
    data['configs']['default']['globalSupportChannelId'] = None
    data['configs']['default']['globalKickLogChannelId'] = None
    data['configs']['default']['globalBanLogChannelId'] = None

    data['configs']['default']['ourDiscordInvite'] = 'Null, Contact one of the devs since this is a placeholder atm'
    data['configs']['default']['enableUserBypassList'] = True
    data['configs']['default']['enableRoleBypassList'] = True
    data['configs']['default']['userBypassList'] = [271612318947868673, 387138288231907329]
    data['configs']['default']['roleBypassList'] = []
    data['configs']['default']['globalBlacklistedUserIds'] = []

    data['configs']['default'][''] = ''
    write_json(data, 'config')

    print(len(data['configs']['default']))

if __name__ == '__main__':
    SetupJsonDefaults()
    bot.run(bot.config_token)
