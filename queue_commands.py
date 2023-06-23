import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import errors

import databse
import utils


class QueueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.db = databse.Database()

    @commands.command()
    async def q_play(self, ctx):
        # Is empty check if so ending the function
        if len(self.queue) == 0:
            await ctx.send('Queue is empty')
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

        while len(self.queue) > 0:
            player = await utils.YTDLSource.from_url(self.queue.pop(0), loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player)
            await ctx.send(f'Now playing: **{player.title}**')
            await asyncio.sleep(player.data.get('duration'))  # duration is in seconds

    @commands.command()
    async def q_add(self, ctx, url):
        self.queue.append(url)
        await ctx.send('Entry was added to the queue.')

    @q_add.error
    async def q_add_error(self, ctx, error):
        if isinstance(error, errors.MissingRequiredArgument):
            await ctx.send('A required argument is missing. Please provide the URL.')

    @commands.command()
    async def q_clear(self, ctx):
        self.queue.clear()
        await ctx.send('Queue was cleared.')

    @commands.command()
    async def q_list(self, ctx):
        queue_embed = discord.Embed(
            title='Queue list',
            color=discord.Color.red(),
        )

        async with ctx.typing():
            value = ''
            for entry in self.queue:
                value += f'* {entry}\n'

            queue_embed.add_field(
                name='Current queue list:',
                value=value
            )

            await ctx.send(embed=queue_embed)
