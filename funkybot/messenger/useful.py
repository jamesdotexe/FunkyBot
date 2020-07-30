#==== Description ====
"""
Sends messages to Discord from useful commands
"""

#==== Imports ====
from funktions import useful
import asyncio
import discord

#==== Setup a reminder for everyone ====
async def announce(message,client):
    if message.author.guild_permissions.administrator:
        reminder = useful.makeReminder(message, announcement=True)

        await message.channel.send(useful.confirmReminder(message, reminder))

        def pred(msg):
            return (msg.author == message.author and
                    msg.channel == message.channel and
                    (msg.content.upper().startswith('!YES') or msg.content.upper().startswith('!NO')))

        try:
            reply = await client.wait_for('message', check=pred, timeout=30)
            if reply.content.upper().startswith('!YES'):
                await message.channel.send(useful.startReminder(reminder))
            elif reply.content.upper().startswith('!NO'):
                await message.channel.send("Ok, I will discard that reminder.")
                
        except asyncio.TimeoutError:
            await message.channel.send("%s, you took too long to respond so I discarded your reminder."
                                          % message.author.mention)
            
    else:
        await message.channel.send("Sorry, only administrators can use that command!")

#==== Convert number to binary ====
async def binary(message):
    await message.channel.send(useful.toBin(message))

#==== Convert number to hexadecimal ====
async def hexadec(message):
    await message.channel.send(useful.toHex(message))

#==== Search for Magic cards ====
async def magic(message):
    for c in useful.fetchCard(message):
        if c[0] == None:
            await message.channel.send(c[1])
        else:
            await message.channel.send(c[0], embed=discord.Embed(title=c[1], description=c[2]).set_image(url=c[3]))

#==== Setup reminder ====
async def remind(message,client):
    reminder = useful.makeReminder(message)

    await message.channel.send(useful.confirmReminder(message, reminder))

    def pred(msg):
        return (msg.author == message.author and
                msg.channel == message.channel and
                (msg.content.upper().startswith('!YES') or msg.content.upper().startswith('!NO')))

    if reminder != None:
        try:
            reply = await client.wait_for('message', check=pred, timeout=30)
            if reply.content.upper().startswith('!YES'):
                await message.channel.send(useful.startReminder(reminder))
            elif reply.content.upper().startswith('!NO'):
                await message.channel.send("Ok, I will discard that reminder.")
                
        except asyncio.TimeoutError:      
            await message.channel.send("%s, you took too long to respond so I discarded your reminder."
                                      % message.author.mention)

#==== Roll a die ====
async def roll(message):
    await message.channel.send(useful.rollDice(message))

#==== Search for a Wikipedia article ====
async def wiki(message):
    a = useful.fetchWiki(message)
    if a[0] == None:
        await message.channel.send(a[1])
    else:
        await message.channel.send(a[0], embed=discord.Embed(title=a[1], description=a[2]).set_image(url=a[3]))