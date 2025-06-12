import discord
from discord.ext import commands

from guild_config import fetch_config, set_config, update_archive_category, update_ban_role


class SetupCog(commands.Cog):
    """ギルド初期設定用のコマンドを提供するCog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="setupguild", description="ギルドの初期設定を行います")
    @commands.has_guild_permissions(administrator=True)
    async def setup_guild(
        self,
        ctx: commands.Context,
        archive_category: discord.CategoryChannel,
        ban_role: discord.Role,
    ) -> None:
        """アーカイブ用カテゴリーとBAN除外ロールを登録"""
        await set_config(self.bot.db_engine, ctx.guild.id, archive_category.id, ban_role.id)
        await ctx.reply("設定を保存しました。")

    @commands.hybrid_command(name="setarchive", description="アーカイブカテゴリーを設定します")
    @commands.has_guild_permissions(administrator=True)
    async def set_archive(self, ctx: commands.Context, category: discord.CategoryChannel) -> None:
        await update_archive_category(self.bot.db_engine, ctx.guild.id, category.id)
        await ctx.reply("アーカイブカテゴリーを更新しました。")

    @commands.hybrid_command(name="setbanrole", description="BAN除外ロールを設定します")
    @commands.has_guild_permissions(administrator=True)
    async def set_ban_role(self, ctx: commands.Context, role: discord.Role) -> None:
        await update_ban_role(self.bot.db_engine, ctx.guild.id, role.id)
        await ctx.reply("BAN除外ロールを更新しました。")

    @commands.hybrid_command(name="showconfig", description="現在の設定を表示します")
    async def show_config(self, ctx: commands.Context) -> None:
        conf = await fetch_config(self.bot.db_engine, ctx.guild.id)
        if conf:
            embed = discord.Embed(title="ギルド設定")
            embed.add_field(name="Archive Category", value=f"<#{conf.archive_category_id}>")
            embed.add_field(name="Ban Allow Role", value=f"<@&{conf.ban_allow_role_id}>")
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("設定がまだ登録されていません。")

    @setup_guild.error
    @set_archive.error
    @set_ban_role.error
    async def on_permission_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply("このコマンドは管理者のみ実行できます。")
        else:
            raise error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SetupCog(bot))

