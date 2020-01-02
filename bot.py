import discord
from discord.ext import commands
import pathlib
from pathlib import Path
import json
import asyncio

#Printing the current working directory just cos
cwd = Path(__file__).parents[0]
print(cwd)

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("-")(bot, message)
    data = read_json('discordConfig')
    did = '{}'.format(message.guild.id)
    if did not in data:
        return commands.when_mentioned_or("-")(bot, message)
    prefix = data[did]['prefix']
    return commands.when_mentioned_or(prefix)(bot, message)

config_file = json.load(open(str(cwd)+'/bot_config/config.json'))
secret_file = json.load(open(str(cwd)+'/bot_config/secrets.json'))
prefix = config_file['configs']['default']['prefix']
bot = commands.Bot(command_prefix=prefix, owner_id=271612318947868673)
bot.config_token = secret_file['token']

botVersion = "0.0.1"

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: {prefix}\n-----")
    await bot.change_presence(activity=discord.Game(name="Playing with dpy anti spam"))

@bot.command()
@commands.has_role('Dev')
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
    jsonFile.write(json.dumps(data,indent=4))
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
    embed.add_field(name='Bot Developer:', value="<@271612318947868673>")
    embed.set_footer(text="Carpe Noctem | {}".format(bot.user.name))
    embed.set_author(name = str(bot.user.name), icon_url = str(bot.user.avatar_url))
    await ctx.send(embed = embed)

if __name__ == '__main__':
    advertising_script.start()
    bot.run(bot.config_token)
