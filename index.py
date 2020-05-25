import discord
from discord.ext import commands
import json
import os

TOKEN = 'Bot token here'

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print (f'Logged in as: {bot.user.name}#{bot.user.discriminator} - {bot.user.id}')
    await bot.change_presence(activity=discord.Game(name='Moderation bot - Type .help!'))

@bot.event
async def on_guild_join(guild):
    for member in guild.members:
        if not member.bot:
            with open('warns.json', 'r') as f:
                msg = json.load(f)
                f.close()

            msg[str(member.id)] = '0'

            with open('warns.json', 'w') as r:
                json.dump(msg, r, indent=4)
                f.close()

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')


bot.run(TOKEN)