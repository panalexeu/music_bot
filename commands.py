import discord
from discord.ext import commands

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
            ctx.voice_client.play(player)

        await ctx.send(f'Now playing: **{player.title}**')

    except discord.ClientException as e:
        await ctx.send(e.__str__())
    except AttributeError as e:
        error_msg = e.__str__()
        if error_msg == "'NoneType' object has no attribute 'channel'":
            await ctx.send(f'User **{user.name}** is not connected to any voice channel.')
        elif error_msg == "'NoneType' object has no attribute 'play'":
            pass


@bot.command()
async def pause(ctx):
    try:
        ctx.voice_client.pause()
        await ctx.send(f'Bot paused.')
    except AttributeError:
        await ctx.send('Bot is not connected to any voice channel.')


@bot.command()
async def resume(ctx):
    try:
        ctx.voice_client.resume()
        await ctx.send(f'Bot resumed.')
    except AttributeError:
        await ctx.send('Bot is not connected to any voice channel.')


@bot.command()
async def stop(ctx):
    try:
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        await ctx.send(f'Bot stopped.')
    except AttributeError:
        await ctx.send('Bot is not connected to any voice channel.')
