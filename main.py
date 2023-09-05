"""
LARPBot
=======

A discord bot to help with LARP Crafting checks.
It runs continuously, listening for commands on connected Discord Servers

Author: Ethan Rockwood
"""


import math
import os
from random import SystemRandom  # Use a random generator that is considered "cryptographically secure"

import discord
import dotenv


def get_args(message):
    """
    This function processes a discord message received by the on_message event.
    It uses : as a delimiter between keys and values, and space as a separator between
    pairs of keys and values.

    :param message: The message received from Discord event on_message.
    :return: A dict that contains key:value pairs parsed from the received Discord message.
    """
    return dict((x.strip(), y.strip())
                for x, y in (element.split(':')
                             for element in message.split(' ')))


async def check_success(message, guess, adjustment, result, leverage):
    """
    This function compares the discord user's guess and their adjustment range to the
    radomly generated number that corresponds to the specified star/difficulty level.
    Outputs to the discord channel with results.

    :param message: The discord message received by the on_message event
    :param guess: The discord user's guess at the random number
    :param adjustment: The amount to adjust the discord user's effective guess range by
    :param result: The result of the random roll made by the system for the relevant trial star/difficulty level
    :param leverage: The window that the user's guess must fall inside to be successful
    :return: void
    """
    if leverage == 0:
        success_range = {result}
    else:
        success_range = set(range(result-leverage, result+leverage))

    if adjustment == 0:
        guess_range = {guess}
    else:
        guess_range = range(guess-adjustment, guess+adjustment)

    check_set = success_range.intersection(guess_range)
    if guess == result:
        await message.channel.send(
            f'Your crafting check was a critical success! Your guess was {guess}, which matched the generated Trial value of {result} exactly!'
        )
    elif len(check_set) != 0:
        await message.channel.send(
            f'Your crafting check succeeded. Your guess was {guess}. It covered an effective range of: {min(guess_range)}-{max(guess_range)}.\n\nThe random number was {result}. The range your effective number needed to fall inside of was: {min(success_range)} - {max(success_range)}'
        )
    else:
        await message.channel.send(
            f'Your crafting check failed. Your guess was {guess}. It covered an effective range of: {min(guess_range)}-{max(guess_range)}.\n\nThe random number was {result}. The range your effective number needed to fall inside of was: {min(success_range)} - {max(success_range)}'
        )


async def process_random(message):
    if message.content == "/LARPBot random" or message.content == "/LARPBot random ":
        await message.channel.send(f'To use the random function, provide your desired rage in the format:```/LARPBot random min:minimum_number max:max_number```')
    else:
        try:
            stripped_message = message.content.replace("/LARPBot random ", '')
            args = get_args(stripped_message)

            result = cryptorand.randrange(int(args['min']), int(args['max'])+1)

            await message.channel.send(f'Random Number is: {result}')
        except (Exception,):
            await message.channel.send(f'Encountered an issue with the formatting of your request for a random number:\n```{message.content}\nPlease ensure there are no typos, you only provided min:number max:number, and that there are no excess spaces')


async def process_craft(message):
    stripped_message = message.content.replace("/LARPBot craft", '')
    if stripped_message == "" or stripped_message == " ":
        await message.channel.send(f'To craft, use: ```/LARPBot craft trial:check_difficulty_as_a_number stars:star_count adjustment:adjustment_number guess:your_guess```\n\tExample: ```/LARPBot craft trial:3 stars:3 adjustment:13 guess:14```')
        await message.channel.send(f'Use the following stat as your adjustment number for the corresponding crafting type:\n\tApothecary (Alchemy): Wits\n\tArcane Scribe (Scribing): Magic\n\tArmorer (Armor Smithing): Willpower\n\tEnchanter (Imbuing): Magic\n\tTinkerer (Tinkering): Luck\n\tWeapon Smith (Weapon Smithing): Might\n\nTrial Check should be provided as a number 0-5, mapped from trivial to impossible.\n\tTrivial: 0\n\tEasy: 1\n\tMedium: 2\n\tModerate: 3\n\tHard: 4\n\tImpossible: 5')
    else:
        try:
            stripped_message = stripped_message.lstrip()
            args = get_args(stripped_message)
            guess = int(args['guess'])
            adjustment = int(args['adjustment'])

            # Trial difficulty calculation. Question Mark always = 5
            # Trivial (0) checks are the only ones that don't adhere to the equation used below
            if args['trial'] == "?":
                args['trial'] = '5'

            match args['trial']:
                case '0':
                    leverage = 12
                case _:
                    leverage = math.floor(8/(2**(int(args['trial']-1))))

            # Star count determines the range to "roll". Question Mark always = 5
            # 0 is the only value that doesn't adhere to the equation used below:
            if args['stars'] == "?":
                args['stars'] = '5'

            match args['stars']:
                case '0':
                    result = cryptorand.randrange(0, 10+1)
                case _:
                    result = cryptorand.randrange(0, (int(args['stars'])*10)+1)

            await check_success(message, guess, adjustment, result, leverage)

        except (Exception,):
            await message.channel.send(f'Failed to process your message:\n\t```{message.content}```\nPlease ensure you only used one space between each argument, there are no typos, and you provided arguments in the format argument:value.')
        else:
            print("Crafting Message was Successfully Processed")


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
dotenv.load_dotenv(dotenv_path=".env")
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(messages=True, message_content=True)
client = discord.Client(intents=intents)

cryptorand = SystemRandom()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.content.startswith("/LARPBot"):
        if message.content == "/LARPBot":
            await message.channel.send(f'LARPBot Usage information:\n\tSupported Functions are:\n\t\trandom\n\t\tcraft\n\nTo get help on a specific function, type ```/LARPBot function_name```')
        elif message.content.startswith("/LARPBot random"):
            await process_random(message)
        elif message.content.startswith("/LARPBot craft"):
            await process_craft(message)


client.run(TOKEN)
