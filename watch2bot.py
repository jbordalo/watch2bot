import discord
import os
import requests
from dotenv import load_dotenv

ROOM_URL = 'https://w2g.tv/rooms/'
PROMPT = '-w '
YOUTUBE = 'https://www.youtube.com/watch?'

load_dotenv()

url = 'https://api.w2g.tv/rooms/create.json'

client = discord.Client()


def print_error():
	return "Aw, let's try that again!\nUsage: `-w https://www.youtube.com/watch?v=1zTbVRPh5EI`"


def print_room(key):
	room = "%s%s" % (ROOM_URL, key)
	return "Here\'s your room, enjoy the party:\n%s" % room


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith(PROMPT):
		yt_link = message.content.split()[1]	

		if not yt_link.startswith(YOUTUBE):
			await message.channel.send(print_error())
			return

		payload = {'w2g_api_key': os.getenv('WATCH_API_KEY'), 'share': yt_link}
		r = requests.post(url, data=payload)
		
		await message.channel.send(print_room(r.json()['streamkey']))

client.run(os.getenv('DISCORD_API_KEY'))
