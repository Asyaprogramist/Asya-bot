import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import re 
import aiosqlite
load_dotenv()
TOKEN = str(os.getenv("DISCORDTOKEN"))

         




intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

AUTO_ROLE_ID = 1558890247839031338

@bot.event
async def on_member_join(member):
    role =member.guild.get_role(AUTO_ROLE_ID)
    if role is not None:
      try:
            await member.add_roles(role)
            print(f"Роль{role.name} выдана пользователю {member.name}")
      except discord.Forbidden:
          print("Ошибка: У бота нет прав для выдачи этой роли. Проверьте иерархию ролей.")
          


bot = commands.Bot(command_prefix='!', intents=intents)
warnings_db = {}


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f'Синхронизировано {len(synced)} команд.')
    except Exception as e:
        print(e)
    print(f'Бот {bot.user} готов к работе!')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    letters = [c for c in message.content if c.isalpha()]
    if len(letters) > 5 and sum(c.isupper() for c in letters) / len(letters) > 0.7:
        await message.delete()
        await message.channel.send(
            f'{message.author.mention}, пожалуйста, не используйте так много заглавных букв!',
            delete_after=5
        )
        return

    text = message.content.lower()
    if any(word in text for word in BAD_WORDS):
        await message.delete()
        await message.channel.send(
            f'{message.author.mention}, не используйте нецензурные слова!',
            delete_after=5
        )
        return

    await bot.process_commands(message)

AUTO_ROLE_ID = 1558890247839031338

@bot.event
async def on_member_join(member):
    role = await member.guild.fetch_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
            print(f"✅ Роль {role.name} успешно выдана пользователю {member.name}")
        except discord.NotFound:
            print("Роль не найдена. Проверьте ID роли.")
        except discord.Forbidden:
            print('У бота нет прав для выдачи роли.')
        except Exception as e:
            print(f"Произошла ошибка: {e}")
     

@bot.event
async def has_bad_word(text: str) -> bool:
     text_lower = text.lower()
     return any(word in text_lower for word in BAD_WORDS)
async def on_message(message):
    if message.author.bot:
        return
    if has_bad_word(message.content):
        try:
            await message.delete()
        except discord.Forbidden:
            pass
        await message.chennel.send(f'{message.author.mention}, не матерись!', delete_after=5)
        return
    await bot.process_commands(message)    

DB_PATH = 'bot.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS levels (   guild_id INTEGER,
                user_id INTEGER,
                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 0,
                last_xp_time REAL DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
                )
            """)    
        await db.commit()
async def get_user(guild_id: int, user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute( 
           "SELECT xp, level, last_xp_time FROM levels WHERE guild_id=? AND user_id=?",
           (guild_id, user_id)  
        ) as cur:
            row = await cur.fetchone()
            if row is None:
                await db.execute(
                    "INSERT INTO levels (guild_id, user_id) VALUES (?, ?)",
                    (guild_id, user_id)  
                )
    await db.commit()
    return 0,0,0.0
    return row
async def update_user(guild_id: int, user_id: int, xp: int,  level: int, last_time: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
              "UPDATE levels SET xp=?, level=?, last_xp_time=? WHERE guild_id=? AND user_id=?",
              (xp, level, last_time, guild_id,user_id)
        )
    await db.commit()
async def get_leaderboard(guild_id: int, limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT user_id, xp, level FROM levels WHERE guild_id=? ORDER BY xp DESC LIMIT ?",
            (guild_id, limit)
        ) as cur:
            return await cur.fetchall()
    def xp_for_level(level: int) -> int:
        return 5 * (level ** 2) + 50 * level + 100


bot.run(TOKEN)
