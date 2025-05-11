#bibliotecas
import discord
from discord.ext import commands,tasks
import importlib
import os
import asyncio
from discord.ui import View, Button
from dotenv import load_dotenv

#setup do bot (Ativa todos os eventos que o bot pode escutar. E o bot é ativo com o prefixo !)
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#quando o bot está ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    prefix = "PLaying"
    try:
        synced = await bot.tree.sync()
        print(f"Comandos de barra sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")
    await bot.change_presence(activity=discord.Game(name=f"{prefix} - Goncas Noob"))
    for server in bot.guilds:
        bot_role = discord.utils.get(server.roles, name="Martemig")
        if bot_role:
            await bot_role.edit(position=0)

#faz load de todos os cogs do bot
async def load():
    cogs_dir = './cogs'
    for file in os.listdir(cogs_dir):
        if file.endswith('.py') and not file.startswith("__"):
            cog_module = f'cogs.{file[:-3]}'
            module = importlib.import_module(cog_module)
            if hasattr(module, 'setup'):
                await module.setup(bot)

#envia mensagem de bem vindo quando user entra no server
@bot.event
async def on_member_join(member):
    await member.guild.text_channels[0].send(f'Bem-vindo, {member.mention}!')


#codigo para correr o bot
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())