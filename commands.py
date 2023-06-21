import discord
from discord.ext import commands

import constants
import music

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def play(ctx, url: str):
    user = ctx.message.author

    try:
        await user.voice.channel.connect()

        async with ctx.typing():
            player = await music.YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.message.guild.voice_client.play(player)

        await ctx.send(f'Now playing: **{player.title}**')

    except discord.ClientException as e:
        await ctx.send(e.__str__())
    except AttributeError:
        await ctx.send(f'User **{user.name}** is not connected to any voice channel.')


@bot.command()
async def pause(ctx):
    try:
        await ctx.message.guild.voice_client.pause()
    except AttributeError:
        await ctx.send('Bot is not connected to any voice channel.')


@bot.command()
async def resume(ctx):
    try:
        await ctx.message.guild.voice_client.resume()
    except AttributeError:
        await ctx.send('Bot is not connected to any voice channel.')


@bot.command()
async def stop(ctx):
    try:
        await ctx.message.guild.voice_client.stop()
        await ctx.message.guild.voice_client.disconnect()
    except AttributeError:
        await ctx.send('Bot is not connected to any voice channel.')
