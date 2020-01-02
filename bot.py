import discord
from discord.ext import commands
import pathlib
from pathlib import Path
import json

#Printing the current working directory just cos
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(cwd)

def get_prefix(bot, message):
    data = read_json('config')
    if not message.guild or str(message.guild.id) not in data:
        return commands.when_mentioned_or(data['configs']['defaults']['prefix'])(bot, message)
    return commands.when_mentioned_or(data['configs'][str(message.guild.id)]['prefix'])(bot, message)

bot = commands.Bot(command_prefix=get_prefix, case_insensitve=True, owner_ids=[271612318947868673, 387138288231907329])

secret_file = json.load(open(cwd+'/bot_config/token.json'))
bot.config_token = secret_file['token']

botVersion = "0.0.1"

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----")
    await bot.change_presence(activity=discord.Game(name="Playing with dpy anti spam"))

@bot.event
async def on_message(message):
    data = read_json('config')
    if message.content == 'test1':
        msg = data['configs']['default']['userSpamWarningMessage']
        await message.channel.send(content=f'{msg}')
    elif message.content == 'test2':
        msg = data['configs']['default']['userSpamMuteMessage']
        await message.channel.send(content=f'{msg}')

@bot.command()
@commands.is_owner()
async def logout(ctx):
    """Log the bot out of discord"""
    await ctx.send("Logging out...")
    await bot.logout()

def read_json(filename):
    jsonFile = open(str(cwd)+'/bot_config/'+filename+'.json', 'r')
    data = json.load(jsonFile)
    jsonFile.close()
    return data

def write_json(data, filename):
    jsonFile = open(str(cwd)+'/bot_config/'+filename+'.json', 'w+')
    jsonFile.write(json.dumps(data, indent=4)) # Indent = 4 so it looks nice in the file
    jsonFile.close()

@bot.command()
async def stats(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(bot.guilds)
    memberCount = len(set(bot.get_all_members()))
    embed = discord.Embed(title='{} Stats'.format(bot.user.name), description='\uFEFF', colour=ctx.author.colour)
    embed.add_field(name='Bot Version:', value=botVersion)
    embed.add_field(name='Python Version:', value=pythonVersion)
    embed.add_field(name='Discord.Py Version', value=dpyVersion)
    embed.add_field(name='Total Guilds:', value=serverCount)
    embed.add_field(name='Total Users:', value=memberCount)
    embed.add_field(name='Bot Developers:', value="<@271612318947868673> and <@387138288231907329>")
    embed.set_footer(text="Carpe Noctem | {}".format(bot.user.name))
    embed.set_author(name = str(bot.user.name), icon_url = str(bot.user.avatar_url))
    await ctx.send(embed = embed)

def SetupJsonDefaults():
    data = read_json('config')
    data['configs'] = {}
    data['configs']['default'] = {}
    data['configs']['default']['prefix'] = '--'
    data['configs']['default']['userSpamWarningMessage'] = "Stop spamming {message.author.mention}, or I will be forced to take action!"
    data['configs']['default']['userSpamMuteMessage'] = "Hey {message.author.mention}! I have muted you for spam, you will be unmuted at {unmuteTime}."
    write_json(data, 'config')

if __name__ == '__main__':
    bot.run(bot.config_token)
