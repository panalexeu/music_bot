import discord
from discord.ext import commands

import constants
import databse

import info_commands
import music_commands
import queue_commands

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(music_commands.MusicCommands(bot))
    await bot.add_cog(queue_commands.QueueCommands(bot))
    await bot.add_cog(info_commands.InfoCommands())

if __name__ == '__main__':
    databse.Database().initialize()
    bot.run(constants.TOKEN)
