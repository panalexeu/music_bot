import discord
from discord.ext import commands
from discord.ext.commands import errors

import databse
import utils


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.db = databse.Database()

    @commands.command()
    async def play(self, ctx, url: str):
        """Plays a song/video from yt from the given url"""

        # Joining to vc handling
        user = ctx.message.author
        try:
            await user.voice.channel.connect()
        except AttributeError:
            await ctx.send(f'User **{user.name}** is not connected to any voice channel.')
            return
        except discord.ClientException:
            pass

        # Music playing handling
        try:
            async with ctx.typing():
                # Incrementing values in stats db
                self.db.increment_times_played()

                player = await utils.YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player)

                await ctx.send(f'Now playing: **{player.title}**')

        except (discord.ClientException, errors.MissingRequiredArgument) as e:
            await ctx.send(e.__str__())
        except AttributeError:
            pass

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, errors.MissingRequiredArgument):
            await ctx.send('A required argument is missing. Please provide the URL.')

    @commands.command()
    async def pause(self, ctx):
        """Pauses a playing song/video"""

        try:
            ctx.voice_client.pause()
            await ctx.send(f'Song paused.')
        except AttributeError:
            await ctx.send('Bot is not connected to any voice channel.')

    @commands.command()
    async def resume(self, ctx):
        """Resumes a playing song/video"""

        try:
            ctx.voice_client.resume()
            await ctx.send(f'Song resumed.')
        except AttributeError:
            await ctx.send('Bot is not connected to any voice channel.')

    @commands.command()
    async def stop(self, ctx):
        """Stops a playing song/video"""

        try:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send(f'Song stopped.')
        except AttributeError:
            await ctx.send('Bot is not connected to any voice channel.')
