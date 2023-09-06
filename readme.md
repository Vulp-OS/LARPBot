![CodeQL](https://github.com/Vulp-OS/LARPBot/actions/workflows/github-code-scanning/codeql/badge.svg)

# LARPBot

A discord bot to help with LARP Crafting checks.
It runs continuously, listening for commands on connected Discord Servers

## Usage:
Once the bot has been added to your server and is running, you can use slash commands to interact with it.

The bot listens for the following slash-commands: `/larp-help`, `/random`, `/craft`.
* When you use a slash-command, a short description is provided, and the values needed for the command are listed, each with their own descriptions.
  * The context for these flags is found in the RS-CER LARP 2nd Edition manual

## Setup:

### Obtain the Code
You can download a zip of the code from GitHub, or you can clone the code to make future updates easier.
```
git clone git@github.com/Vulp-OS/LARPBot.git
```
To apply future updates, you can use `git pull`.

### Discord Setup
To use this Discord Bot, you must create an application and bot on the [Discord Devlopers](https://discord.com/developers/applications) page.

* Create an Application and name it `LARPBot`
* Inside the application settings, go to the Bot tab and give it the `LARPBot` username.
* Copy the token from this page. If you can't find it, you can reset the token. (Resetting the token will invalidate the old token)
* Put the token you get in a new file named `.env` in the project directory that contains: `DISCORD_TOKEN=YOUR_COPIED_TOKEN`
* On the Bot page, enable the `Message Content Intent`. **Make sure you save your changes!**
* Go to the `OAuth2` page, then `URL Generator` and select the `bot` scope, then in `Bot Permissions`:
  * Send Messages
  * Create Public Threads
  * Send Messages in Threads
  * Read Message History
* Copy the generated URL from the bottom of this page, and put it in your web browser. This will prompt you to authorize the bot on your server.
* In your server settings, go to the `Integrations` tab, and click manage on `LARPBot`
* Disable the bot's access to All Channels, then click `Add Channels` to select the channels it is authorized on.

### App Config
This was developed and tested on Python >=3.11. It may work on earlier versions, but has not been tested. It is recommended that a virtual environment is used to install the required libraries.
In the app directory on Linux, run:
```
python -mvenv venv
source ./venv/bin/activate
```

If you're on Windows, use PowerShell, then:
```
python -mvenv venv
.\venv\Scripts\activate.ps1
```
Note: You may need to allow script execution using the `Set-ExecutionPolicy` command.

Once you have the virtual environment activated on the appropriate platform, install the required packages:
```
pip install -r requirements.txt
```

Then, run the bot:
```
python main.py
```
