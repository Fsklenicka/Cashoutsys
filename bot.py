import discord
import requests
from discord.ext import commands

# Hardcoded sensitive data (Use with caution)
TOKEN = 'MTI1MTEyODIxNzczMDAyMzUwNQ.GoppQp.AXTs0oKEuRCVimHSOpifAWsTDMTrzvPEXShIk4'  # Replace with your actual token
SERVER_URL = 'http://127.0.0.1:5000'  # Replace with your actual server URL

intents = discord.Intents.default()
intents.messages = True  # Enable the intents required
intents.message_content = True  # Enable message content intent

# Initializing bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    print(f'Error occurred: {error}')

@bot.command(name='cashout')
async def cashout(ctx):
    user_id = str(ctx.author.id)
    try:
        response = requests.post(f'{SERVER_URL}/cashout', json={'user_id': user_id})
        response.raise_for_status()
        await ctx.send(response.json()['message'])
    except requests.RequestException as e:
        await ctx.send('Failed to process cashout. Please try again later.')
        print(f'Error during cashout: {e}')

@bot.command(name='money')
async def money(ctx):
    user_id = str(ctx.author.id)
    try:
        response = requests.get(f'{SERVER_URL}/get_earnings')
        response.raise_for_status()
        data = response.json()
        if user_id in data:
            earnings = data[user_id]['earnings']
            await ctx.send(f'Your earnings: ${earnings}')
        else:
            await ctx.send('No earnings found.')
    except requests.RequestException as e:
        await ctx.send('Failed to retrieve earnings. Please try again later.')
        print(f'Error during earnings retrieval: {e}')

# Running the bot with the hardcoded token
bot.run(TOKEN)
