import discord
from discord.ext import commands

import constants
import music_commands

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(music_commands.MusicCommands(bot))

if __name__ == '__main__':
    bot.run(constants.TOKEN)
