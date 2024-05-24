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
#鯖設定するなら　guild = discord.guild(id=)
class confomationview(discord.ui.View):
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
        #チャンネルID書き換えること
        self.channel = client.get_channel(907814218227646536)
    @discord.ui.button(label="OK", style=discord.ButtonStyle.success)
    async def ok(self, button: discord.ui.Button, interaction: discord.Interaction):
        #Embedの中身を指定すること
        await self.channel.send(embed=self.send_embed)
        pass
    @discord.ui.button(label="NG", style=discord.ButtonStyle.gray)
    async def ng(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass
    
@client.event
async def on_ready():
    print("起動完了")
    await tree.sync()
    """for guild in client.guilds:
        for category in guild.categories:
            for channel in category.channels:
                last_message = channel.last_message
                if last_message is None or last_message.created_at < deadline:
                    await channel.archive()
                    await channel.send("しばらく書き込みがなかったので、御負担のないようアクティブクリエイター以上でないと見れないカテゴリーに移動しました。\n\nなにか書き込んで頂けたらすぐに復活しますので、気が向いたとき、お時間が出来た時にでもお気軽に書きこんでくださいね🥰 \n\nアクティブクリエイターの権限が上がって、Everyone通知も出来るようになっています。宣伝等にもご活用いただけましたら幸いです✨")"""

@tree.command(name="promotion",description="アクティブクリエイターが宣伝するためのコマンドです。")
@discord.app_commands.describe(role="誰に送るかを指定。",text="送りたい文章を書き込んでください。")
async def promotion(interaction: discord.Interaction,role: discord.Role,text: str):
    #ここで一回確認を取りたい　フォローアップ関数だとエラーを吐く
    #rolenameの定義の仕方(問題なし)
    rolename = role
    view = confomationview(interaction=interaction, text=text,)
    #Interaction.response.send_message()
    await interaction.response.send_message(f"{rolename}へ{text}  　　と送信してよいですか？", ephemeral=True)
    await interaction.followup.send(view=view, ephemeral=True)


@tree.command(name="roleee",description="ロール所持者を出力するコマンドです。")
async def roleee(interaction: discord.Interaction,role: discord.Role):
    #ロールの名前を取得
    rolename = role
    #ロールのメンバーを取得
    members = rolename.members
    #メンバーの名前を取得
    membername = [member.name for member in members]
    #メンバーの名前を改行で区切って出力
    await interaction.response.send_message(f"{membername}", ephemeral=True)

"""可能だが2000文字以上の出力は止められることに留意すること
@tree.command(name="holder",description="NFT所持者を出力するコマンドです。")
async def holder(interaction: discord.Interaction,token: str):
    url = f"{AlchemyURL}/getOwnersForCollection?contractAddress={token}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    await interaction.response.send_message(f"{response.text}", ephemeral=True)

自動アーカイブ
@client.event
async def on_ready():
    for guild in client.guilds:
        for category in guild.categories:
            for channel in category.channels:
                last_message = channel.last_message
                if last_message is None or last_message.created_at < datetime.now() - timedelta(days=7):
                    await channel.archive()
                    await channel.send("This channel has been archived due to inactivity.")

"""
async def is_leader(ctx):
    #ここでロールのIDを指定すること
    return ctx.author.id == 467684948032356353
@tree.command(name="addcomminitymember",description="コミュニティチームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addcomminitymember(interaction: discord.Interaction,member: discord.Member):
    await member.add_roles(1113451626708074637)
    await interaction.response.send_message(f"{member}にコミュニティチームメンバーのロールを付与しました。", ephemeral=True)
    #例外を追加
@addcomminitymember.error
async def addcomminitymember_error(ctx, error):
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("コミュニティチームリーダーのみが実行できるコマンドです。")
    else:
        raise error
    await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
    #ここでロールのIDを指定すること
    return ctx.author.id == 431045993530785793
@tree.command(name="addkouhoumember",description="広報チームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addcomminitymember(interaction: discord.Interaction,member: discord.Member):
    await member.add_roles(1113459650495524874)
    await interaction.response.send_message(f"{member}に広報チームメンバーのロールを付与しました。", ephemeral=True)
    #例外を追加
@addcomminitymember.error
async def addkouhoumember_error(ctx, error):
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("広報チームリーダーのみが実行できるコマンドです。")
    else:
        raise error
    await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
    #ここでロールのIDを指定すること
    return ctx.author.id == 658169582246166578
@tree.command(name="addoujinmember",description="同人チームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addcomminitymember(interaction: discord.Interaction,member: discord.Member):
    await member.add_roles(1113463872368693318)
    await interaction.response.send_message(f"{member}に同人チームメンバーのロールを付与しました。", ephemeral=True)
    #例外を追加
@addcomminitymember.error
async def adddoujinmember_error(ctx, error):
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("同人チームリーダーのみが実行できるコマンドです。")
    else:
        raise error
    await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
    #ここでロールのIDを指定すること
    return ctx.author.id == 624760316499841792
@tree.command(name="addbmbmmember",description="bmbmチームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addcomminitymember(interaction: discord.Interaction,member: discord.Member):
    await member.add_roles(1113453177426157578)
    await interaction.response.send_message(f"{member}にbmbmチームメンバーのロールを付与しました。", ephemeral=True)
      #例外を追加
@addcomminitymember.error
async def addbmbmmember_error(ctx, error):
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("広報チームリーダーのみが実行できるコマンドです。")
    else:
        raise error
    await ctx.send("bot作成者に聞いてみてね!")

async def is_leader(ctx):
    #ここでロールのIDを指定すること
    return ctx.author.id == 917252567313055764
@tree.command(name="addshareworldmember",description="シェアワールドチームリーダー限定のコマンドです。")
@discord.app_commands.describe(member="誰に付与するかを指定。")
@discord.ext.commands.check(is_leader)
async def addcomminitymember(interaction: discord.Interaction,member: discord.Member):
    await member.add_roles(1113459470148841633)
    await interaction.response.send_message(f"{member}にシェアワールドチームメンバーのロールを付与しました。", ephemeral=True)
    #例外を追加
@addcomminitymember.error
async def addshareworldmember_error(ctx, error):
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.send("広報チームリーダーのみが実行できるコマンドです。")
    else:
        raise error
    await ctx.send("bot作成者に聞いてみてね!")

async def on_guild_channel_create(channel):
    role = channel.guild.get_role(1113815534472015965)  # ロールIDを整数として指定
    if role:
        await channel.set_permissions(role, read_messages=True)

async def on_thread_join(thread):
    role = thread.guild.get_role(1113815534472015965)  # ロールIDを整数として指定
    if role:
        await thread.set_permissions(role, read_messages=True)

# ここからスパム対策コードを書き始める

keep_alive()

client.run(TOKEN)