import discord
from discord.ext  import commands
import copy

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

def setup(bot):
    bot.add_cog(Events(bot))
