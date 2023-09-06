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
from discord import app_commands
from discord.ext import commands
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


async def check_success(interaction, guess, adjustment, result, leverage):
    """
    This function compares the discord user's guess and their adjustment range to the
    radomly generated number that corresponds to the specified star/difficulty level.
    Outputs to the discord channel with results.

    :param interaction: The discord bot interaction received by the command
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
        await interaction.response.send_message(
            f'Your crafting check was a critical success! Your guess was {guess}, which matched the generated Trial value of {result} exactly!'
        )
    elif len(check_set) != 0:
        await interaction.response.send_message(
            f'Your crafting check succeeded. Your guess was {guess}. It covered an effective range of: {min(guess_range)}-{max(guess_range)}.\n\nThe random number was {result}. The range your effective number needed to fall inside of was: {min(success_range)} - {max(success_range)}'
        )
    else:
        await interaction.response.send_message(
            f'Your crafting check failed. Your guess was {guess}. It covered an effective range of: {min(guess_range)}-{max(guess_range)}.\n\nThe random number was {result}. The range your effective number needed to fall inside of was: {min(success_range)} - {max(success_range)}'
        )
    return 0


# if __name__ == '__main__':
dotenv.load_dotenv(dotenv_path=".env")
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents(messages=True, message_content=True)
bot = commands.Bot(
    command_prefix='/',
    description='RS-CER LARP Bot for Crafting Checks',
    intents=intents,
    help_command=None
)

cryptorand = SystemRandom()


@bot.tree.command(name="craft", description="Ask LARPBot to perform a Crafting Trial for you")
@app_commands.describe(
    trial="The Trial rating you are crafting against",
    stars="The Star rating you are crafting against",
    adjustment="Your adjustment value for the stat you're crafting with",
    guess="Your guess between 0 and 20"
)
async def craft(interaction: discord.Interaction, trial: int, stars: int, adjustment: int, guess: int):
    print(f'Received Command to perform a Trial...')
    try:
        # Trial difficulty calculation.
        # Trivial (0) checks are the only ones that don't adhere to the equation used below
        match trial:
            case 0:
                leverage = 12
            case _:
                leverage = math.floor(8/(2**(int(trial-1))))

        # Star count determines the range to "roll".
        # 0 is the only value that doesn't adhere to the equation used below:
        match stars:
            case 0:
                result = cryptorand.randrange(0, 10+1)
            case _:
                result = cryptorand.randrange(0, (stars*10)+1)

        await check_success(interaction, guess, adjustment, result, leverage)

    except (Exception,):
        await interaction.response.send_message(f'Failed to process your message!\nPlease ensure you only used one space between each argument, there are no typos, and you provided arguments in the format argument:value.')
    finally:
        print("Command for Crafting was Successfully Processed\n")
        return 0


@bot.tree.command(name="random", description="Have LARPBot generate a random number for you")
@app_commands.describe(
    low="The bottom end of the random range",
    high="The upper end of the random range"
)
async def random(interaction: discord.Interaction, low: int, high: int):
    print(f'Received Command to generate a random number between {low} and {high}...')
    try:
        result = cryptorand.randrange(low, high+1)

        await interaction.response.send_message(f'Random Number is: {result}')
    except (Exception,):
        await interaction.response.send_message(f'Encountered an issue with the formatting of your request for a random number!\nPlease ensure there are no typos, you only provided min:number max:number, and that there are no excess spaces')
    finally:
        print("Command for Random was Successfully Processed\n")
        return 0


@bot.tree.command(name="larp-help", description="Ask LARPBot for help")
@app_commands.describe(
    help_term="The function you'd like help with. Currently, you can provide 'random' or 'craft' here."
)
async def larphelp(interaction: discord.Interaction, help_term: str):
    try:
        if help_term == "craft":
            message = f'To craft, use: ```/craft trial:check_difficulty_as_a_number stars:star_count adjustment:adjustment_number guess:your_guess```\n\tExample: ```/craft trial:3 stars:3 adjustment:13 guess:14```\n'
            message += f'Use the following stat as your adjustment number for the corresponding crafting type:\n\tApothecary (Alchemy): Wits\n\tArcane Scribe (Scribing): Magic\n\tArmorer (Armor Smithing): Willpower\n\tEnchanter (Imbuing): Magic\n\tTinkerer (Tinkering): Luck\n\tWeapon Smith (Weapon Smithing): Might\n\nTrial Check should be provided as a number 0-5, mapped from trivial to impossible.\n\tTrivial: 0\n\tEasy: 1\n\tMedium: 2\n\tModerate: 3\n\tHard: 4\n\tImpossible: 5'
            await interaction.response.send_message(message)
        elif help_term == "random":
            await interaction.response.send_message(f'To use the random function, provide your desired rage in the format:```/random min:minimum_number max:max_number```')
        else:
            await interaction.response.send_message(f'Help Command not recognized!\nLARPBot Usage information:\n\tSupported Functions are:\n\t\trandom\n\t\tcraft\n\nTo get help on a specific function, type ```/help function_name```')
    except (Exception,):
        await interaction.response.send_message(f'Experienced an issue processing your help request.\nLARPBot Usage information:\n\tSupported Functions are:\n\t\trandom\n\t\tcraft\n\nTo get help on a specific function, type ```/help function_name```')
    finally:
        print("Command for Help was Successfully Processed\n")
        return 0


@bot.event
async def on_ready():
    await bot.tree.sync()
    guilds = [guild async for guild in bot.fetch_guilds(limit=1)]
    print(f'LARPBot is ready! The following guilds are visible:')
    for guild in guilds:
        print(f'\t{guild.name} as {bot.user}')

    print("\nListening for Messages...\n")


bot.run(TOKEN)
