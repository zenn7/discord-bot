import os
os.system("pip install flask discord.py python-dotenv PyNaCl")

import discord
from discord.ext import commands
from dotenv import load_dotenv
from threading import Thread
from flask import Flask

# Setup web server buat keep-alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    Thread(target=run).start()

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
VC_ID = int(os.getenv("VOICE_CHANNEL_ID"))

# Setup bot
intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot aktif sebagai {bot.user}")
    try:
        vc_channel = bot.get_channel(VC_ID)
        if vc_channel:
            await vc_channel.connect(reconnect=True)
            print(f"Gabung ke voice: {vc_channel.name}")
        else:
            print("Voice channel gak ketemu. Cek VOICE_CHANNEL_ID.")
    except Exception as e:
        print("Gagal join VC:", e)

@bot.event
async def on_disconnect():
    print("Bot disconnect, coba reconnect...")

# Run bot
keep_alive()
bot.run(TOKEN)
