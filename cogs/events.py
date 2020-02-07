import discord
from discord.ext  import commands
import copy
import datetime

import cogs._json
import cogs.util_functions

class Events(commands.Cog):

    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        done = await cogs.util_functions.SetupGuildDefaultConfig(guild)
        if done:
            await cogs.util_functions.SendGlobalLog(self.bot,
            f'Created dataset for guild: {guild.name}\nReason: on_guild_join event')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if self.bot.delete_guild_data_on_remove == True:
            done = await cogs.util_functions.DeleteGuildSettings(str(guild.id))
            if done:
                await cogs.util_functions.SendGlobalLog(self.bot,
                f'Deleted dataset for guild: {guild.name}\nReason: on_guild_remove event')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await cogs.util_functions.CheckGuildHasSettings(member.guild)
        data = cogs._json.read_json('config')
        if data['configs'][str(member.guild.id)]['welcomer'] == True:
            if data['configs'][str(member.guild.id)]['welcomeChannelId'] == None:
                if data['configs'][str(member.guild.id)]['auditChannelId'] != None:
                    channel = self.bot.get_channel(int(data['configs'][str(member.guild.id)]['auditChannelId']))
                    await channel.send(content="Hey! You have welcomer turned on however you have not set the welcome channel. Please set this asap using the settings command! @here")
                else:
                    guildOwner = member.guild.owner
                    await guildOwner.send(content='Hey! You have welcomer turned on however you have not set the welcome channel. Please set this asap using the settings command!')
                return

            welcomeMessage = data['configs'][str(member.guild.id)]['welcomeMessage']
            welcomeMessage = await cogs.util_functions.StringReplaceConfigMessages(string=welcomeMessage, guild=member.guild, member=member)
            color = await cogs.util_functions.RandomEmbedColor(self)
            embed = discord.Embed(description=welcomeMessage, color=color)
            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
            embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(int(data['configs'][str(member.guild.id)]['welcomeChannelId']))
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        await cogs.util_functions.CheckGuildHasSettings(member.guild)
        data = cogs._json.read_json('config')
        if data['configs'][str(member.guild.id)]['welcomer'] == True:
            if data['configs'][str(member.guild.id)]['welcomeChannelId'] == None:
                if data['configs'][str(member.guild.id)]['auditChannelId'] != None:
                    channel = self.bot.get_channel(int(data['configs'][str(member.guild.id)]['auditChannelId']))
                    await channel.send(content="Hey! You have welcomer turned on however you have not set the welcome channel. Please set this asap using the settings command! @here")
                else:
                    guildOwner = member.guild.owner
                    await guildOwner.send(content='Hey! You have welcomer turned on however you have not set the welcome channel. Please set this asap using the settings command!')
                return

            leaveMessage = data['configs'][str(member.guild.id)]['leaveMessage']
            leaveMessage = await cogs.util_functions.StringReplaceConfigMessages(string=leaveMessage, guild=member.guild, member=member)
            color = await cogs.util_functions.RandomEmbedColor(self)
            embed = discord.Embed(description=welcomeMessage, color=color)
            embed.set_thumbnail(url=f'{member.avatar_url}')
            embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
            embed.set_footer(text=f'{member.guild}', icon_url=f'{member.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(int(data['configs'][str(member.guild.id)]['welcomeChannelId']))
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
