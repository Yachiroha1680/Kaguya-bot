import os
import discord
import logging
import time
from discord.ext import commands
from dotenv import load_dotenv
from call_api import Kaguya

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '0'))

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.presences = True
intents.members = True  

client = discord.Client(intents=intents)
kaguya = Kaguya()

# --- RATE LIMIT CONFIGURATION ---
MAX_RPM = 5           # Maximum requests allowed per minute (Adjust based on your Gemini tier)
request_history = []  # Stores timestamps of recent API calls

def is_rate_limited() -> bool:
    """Checks if the bot has exceeded the allowed Requests Per Minute."""
    current_time = time.time()
    global request_history
    
    # Clean up timestamps older than 60 seconds
    request_history = [t for t in request_history if current_time - t < 60]
    
    # If we haven't reached the limit, allow the request
    if len(request_history) < MAX_RPM:
        request_history.append(current_time)
        return False
        
    return True
# --------------------------------

def is_target_channel(channel):
    print(f"Checking channel: {channel.id}, Target channel: {CHANNEL_ID}")
    return CHANNEL_ID != 0 and channel.id == CHANNEL_ID
# --------------------------------

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    greeting = kaguya.greet()
    target = client.get_channel(CHANNEL_ID)
    if target and isinstance(target, discord.TextChannel) and target.permissions_for(target.guild.me).send_messages:
        await target.send(greeting)

@client.event
async def on_member_join(member):
    try:
        await member.send(f'{member.name}, Tsukuyomi e yokoso!')
    except discord.Forbidden:
        pass

@client.event
async def on_member_remove(member):
    try:
        await member.send(f'Sayonara {member.name}, I hope to see you again :<')
    except discord.Forbidden:
        pass

@client.event
async def on_presence_update(before, after):
    if before.status == discord.Status.offline and after.status == discord.Status.online:
        target = client.get_channel(CHANNEL_ID)
        if target and isinstance(target, discord.TextChannel) and target.permissions_for(target.guild.me).send_messages:
            await target.send(f'Welcome back {after.mention}! How was your day? *Smiles*')

@client.event
async def on_message(message):    
    if message.author == client.user:
        return

    is_target = is_target_channel(message.channel)
    is_mentioned = client.user.mentioned_in(message)

    if not is_target and not is_mentioned:
        return

    clean_content = message.content
    if is_mentioned:
        clean_content = clean_content.replace(f'<@{client.user.id}>', '').replace(f'<@!{client.user.id}>', '').strip()

    if clean_content.lower().startswith("yo"):
        await message.channel.send("*Smiles*")
        return

    # --- RATE LIMIT CHECK ---
    if is_rate_limited():
        # Inform the user without calling the Gemini API
        await message.channel.send("⏱️ *Hold on! I'm processing too many cosmic requests right now. Please slow down a bit!*")
        return
    # ------------------------

    print(f"Message from {message.author}: {clean_content}")
    
    if not clean_content:
        clean_content = "Hello!"

    response = await kaguya.respond(clean_content)
    await message.channel.send(response)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if not is_target_channel(reaction.message.channel):
        return

    emoji = reaction.emoji
    if isinstance(emoji, (discord.Emoji, discord.PartialEmoji)) and emoji.id:
        emoji = client.get_emoji(emoji.id) or emoji

    try:
        await reaction.message.add_reaction(emoji)
    except discord.HTTPException:
        pass

client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)