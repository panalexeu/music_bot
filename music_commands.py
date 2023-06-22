import discord
from discord.ext import commands

import databse
import utils


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = databse.Database()

    @commands.command()
    async def play(self, ctx, url: str):
        """Plays a song from yt from the given url"""

        user = ctx.message.author

        try:
            await user.voice.channel.connect()

            async with ctx.typing():
                self.db.increment_times_played()
                self.db.increment_amount_of_commands_used()

                player = await utils.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
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

    @commands.command()
    async def pause(self, ctx):
        """Pauses a playing song"""

        try:
            self.db.increment_amount_of_commands_used()

            ctx.voice_client.pause()
            await ctx.send(f'Song paused.')
        except AttributeError:
            await ctx.send('Bot is not connected to any voice channel.')

    @commands.command()
    async def resume(self, ctx):
        """Resumes a playing song"""

        try:
            self.db.increment_amount_of_commands_used()

            ctx.voice_client.resume()
            await ctx.send(f'Song resumed.')
        except AttributeError:
            await ctx.send('Bot is not connected to any voice channel.')

    @commands.command()
    async def stop(self, ctx):
        """Stops a playing song"""

        try:
            self.db.increment_amount_of_commands_used()

            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send(f'Song stopped.')
        except AttributeError:
            await ctx.send('Bot is not connected to any voice channel.')
