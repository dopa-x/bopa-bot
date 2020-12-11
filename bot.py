# bot.py
import os
import discord
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
prefix = '.'
client = commands.Bot(command_prefix=prefix)

#Uses a .env to access it's discord token to prevent token stealing.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#Put a user ID as any of these variables to target it.
dopa = 318151890405687296
DV_list = []
GONE_list = []
ACCESS_list = [dopa]



async def log_print(text):
    print(text)
    with open('log.txt', 'a') as log_file:
        log_file.write(text + "\n")
        
@client.event
async def on_ready():
    await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' ' + f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your every move!"))
    
@client.command(name='s')
async def say(message):
    if (message.author.id in ACCESS_list):
        text = message.message.content.replace(".s", "")
        await message.send(text)
        await message.message.delete()
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' Said \"' + text + '\"!')

@client.command(name='op')
async def op(message, text):
    if (message.author.id == dopa):
        strippedtext = int(text.strip('<>!@'))
        ACCESS_list.append(strippedtext)
        await message.message.delete()
        strippedtext = str(strippedtext)
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' Gave \"' + strippedtext + '\" permissions!')
        
@client.command(name='deop')
async def deop(message, text):
    if (message.author.id == dopa):
        strippedtext = int(text.strip('<>!@'))
        ACCESS_list.remove(strippedtext)
        await message.message.delete()
        strippedtext = str(strippedtext)
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' Took away \"' + strippedtext + '\"\'s permissions!')
        
@client.command(name='dv')
async def downvote(message, text):
    if (message.author.id in ACCESS_list):
        strippedtext = int(text.strip('<>!@'))
        DV_list.append(strippedtext)
        await message.message.delete()
        strippedtext = str(strippedtext)
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' Added \"' + strippedtext + '\" to the DV list!')
        
@client.command(name='sdv')
async def sdownvote(message, text):
    if (message.author.id in ACCESS_list):
        strippedtext = int(text.strip('<>!@'))
        DV_list.remove(strippedtext)
        await message.message.delete()
        strippedtext = str(strippedtext)
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' Removed \"' + strippedtext + '\" from the DV list!')
        
@client.command(name='g')
async def goneify(message, text):
    if (message.author.id in ACCESS_list):
        strippedtext = int(text.strip('<>!@'))
        GONE_list.append(strippedtext)
        await message.message.delete()
        strippedtext = str(strippedtext)
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' Added \"' + strippedtext + '\" to the GONE list!')
             
@client.command(name='sg')
async def ungoneify(message, text):
    if (message.author.id in ACCESS_list):
        strippedtext = int(text.strip('<>!@'))
        GONE_list.remove(strippedtext)
        await message.message.delete()
        strippedtext = str(strippedtext)
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' Removed \"' + strippedtext + '\" from the GONE list!')
        
@client.event 
async def on_message(message): 
    if message.channel.type == discord.enums.ChannelType.private:
        return
    ID = str(message.author.name)
    LINEBREAK = str(message.content)
    CONTENT = LINEBREAK.replace('\n', ' \\n ')
    CHANNEL = str(message.channel.name)
    if (message.author.id != dopa):
        if message.author == client.user:
            return
        if (message.author.id in GONE_list):
            await message.delete()
            CONTENT = str(message.content)
            await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' (#' + CHANNEL + ') ' + ID + ': ' + CONTENT + ' [G]')
        if (message.author.id in DV_list):
            await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' (#' + CHANNEL + ') ' + ID + ': ' + CONTENT + ' [DV]')
            reaction = '<:downvote:713550522635780168>'
            await message.add_reaction(emoji=reaction)
        else:
            if (message.author.id not in GONE_list):               
                await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' (#' + CHANNEL + ') ' + ID + ': ' + CONTENT)
    else:
        await log_print('[' + datetime.now().strftime("%x %X") + ']' + ' (#' + CHANNEL + ') ' + ID + ': ' + CONTENT);
    await client.process_commands(message)


    

client.run(TOKEN)

