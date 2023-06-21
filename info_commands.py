import discord
from discord.ext import commands


class InfoCommands(commands.Cog):
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
