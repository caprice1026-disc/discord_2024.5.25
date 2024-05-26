import discord
import discord.ext.commands
import os
import datetime
from server import keep_alive
from discord.ext import commands

TOKEN = os.getenv("API_KEY")
AlchemyURL = os.getenv("Alchemy_KEY")
deadline = datetime.timedelta(days=21)

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
prefix = "/"

class ConfirmationView(discord.ui.View):
   def __init__(self, interaction: discord.Interaction, timeout=60, text=""):
       super().__init__(timeout=timeout)
       self.send_embed = discord.Embed(title="新作の宣伝です！", description=text)
       self.send_embed.set_author(
           name=interaction.user.display_name,
           icon_url=interaction.user.display_avatar.url,
       ).set_footer(
           text=f"transfar from {interaction.user.display_name}",
           icon_url=interaction.user.display_avatar.url,
       )
       self.channel = client.get_channel(907814218227646536)

   @discord.ui.button(label="OK", style=discord.ButtonStyle.success)
   async def ok(self, button: discord.ui.Button, interaction: discord.Interaction):
       await self.channel.send(embed=self.send_embed)
       pass

   @discord.ui.button(label="NG", style=discord.ButtonStyle.gray)
   async def ng(self, button: discord.ui.Button, interaction: discord.Interaction):
       pass

@client.event
async def on_ready():
   print("起動完了")
   await tree.sync()

@tree.command(name="promotion", description="アクティブクリエイターが宣伝するためのコマンドです。")
@discord.app_commands.describe(role="誰に送るかを指定。", text="送りたい文章を書き込んでください。")
async def promotion(interaction: discord.Interaction, role: discord.Role, text: str):
   rolename = role
   view = ConfirmationView(interaction=interaction, text=text)
   await interaction.response.send_message(f"{rolename}へ{text}と送信してよいですか？", ephemeral=True)
   await interaction.followup.send(view=view, ephemeral=True)

@tree.command(name="roleee", description="ロール所持者を出力するコマンドです。")
async def roleee(interaction: discord.Interaction, role: discord.Role):
   rolename = role
   members = rolename.members
   membername = [member.name for member in members]
   await interaction.response.send_message(f"{membername}", ephemeral=True)

async def is_leader(ctx):
   return ctx.author.id == 467684948032356353

@tree.command(name="addcomminitymember", description="コミュニティチームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addcomminitymember(interaction: discord.Interaction, member: discord.Member):
   await member.add_roles(1113451626708074637)
   await interaction.response.send_message(f"{member}にコミュニティチームメンバーのロールを付与しました。", ephemeral=True)

@addcomminitymember.error
async def addcomminitymember_error(ctx, error):
   if isinstance(error, discord.ext.commands.CheckFailure):
       await ctx.send("コミュニティチームリーダーのみが実行できるコマンドです。")
   else:
       raise error
   await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
   return ctx.author.id == 431045993530785793

@tree.command(name="addkouhoumember", description="広報チームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addkomminitymember(interaction: discord.Interaction, member: discord.Member):
   await member.add_roles(1113459650495524874)
   await interaction.response.send_message(f"{member}に広報チームメンバーのロールを付与しました。", ephemeral=True)

@addkomminitymember.error
async def addkouhoumember_error(ctx, error):
   if isinstance(error, discord.ext.commands.CheckFailure):
       await ctx.send("広報チームリーダーのみが実行できるコマンドです。")
   else:
       raise error
   await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
   return ctx.author.id == 658169582246166578

@tree.command(name="addoujinmember", description="同人チームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addoujinmember(interaction: discord.Interaction, member: discord.Member):
   await member.add_roles(1113463872368693318)
   await interaction.response.send_message(f"{member}に同人チームメンバーのロールを付与しました。", ephemeral=True)

@addoujinmember.error
async def adddoujinmember_error(ctx, error):
   if isinstance(error, discord.ext.commands.CheckFailure):
       await ctx.send("同人チームリーダーのみが実行できるコマンドです。")
   else:
       raise error
   await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
   return ctx.author.id == 624760316499841792

@tree.command(name="addbmbmmember", description="bmbmチームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addbmbmmember(interaction: discord.Interaction, member: discord.Member):
   await member.add_roles(1113453177426157578)
   await interaction.response.send_message(f"{member}にbmbmチームメンバーのロールを付与しました。", ephemeral=True)

@addbmbmmember.error
async def addbmbmmember_error(ctx, error):
   if isinstance(error, discord.ext.commands.CheckFailure):
       await ctx.send("広報チームリーダーのみが実行できるコマンドです。")
   else:
       raise error
   await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
   return ctx.author.id == 917252567313055764

@tree.command(name="addshareworldmember", description="シェアワールドチームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addshareworldmember(interaction: discord.Interaction, member: discord.Member):
   await member.add_roles(1113459470148841633)
   await interaction.response.send_message(f"{member}にシェアワールドチームメンバーのロールを付与しました。", ephemeral=True)

@addshareworldmember.error
async def addshareworldmember_error(ctx, error):
   if isinstance(error, discord.ext.commands.CheckFailure):
      await ctx.send("広報チームリーダーのみが実行できるコマンドです。")
   else:
      await ctx.send("bot作成者に聞いてみてね!")
async def on_guild_channel_create(channel):
   role = channel.guild.get_role(1113815534472015965)
   if role:
      await channel.set_permissions(role, read_messages=True)
      async def on_thread_join(thread):
         role = thread.guild.get_role(1113815534472015965)
         if role:
            await thread.set_permissions(role, read_messages=True)
keep_alive()
client.run(TOKEN)