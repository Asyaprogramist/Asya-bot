import discord 
from discord import app_commands
from discord.ext import commands
import datetime
import re
import os 

from dotenv import load_dotenv 
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN") 

intents = discord.Intents.default()
intents.message_content = True
intents = discord.Intents.default()
BAD_WORDS =['мат1', 'мат2', 'плохое_слово']

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.moderation = True

client  = discord.Client(intents=intents) 

bot = commands.Bot(command_prefix='!', intents=intents)
warnings_db ={}

@bot.event
async def on_ready():
  try :
    synced = await bot.tree.sync()
    print(f'Синхронизировано {len(synced)} команд.')
  except Exception as e:
    print(e)
  print(f'Бот {bot.user} готов к работе!') 

@bot.event
async def on_message(message):
  if  message.author.bot:
    return 

  if len (message.content) > 5 and sum(1 for c in message.content if c.isupper()) / len (message.content) > 0.7:
    await message.delete() 
    await message.channel.send(f'{message.author.mention}, Пожалуйста, не используете так много заглавных букв!', delete_after=5)
    return

  await bot.process_commands(message)

@bot.event 
async def on_memder_join(member):
  AUTO_ROLE_ID = 1558890247839031338
  role = member.guild.get_role(AUTO_ROLE_ID)
  if role:
    try:
      await member.add_roles(role)
    except discord.Forbidden:
      print('У бота нет прав для выдача роли.')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

client.run(TOKEN)