import discord
from discord.ext import commands
import platform

import cogs._json

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='logout', description='Log the bot out of discord')
    @commands.is_owner()
    async def logout(self, ctx):
        """Log the bot out of discord"""
        await ctx.send("Logging out...")
        await self.bot.logout()

    @commands.command(name='prefix', description='Set your guilds prefix, or check your guilds prefix', usage='*(Optional-New prefix)')
    @commands.is_owner()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def prefix(self, ctx, *, pre=None):
        '''Set a custom prefix for the guild.'''
        data = cogs._json.read_json('config')
        if isinstance(ctx.channel, discord.DMChannel):
            return
        await cogs.util_functions.CheckGuildHasSettings(ctx.guild)
        if not pre:
            await ctx.send(f"The guild prefix is `{data['configs'][str(ctx.guild.id)]['prefix']}` Use `{data['configs'][str(ctx.guild.id)]['prefix']}prefix <prefix>` to change it.")
            return
        data['configs'][str(ctx.guild.id)]['prefix'] = str(pre)
        #update json file for that discord
        cogs._json.write_json(data, 'config')
        await ctx.send(f'The guild prefix has been set to `{pre}` Use `{pre}prefix <prefix>` to change it again.')

    @commands.command(name='ping', description='Gets and sends bot latency')
    async def ping(self, ctx):
        await ctx.send(f"Bot ping: **{round((self.bot.latency) * 1000)}ms**")

    @commands.command(name='stats', description='Sends some bot stats')
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))
        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour)
        embed.add_field(name='Bot Version:', value=self.bot.Version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="<@271612318947868673> and <@387138288231907329>")
        embed.set_footer(text=f"Carpe Noctem | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))
