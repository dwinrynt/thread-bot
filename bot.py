import os
import ssl
import datetime
import discord
import aiohttp
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
sslcontext = ssl.create_default_context()
sslcontext.check_hostname = False
sslcontext.verify_mode = ssl.CERT_NONE
connector = aiohttp.TCPConnector(ssl=sslcontext)
client = discord.Client(connector=connector, intents=intents)

async def wait_until_11_15_am():
    now = datetime.datetime.now()
    desired_time = datetime.time(hour=16, minute=30)
    while now.time() < desired_time:
        await asyncio.sleep(60)  # wait 1 minute before checking the time again
        now = datetime.datetime.now()

@client.event
async def on_ready():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in client.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")
    
async def create_thread_at_11_15_am():
    await wait_until_11_15_am()
    for guild in client.guilds:
        channel = guild.get_channel(1102845672287387668)  # replace CHANNEL_ID with the ID of the channel where you want to create the thread
        if isinstance(channel, discord.TextChannel):
            thread = await channel.create_thread(name='New Thread', type=discord.ChannelType.public, auto_archive_duration=1440)
            await thread.send('@everyone update')
            print(f"Created new public thread: {thread.name} in {channel.name}")
        else:
            print("Invalid channel or channel is not a text channel")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello Dwi Nuryanto!')

    if message.content.startswith('!create_thread'):
        channel = message.channel
        if isinstance(channel, discord.TextChannel):
            thread = await channel.create_thread(
                name='New Thread', 
                auto_archive_duration=1440,
                type=discord.ChannelType.public_thread
            )
            await thread.send('@everyone update')
            await message.channel.send(f"Created new thread: {thread.name} in {channel.name}")
        else:
            await message.channel.send("Invalid channel or channel is not a text channel")



    await bot.process_commands(message)

client.loop.create_task(create_thread_at_11_15_am())
client.run(TOKEN)
