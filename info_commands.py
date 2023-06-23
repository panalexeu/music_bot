import discord
from discord.ext import commands

import databse


class InfoCommands(commands.Cog):

    def __init__(self):
        self.db = databse.Database()

    @commands.command()
    async def info(self, ctx):
        """Basic info"""

        info_embed = discord.Embed(
            title='Basic information',
            color=discord.Color.red(),
            description=''
        )

        info_embed.add_field(
            name='Commands syntax',
            value='To use commands follow this syntax: **!command_name** (!play, !resume, !pause, etc.)',
            inline=False
        )
        info_embed.add_field(
            name='Supported commands list',
            value='* !info\n* !play\n* !resume\n* !pause\n* !stop\n* !help',
            inline=False
        )
        info_embed.add_field(
            name='Developer',
            value='alexeu',
            inline=False
        )

        await ctx.send(embed=info_embed)

    @commands.command()
    async def stats(self, ctx):
        """Bot usage statistics"""

        stats_embed = discord.Embed(
            title='Bot usage statistics',
            color=discord.Color.red()
        )

        stats_embed.add_field(
            name='Amount of songs/videos played:',
            value=self.db.get_times_played(),
            inline=True
        )

        async with ctx.typing():
            await ctx.send(embed=stats_embed)
