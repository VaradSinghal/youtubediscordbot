import discord
import requests
import asyncio
import os
from dotenv import load_dotenv
from keep_alive import keep_alive 

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_live_video_id = None

async def check_youtube_live():
    global last_live_video_id
    await client.wait_until_ready()
    while not client.is_closed():
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={YOUTUBE_CHANNEL_ID}&eventType=live&type=video&key={YOUTUBE_API_KEY}"
        response = requests.get(url)
        data = response.json()

        if 'items' in data and data['items']:
            live_video = data['items'][0]
            video_id = live_video['id']['videoId']
            title = live_video['snippet']['title']
            link = f"https://www.youtube.com/watch?v={video_id}"

            if video_id != last_live_video_id:
                channel = client.get_channel(DISCORD_CHANNEL_ID)
                if channel:
                    await channel.send(f"🔴 **{title}** is LIVE now!\n📺 Watch here: {link}")
                    last_live_video_id = video_id
        else:
            print("No live video found.")

        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f'✅ Bot is live as {client.user}')
    client.loop.create_task(check_youtube_live())

keep_alive()
client.run(TOKEN)
