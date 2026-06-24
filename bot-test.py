import os
import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
            return

    if message.content.startswith(('hello', 'Hello', 'Hi', 'hi')):
            await message.channel.send('Hi there! I\'m Kaguya!')

    if message.content.startswith(('bye', 'Bye', 'Goodbye', 'goodbye')):
            await message.channel.send('See you later!')

    if message.content.startswith((':)', ':D', 'XD', 'xD', ':>')):
            await message.channel.send('I see you\'re happy!')

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)
