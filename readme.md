![CodeQL](https://github.com/Vulp-OS/LARPBot/actions/workflows/github-code-scanning/codeql/badge.svg)

# LARPBot

A discord bot to help with LARP Crafting checks.
It runs continuously, listening for commands on connected Discord Servers

## Usage:
Once the bot has been added to your server and is running, you can use slash commands to interact with it.

The bot listens for messages that start with `/LARPBot`. The currently-supported functions are:
* random
  * Example: `/LARPBot random min:0 max:20`
* craft
  * Example: `/LARPBot craft trial:3 stars:3 adjustment:10 guess:15`
  * The context for these flags is found in the RS-CER LARP 2nd Edition manual

To receive help from the bot about which functions are available, use `/LARPBot` without specifying a command. To receive more specific help for a function, use `/LARPBot function_name` without any further input. 

## Setup:

### Discord Setup
To use this Discord Bot, you must create an application and bot on the Discord Devlopers page.
https://discord.com/developers/applications

* Create an Application and name it `LARPBot`
* Inside the application settings, go to the Bot tab and give it the `LARPBot` username.
* Copy the token from this page. If you can't find it, you can reset the token.
* Put the token you get in a file named `.env` in the project directory with: `DISCORD_TOKEN=YOUR_COPIED_TOKEN`
* On the Bot page, scroll down to Bot Permissions.
  * Enable the `Message Content Intent`
* Go to the `OAuth2` page, then `URL Generator` and select the `bot` scope, then in `Bot Permissions`:
  * Send Messages
  * Create Public Threads
  * Send Messages in Threads
  * Read Message History
* Copy the generated URL from the bottom of this page, and put it in your web browser. This will prompt you to authorize the bot on your server.
* In your server settings, go to the `Integrations` tab, and click manage on `LARPBot`
* Disable the bot's access to All Channels, then click `Add Channels` to select the channels it is authorized on.

### App Config
You need Python >=3.11, and we need a virtual environment to install the required libraries to.
In the app directory on Linux, run:
```
python3.11 -mvenv venv
source ./venv/bin/activate
```

If you're on Windows, use PowerShell, then:
```
python3.11 -mvenv venv
.\venv\Scripts\activate.ps1
```

Once you have the virtual environment activated on the appropriate platform, install the required packages:
```
pip install -r requirements.txt
```

Then, run the bot:
```
python main.py
```
