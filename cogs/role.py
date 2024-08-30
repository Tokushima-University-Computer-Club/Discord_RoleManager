import discord
import os
import sys
from typing import Literal
from discord import app_commands
from discord.ext import commands
from os.path import join, dirname
from dotenv import load_dotenv

# 環境変数の取得
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)
guild_id = int(os.environ.get("GUILD_ID"))

cache = f'{os.getcwd()}/auto_given_roleID'

# コマンドの本体
class role(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        #tokenやidの取得
        self.guild: discord.Guild = self.bot.get_guild(guild_id)

        await self.bot.tree.sync(guild=self.guild)

    @app_commands.command(
        name="tucc-role",
        description="ユーザのロールを制御します"
    )
    @app_commands.guilds(guild_id)
    async def role(self, ctx: discord.Interaction, option: Literal['give', 'remove', 'auto'], user: discord.Member = None, role: discord.Role = None):
        # ユーザに指定されたロールを付与する
        if option == 'give':
            if not(role in user.roles):  # ユーザが指定されたロールをもっていない場合のみ発火
                await user.add_roles(role)
                await ctx.response.send_message(f'{user.name} に {role.name} ロールを与えました', ephemeral=True)
            else:
                await ctx.response.send_message(f'{user.name} は {role.name} ロールをすでに持っています', ephemeral=True)
        # ユーザから指定されたロールを削除する
        elif option == 'remove':
            if role in user.roles:      # ユーザが指定されたロールをもっている場合のみ発火
                await user.remove_roles(role)
                await ctx.response.send_message(f'{user.name} から {role.name} ロールを削除しました', ephemeral=True)
            else:
                await ctx.response.send_message(f'{user.name} は {role.name} ロールを持っていません', ephemeral=True)
        # 新規参加者に自動で付与するロールを変更する
        elif option == 'auto':
            # キャッシュにロールIDを書き込む
            with open(cache, mode='w') as f:
                f.write(str(role.id))
            await ctx.response.send_message(f'新規参加者に自動で {role.name} ロールを付与します', ephemeral=True)
            
    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        #try:
            with open(cache, "r") as f:
                given_role = self.guild.get_role(int(f.readline()))
                await member.add_roles(given_role)
        #except:
            #print("自動付与ロールが読み込めませんでした")
            #sys.stdout.flush()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        role(bot)
    )