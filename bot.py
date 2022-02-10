from click import command
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from pymongo import MongoClient

db_url = 'url'
cluster = MongoClient(db_url)
database = cluster["Jarvis"]
database = cluster['flaskapp']



bot = commands.Bot(command_prefix="=")

@bot.command()
async def test(ctx):
    await ctx.reply("Yes test work succesfuly", mention_author=False)

@bot.command()
async def something():
    pass



bot.run(os.environ['BOT_TOKEN'])