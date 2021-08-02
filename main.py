import os
import discord
import random
from discord.ext import commands
from alive import keep_alive
from discord.ext import slash

prefix = '/'
activity = discord.Activity(type=discord.ActivityType.watching, name="Math's Community")
client = commands.Bot(command_prefix=prefix, activity=activity, status=discord.Status.online)
client.remove_command("help")
line = "'"

@client.event
async def on_ready():
  print('Bot is ready.')

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please pass all required arguments.')

@client.command()
async def ping(ctx):
  embed=discord.Embed(title='Pong!', color=0xe74c3c)
  embed.add_field(name='Ping is', value=f'{round(client.latency * 1000)}ms')
  message = await ctx.send(embed=embed)

@client.command(aliases=['8ball', 'eightball'])
async def _thiscommanddoesnotexist(ctx, *, question):
  responses = ['Don’t count on it',
    'Outlook not so good',
    'My sources say no',
    'Very doubtful',
    'My reply is no',
    'Reply hazy try again',
    'Better not tell you now',
    'Ask again later',
    'Cannot predict now',
    'Concentrate and ask again',
    'It is certain',
    'Without a doubt',
    'You may rely on it',
    'Yes definitely',
    'It is decidedly so',
    'As I see it, yes',
    'Most likely',
    'Yes',
    'Outlook good',
    'Signs point to yes',
]
  embed=discord.Embed(title=f'{question}', color=0xe74c3c)
  embed.add_field(name='Answer', value=f'{random.choice(responses)}')
  message = await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed=discord.Embed(title='Help', color=0xe74c3c)
    embed.add_field(name='What am I?', value='I' + line + 'm a custom bot made by Math.')
    embed.add_field(name='Commands', value='8ball: Just a regular 8ball.\nping: A command to ping the bot.\nHelp: A command to show help info.')
    message = await ctx.send(embed=embed)


keep_alive()
client.run(os.environ['token'])