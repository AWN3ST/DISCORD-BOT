import io
import discord
import time
from datetime import *
import asyncio
import sys
import random
import os
from bs4 import BeautifulSoup
import requests
from discord.ext import commands
from datetime import datetime
import pyowm
import tweepy
import time
import json



token = ('')
client = commands.Bot('!')
jahcoins = {}
jahcoin_emoji = '<:jahcoin2:600180930761588747>'


@client.event
#This tells you that the bot is loaded and working
async def on_ready():
    print("Bot is loaded.")
    global jahcoins
    try:
        with open('jahcoins.json') as f:
            jahcoins = json.load(f)
    except FileNotFoundError:
        print("Could not load jahcoins.json")
        jahcoins = {}

@client.command()
async def bal(ctx):
    channel = ctx.message.channel
    id = ctx.message.author.id
    if id in jahcoins:
        await channel.send(f"You have {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}")
    else:
        await channel.send(f"You do not have an account, please make one by typing !register {ctx.message.author.mention}")


@client.command()
async def gamble(ctx, gamble_amount: int):
    channel = ctx.message.channel
    id = ctx.message.author.id
    if id in jahcoins:
        random_number = random.randint(0,100)
        correct_number = random.randint(0,100)
        gamble_amount = int(ctx.message.content[8:])
        if gamble_amount > jahcoins[id]:
            await channel.send(f"You don't have enough! You have {(jahcoins[id])}{jahcoin_emoji} when you tried betting {gamble_amount}{jahcoin_emoji} {ctx.message.author.mention}")
        elif gamble_amount <= jahcoins[id]:
            if random_number < correct_number:
                jahcoins[id] += gamble_amount
                _save()
                await channel.send(f'You won! Congratulations, you now have {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number > correct_number:
                jahcoins[id] -= gamble_amount
                _save()
                await channel.send(f'Unfortunately you lost, you now have {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')

@client.command()
@commands.cooldown(1, 60*60*24, commands.BucketType.user)
async def dailyspin(ctx):
    channel = ctx.message.channel
    id = ctx.message.author.id
    if id in jahcoins:
            random_number = random.uniform(0.0, 100.0)
            await channel.send('You spin the wheel really fast. . .')
            time.sleep(0.75)
            await channel.send('The wheel continues to spin fast. . .')
            time.sleep(0.75)
            await channel.send('The wheel begins to slow down. . .')
            time.sleep(0.75)
            await channel.send('The wheel is just about to stop. . .')
            time.sleep(0.75)
            if random_number <= 5.0:
                won_amount = int(5000)
                jahcoins[id] += won_amount
                _save()
                await channel.send(f'The wheel finally stops and with a 5% chance,\nyou won {won_amount}{jahcoin_emoji} for your daily spin, consider yourself lucky!\n\nYour new balance is - {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number <= 10.0:
                won_amount = int(2500)
                jahcoins[id] += won_amount
                _save()
                await channel.send(f'The wheel finally stops and with a 10% chance,\nyou won {won_amount}{jahcoin_emoji} for your daily spin, consider yourself kinda lucky!\n\nYour new balance is: {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number <= 20.0:
                won_amount = int(1250)
                jahcoins[id] += won_amount
                _save()
                await channel.send(f'The wheel finally stops and with a 20% chance,\nyou won {won_amount}{jahcoin_emoji} for your daily spin, you were semi-lucky!\n\nYour new balance is: {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number <= 30.0:
                won_amount = int(800)
                jahcoins[id] += won_amount
                _save()
                await channel.send(f'The wheel finally stops and with a 30% chance,\nyou won {won_amount}{jahcoin_emoji} for your daily spin, decent spin, good job!\n\nYour new balance is: {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number <= 50.0:
                won_amount = int(500)
                jahcoins[id] += won_amount
                _save()
                await channel.send(f'The wheel finally stops and with a 50% chance,\nyou won {won_amount}{jahcoin_emoji} for your daily spin, OK spin, see you tomorrow!\n\nYour new balance is: {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number <= 75.0:
                won_amount = int(250)
                jahcoins[id] += won_amount
                _save()
                await channel.send(f'The wheel finally stops and with a 75% chance,\nyou won {won_amount}{jahcoin_emoji} for your daily spin, bad spin, better luck tomorrow!\n\nYour new balance is: {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')
            elif random_number <= 100.0:
                won_amount = int(100)
                jahcoins[id] += won_amount
                _save()
                await channel.send(f'The wheel finally stops and with a 100% chance,\nyou won {won_amount}{jahcoin_emoji} for your daily spin, TERRIBLE SPIN, better luck tomorrow!\n\nYour new balance is: {(jahcoins[id])}{jahcoin_emoji} {ctx.message.author.mention}')

    if id not in jahcoins:
            await channel.send(f"You don't have an account! Please type !register to make an account {ctx.message.author.mention}")

'''@dailyspin.error
async def dailyspin_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Error")'''


@client.command()
async def register(ctx):
    id = ctx.message.author.id
    channel = ctx.message.channel
    if id not in jahcoins:
        jahcoins[id] = 100
        await channel.send(f"You are now registered and have been given 100{jahcoin_emoji} {ctx.message.author.mention}")
        _save()
    else:
        await channel.send(f"You already have an account {ctx.message.author.mention}")

@client.command()
async def give(ctx, other: discord.Member, jahcoin: int, error):
    channel = ctx.message.channel
    primary_id = ctx.message.author.id
    other_id = other.id
    if primary_id not in jahcoins:
        await channel.send(f"You do not have an account, create one by typing !register {ctx.message.author.mention}")
    elif other_id not in jahcoins:
        await channel.send(f"The other party {other.mention} does not have an account, he/or she needs to type !register {ctx.message.author.mention}")
    elif jahcoins[primary_id] < jahcoin:
        await channel.send(f"You cannot afford to give {other.mention} {jahcoin}{jahcoin_emoji} because you only have {jahcoins[primary_id]}{jahcoin_emoji} {ctx.message.author.mention}")
    else:
        jahcoins[primary_id] -= jahcoin
        jahcoins[other_id] += jahcoin
        await channel.send(f"Transaction complete.\n\n{other.mention} new balance is: {jahcoins[other_id]}{jahcoin_emoji}\n\n{ctx.message.author.mention} new balance is: " +
                                  f"{jahcoins[primary_id]}{jahcoin_emoji}")
    _save()

def _save():
    with open('jahcoins.json', 'w+') as f:
        json.dump(jahcoins, f)

@client.command()
async def jahcoin(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(title = "How to use Jahcoin Currency", color = 0xdaa520)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/593203992541003807/600183870520033281/exclamation.png")
    embed.add_field(name = "=== Registering ===", value = "First thing first is to register an account by typing **!register**.\nThis will register you into the database and start you out with 100 Jahcoin(s).", inline = True)
    embed.add_field(name = "=== Gambling ===", value = " You can gamble your jahcoin by typing **!gamble (amount to gamble)**. If you win, the amount you gambled will be added to your balance, if you lose the amount\nyou gambled will be taken away.", inline = True)
    embed.add_field(name = "=== Daily Spin ===", value = "You can have a daily spin by typing **!dailyspin**.", inline = True)
    embed.add_field(name = "=== Checking your Balance ===", value = "To check your balance simply type **!bal**.", inline = True)
    embed.add_field(name = "=== Giving ===", value = "Feeling generous? Give some of your {jahcoin_emoji} to another user by\ntyping **!give (amount) @USER**.", inline = True)
    
    await channel.send(content=None, embed=embed)


@client.command()
async def save():
    _save()


'''async def background_loop():
    await client.wait_until_ready()
    while not client.is_closed:
        channel = client.get_channel("")
        
        twitter_status = 'https://twitter.com/i/web/status/'
        username = "wojespn"

        CONSUMER_KEY = 'AkmgJEBZsoUFIsdbysIFrbRxD'
        CONSUMER_SECRET = 'oy4MHCiFlvNxUM9dl2UheTpK5VbvhTk6a18ASJyQkXfQmMNyrt'
        ACCESS_KEY = '1130148049970454533-Rvo4c1IUKqczb6rpn1jBxr9IMOZYfb'
        ACCESS_SECRET = 'nbNb2bqkCgojClRSJiFh0Kn57dVT6Z7wQfHQ1ubvivIBg'

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        while True:
            for status in api.user_timeline(username, count = 1):
                current_status = status.id
                latest_tweet = (twitter_status + str(current_status))
                print(latest_tweet)
                time.sleep(3)
                    
           
            await client.send_message(channel, latest_tweet)
            await asyncio.sleep(3)

client.loop.create_task(background_loop())'''


@client.command()
async def cmds(ctx):
        embed = discord.Embed(title = "AwnBot Commands", color = 0x008000)
        embed.add_field(name = "!gm", value = "Says good morning & tells word of the day + Bible verse of the day + today's date\n" + "-"*95, inline = False)
        embed.add_field(name = "!8ball", value = "Let's you play 8-ball\n" + "-"*95, inline = False)
        embed.add_field(name = "!coinflip", value = "Flips a coin for heads or tails\n" + "-"*95, inline = False)
        embed.add_field(name = "!say", value = "Repeats whatever your \nmessage is in Text-to-speech\n" + "-"*95, inline = False)
        embed.add_field(name = "!weather", value = "Shows current temperature of a city by the following format: !weather (CITY NAME, COUNTRY CODE) with no parantheses.\n" + "-"*95, inline = False)
        embed.add_field(name = "!chance", value = "Gives you a random percentage between 0-100% of something happening.\n Example: !chance The Pats win the super bowl this year?\n" + "-"*95, inline = False)
        embed.add_field(name = "!kawhi", value = "WHAT IT DO BABY, check for yourself what it does ;)" + "-"*95 , inline = False)
        embed.add_field(name = "!randomvid", value = "Sends a random video, usually a funny meme", inline = False)
        embed.add_field(name = "!jahcoin", value = "Tells you the list of commands for our discord currency, Jahcoin.", inline = False)
           
        await ctx.send(content=None, embed=embed)

        

@client.event
async def on_message(message):
        responses = ['It is certain.','It is decidedly so.','Without a doubt','Yes - definitely',
                        'You may rely on it.','As I see it, yes.','Most likely.','Outlook good.','Yes.',
                        'Signs point to yes.','Reply hazy, try again','Ask again later','Better not tell you now',
                        'Cannot predict now.','Concentrate and ask again','Do not count on it','My reply is no.',
                        'My sources say no.','Outlook not so good.','Very doubtful.']
        channel = message.channel
        if message.content.upper().startswith('!8BALL'):
            await channel.send(random.choice(responses) + f" {message.author.mention}")

        await client.process_commands(message)

        


@client.command()
async def coinflip(ctx):
        channel = ctx.message.channel
        await channel.send('Coin is tossed in the air . . .')
        time.sleep(1.5)
        await channel.send('Coin flips numerous times before landing . . .')
        time.sleep(1.5)
        await channel.send('The coin finally lands. . . and it is ' + random.choice(['Heads','Tails']) + f" {ctx.message.author.mention}")


@client.command()
async def say(ctx):
        channel = ctx.message.channel
        args = ctx.message.content.split(" ")
        await channel.send("%s" % (" ".join(args[1:])), tts=True)


@client.command()
async def gmall(ctx):
        channel = ctx.message.channel
        if ctx.message.author.id == '143583362508914688':
            await channel.send("Good morning Bobby Shmelter nation! <@121441376561790976>\n" + "Good morning Carbon nation! <@338154331897593866>\n"
                                        + "Good morning seb nation! <@121333924529045504>\n" + "Good morning Tazz Nation! <@121045727299239937>\n" + "Good morning ramsey nation! <@148931357941301248>")


@client.command()
async def gm(ctx):
        channel = ctx.message.channel
        date = datetime.today().strftime('%Y-%m-%d')
        bibledate = datetime.today().strftime('%Y/%m/%d')

        await channel.send(f"Good morning! {ctx.message.author.mention}\n" + "\nToday's date is " + date + " \n\n**Below is the word of the day**\n" + "https://www.merriam-webster.com/word-of-the-day\n")
        await channel.send("\n**Bible verse of the day is below**" + "\nhttps://www.dailyverses.net/" + bibledate)


@client.command()
async def weather(ctx):
        channel = ctx.message.channel
        degree_sign = u'\N{DEGREE SIGN}'
        owm = pyowm.OWM('')
        location = ctx.message.content[9:]
        zipcode = ctx.message.content[9:]
        observation = owm.weather_at_place(location or zipcode)
        weather = observation.get_weather()
        temperature = weather.get_temperature('fahrenheit')['temp']
        wind = weather.get_wind('miles_hour')['speed']
        windspeed = (round(wind, 2))
        humidity = weather.get_humidity()
        status = weather.get_detailed_status()

        embed = discord.Embed(title = f'Weather for {location}', color = 0x00ffff)
        embed.add_field(name = "-"*99, value = f':thermometer: The temperature in {location} is {temperature}{degree_sign}F', inline = False)
        embed.add_field(name = "-"*99, value = f':dash: {location} has a wind speed of {windspeed} mph.', inline = False)
        embed.add_field(name = "-"*99, value = f':sweat_drops: {location} humidity is {humidity}% with {status}', inline = False)

        await channel.send(content=None, embed=embed)



@client.command()
async def chance(ctx):
        channel = ctx.message.channel
        percentage = (random.uniform(0.00, 100.00))
        percent = (round(percentage, 2))
        
        await channel.send(f'There is a {percent}% chance of it happening. {ctx.message.author.mention}')
        
@client.command()
async def kawhi(ctx):
    channel = ctx.message.channel
    await channel.send("WHAT IT DO BABY", file = discord.File(r"C:\Users\Matt\Desktop\AwnBot Discord\kawhi.mp4"))


@client.command()
async def randomvid(ctx):
    path ='C:/Users/Matt/Desktop/AwnBot Discord/meme vids'
    files = os.listdir(path)
    index = random.randrange(0, len(files))
    vidName = (files[index])

    await ctx.send(file = discord.File(r'C:/Users/Matt/Desktop/AwnBot Discord/meme vids/' + vidName))
                                               
client.run(token)
                            


            
       

