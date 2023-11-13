import discord
import os
import asyncio
import random
import aiohttp
from discord.ext import commands

token = ""
log_id = 1234567890 # The ID of the Channel where the Logs are getting saved
path = "pictures" # Path where the Pictures are saved
time = 600 # Time between every Automatic Change
# 600 Seconds = 10 Minutes

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

async def download_image(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(filename, "wb") as f:
                    f.write(await response.read())

@bot.event
async def on_ready():
    while True:
        log = bot.get_channel(log_id)
        files = os.listdir(path)
        image_files = [file for file in files if file.lower().endswith(("png", "jpg", "jpeg", "gif"))]

        if not image_files:
            await log.send("No image files found in the folder.")
            return
        
        random_image = random.choice(image_files)
        image_path = os.path.join(path, random_image)

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

            guild = bot.guilds[0]
            await guild.edit(icon=image_data)

        await log.send("Server Icon automaticly changed!")
        print("Server Icon automaticly changed!")
        await asyncio.sleep(time)

@bot.command()
async def skip(ctx):
    log = bot.get_channel(log_id)
    files = os.listdir(path)
    image_files = [file for file in files if file.lower().endswith(("png", "jpg", "jpeg", "gif"))]

    if not image_files:
        await log.send("No image files found in the folder.")
        return
    
    random_image = random.choice(image_files)
    image_path = os.path.join(path, random_image)

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

        guild = bot.guilds[0]
        await guild.edit(icon=image_data)

        await ctx.send("Skipped the current Server Icon!")
        await log.send("Skiped the Server Icon!")

bot.run(token)