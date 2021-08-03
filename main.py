import os
import discord
import random
import json
import time
from discord.ext import commands
from alive import keep_alive
from discord_slash import SlashCommand

line = "'"
prefix = "%"
activity = discord.Activity(type=discord.ActivityType.listening, name="Math's Community")
client = commands.Bot(command_prefix=prefix, activity=activity, status=discord.Status.online,intents=discord.Intents.all())
client.remove_command("help")
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
  print('Bot is ready.')

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
      embed=discord.Embed(title='Prefix', description='The current prefix is ' + prefix + '.\nConfused why you got this message? Well you pinged me!', color=0xe74c3c)
      await message.channel.send(embed=embed)
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please pass all required arguments.')

@client.event
async def on_raw_reaction_add(payload):

  if payload.member.bot:
    pass

  else:
    
    with open('rr.json') as rr_file:

      data = json.load(rr_file)
      for x in data:
        if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
          role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])

          await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
  with open('rr.json') as rr_file:
     data = json.load(rr_file)
     for x in data:
      if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
        role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])
        await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

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
  embed=discord.Embed(title=f'{question}', description = random.choice(responses),  color=0xe74c3c)
  message = await ctx.send(embed=embed)

@slash.slash(description="A simple 8ball.")
async def eightball(ctx, *, question):
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
  embed=discord.Embed(title=f'{question}', description = random.choice(responses),  color=0xe74c3c)
  message = await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    embed=discord.Embed(title='Pong!', description=f'The ping is {round(client.latency * 1000)}ms', color=0xe74c3c)
    message = await ctx.send(embed=embed)

@slash.slash(description="Check the latency of the bot.")
async def ping(ctx):
    embed=discord.Embed(title='Pong!', description=f'The ping is {round(client.latency * 1000)}ms', color=0xe74c3c)
    message = await ctx.send(embed=embed)

@client.command()
async def prefix(ctx):
  await message.channel.send("prefix will be removed, this is just a place holder until i reset the slash commands")

@slash.slash(description="not usable")
async def prefix(ctx):
  await message.channel.send("prefix will be removed, this is just a place holder until i reset the slash commands, just ping the bot")

@client.command()
async def help(ctx):
    embed=discord.Embed(title='Help', color=0xe74c3c)
    embed.add_field(name='What am I?', value='I' + line + 'm a custom bot made by Math.\nUpdate: Slash Commands have been added!.')
    embed.add_field(name='Commands', value='8ball: Just a regular 8ball.\nping: A command to ping the bot.\nHelp: A command to show help info.\nPrefix: Shows the current prefix, same can be done by pinging the bot.\nRR: Reaction Role (staff only + beta).')
    message = await ctx.send(embed=embed)

@slash.slash(description="Help for all of the commands.")
async def help(ctx):
    embed=discord.Embed(title='Help', color=0xe74c3c)
    embed.add_field(name='What am I?', value='I' + line + 'm a custom bot made by Math.\nLatest Update: Slash commands have been added!')
    embed.add_field(name='Commands', value='8ball: Just a regular 8ball.\nping: A command to ping the bot.\nHelp: A command to show help info.\nPrefix: Shows the current prefix, same can be done by pinging the bot.\nRR: Reaction Role (staff only + beta).')
    message = await ctx.send(embed=embed)

@client.command()
@commands.has_any_role("Owner", "Admin")
async def rr(ctx, emoji, role: discord.Role,*, message):
    embed=discord.Embed(title=message, color=0xe74c3c)
    message = await ctx.send(embed=embed)
    await message.add_reaction(emoji)

    with open('rr.json') as json_file:
      data = json.load(json_file)

      new_rr = {
        'role_name':role.name,
        'role_id':role.id,
        'emoji':emoji,
        'message_id':message.id
      }

      data.append(new_rr)


    with open('rr.json','w') as j:
      json.dump(data,j,indent=4)

@client.command()
@commands.has_any_role("Owner", "Admin")
async def rem(ctx, emoji, role: discord.Role, message):
    await message.add_reaction(emoji)

    with open('rr.json') as json_file:
      data = json.load(json_file)

      new_rr = {
        'role_name':role.name,
        'role_id':role.id,
        'emoji':emoji,
        'message_id':message
      }

      data.append(new_rr)


    with open('rr.json','w') as j:
      json.dump(data,j,indent=4)

 
keep_alive()
client.run(os.environ['token'])
