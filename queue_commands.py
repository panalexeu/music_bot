import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import errors

import databse
import utils


class QueueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.db = databse.Database()

    @commands.command()
    async def q_play(self, ctx):
        """PLays songs/videos from queue list"""

        # Is empty check if so ending the function
        if not await self.is_queue_exist(ctx) or len(self.queue[ctx.guild.id]) == 0:
            await ctx.send('Queue is empty.')
            return

        # Joining to vc handling
        user = ctx.message.author
        try:
            await user.voice.channel.connect()
        except AttributeError:
            await ctx.send(f'User **{user.name}** is not connected to any voice channel.')
            return
        except discord.ClientException:
            pass

        server_queue = self.queue[ctx.guild.id]
        while len(server_queue) > 0:
            try:
                # Incrementing values in stats db
                self.db.increment_times_played()

                player = await utils.YTDLSource.from_url(server_queue.pop(0), loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player)

                await ctx.send(f'Now playing: **{player.title}**')
                await asyncio.sleep(player.data.get('duration'))  # duration is in seconds

            except discord.ClientException as e:
                await ctx.send(e.__str__())
                return

    @commands.command()
    async def q_add(self, ctx, url):
        """Adds a song/video url to queue list"""

        if not await self.is_queue_exist(ctx):
            self.queue[ctx.guild.id] = []  # if query doesn't exist in the guild we create a new one with empty list

        self.queue[ctx.guild.id].append(url)
        await ctx.send('Entry was added to the queue.')

    @q_add.error
    async def q_add_error(self, ctx, error):
        if isinstance(error, errors.MissingRequiredArgument):
            await ctx.send('A required argument is missing. Please provide the URL.')

    @commands.command()
    async def q_clear(self, ctx):
        """Clears queue list"""

        # Is empty check if so ending the function
        if not await self.is_queue_exist(ctx) or len(self.queue[ctx.guild.id]) == 0:
            await ctx.send('Queue is empty.')
            return

        self.queue[ctx.guild.id].clear()
        await ctx.send('Queue was cleared.')

    @commands.command()
    async def q_list(self, ctx):
        """Shows queue list"""

        if not await self.is_queue_exist(ctx):
            await ctx.send('Queue is empty.')
            return

        queue_embed = discord.Embed(
            title=f'{ctx.guild.name} queue list',
            color=discord.Color.red(),
        )

        async with ctx.typing():
            # Parsing the values of requested songs so they look good
            value = ''
            for entry in self.queue[ctx.guild.id]:
                value += f'* {entry} **|** requested by: **{ctx.message.author.name}** **|**\n'

            queue_embed.add_field(
                name='Current queue list:',
                value=value
            )

            await ctx.send(embed=queue_embed)

    async def is_queue_exist(self, ctx):
        return ctx.guild.id in self.queue
