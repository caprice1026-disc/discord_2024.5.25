import discord
from discord.ext import commands

class GeneralCog(commands.Cog):
    """一般的なコマンドをまとめたCog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="ping", description="botが応答するか確認します")
    async def ping(self, ctx: commands.Context) -> None:
        """応答確認用コマンド"""
        await ctx.reply("Pong!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GeneralCog(bot))
