#==== Description ====
"""
Sends messages to Discord from useful commands
"""

#==== Imports ====
import asyncio
import discord

from funktions import useful
from helpers import helper_functions as helpers
from errors import errors

#==== Setup a reminder for everyone ====
async def announce(message,client):
    if message.author.guild_permissions.administrator:
        try:
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
        except errors.Error as e:
            await message.channel.send(helpers.badArgs(e))
            
    else:
        await message.channel.send("Sorry, only administrators can use that command!")

#==== Convert number to binary ====
async def binary(message):
    try:
        await message.channel.send(useful.toBin(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Convert number to hexadecimal ====
async def hexadec(message):
    try:
        await message.channel.send(useful.toHex(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Search for Magic cards ====
async def magic(message,apiHeaders):
    try:
        for c in useful.fetchCard(message,apiHeaders):
            if c.empty():
                await message.channel.send(c.text)
            else:
                await message.channel.send("", embed=discord.Embed(title=c.title,description=c.text,url=c.url)
                                           .set_image(url=c.image))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))
            
#==== Setup a poll ====
async def poll(message,client):
    activeId = str(message.author.id) + str(message.channel.id)

    if helpers.isPollRunning(activeId): #Only begin a poll if not already one in channel
        await message.channel.send("Sorry, you already have a poll running in this channel. If you want to end it, send `!end`.")

    else:                          
        try:
            poll = useful.makePoll(message)
            reactions = []
            helpers.addToActivePolls(activeId)
            sentMsg = await message.channel.send(poll.body)

            def pred(msg):
                return (msg.author == message.author and
                        msg.channel == message.channel and
                        msg.content.upper().startswith('!END'))

            for o in poll.options:
                await sentMsg.add_reaction(o)

            try:
                reply = await client.wait_for('message', check=pred, timeout = 10800)
            except asyncio.TimeoutError:
                pass

            fetchedMsg = await message.channel.fetch_message(sentMsg.id) #Update message information
            await message.channel.send(useful.finishPoll(fetchedMsg,poll))
            helpers.removeFromActivePolls(activeId)
            
        except errors.Error as e:
            await message.channel.send(helpers.badArgs(e))

#==== Setup reminder ====
async def remind(message,client):
    try:
        reminder = useful.makeReminder(message)

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

    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Roll a die ====
async def roll(message):
    try:
        await message.channel.send(useful.rollDice(message))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))

#==== Search for a Wikipedia article ====
async def wiki(message,apiHeaders):
    try:
        a = useful.fetchWiki(message,apiHeaders)
        if a.empty():
            await message.channel.send(a.text)
        else:
            await message.channel.send("", embed=discord.Embed(title=a.title,description=a.text,url=a.url)
                                       .set_image(url=a.image))
    except errors.Error as e:
        await message.channel.send(helpers.badArgs(e))
