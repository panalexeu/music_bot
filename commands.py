import asyncio

import discord
from discord.ext import commands

import constants
import youtube

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def play(ctx, url: str):
    user = ctx.message.author

    try:
        await user.voice.channel.connect()

        async with ctx.typing():
            filename = await youtube.YTDLSource.from_url(url, loop=bot.loop)
            ctx.message.guild.voice_client.play(
                discord.FFmpegPCMAudio(executable=constants.FFMPEG_PATH, source=filename))

    except discord.ClientException as e:
        await ctx.send(e.__str__())
    except AttributeError:
        await ctx.send(f'User **{user.name}** is not connected to any voice channel')
