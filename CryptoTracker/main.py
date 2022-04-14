## CryptoTracker v1.1 ##
import discord
from discord.ext import commands
import os
from datetime import datetime
from pytz import timezone

from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "-", intents = intents, case_insensitive = True) # Command Prefix: -

bot.remove_command("help") # Remove built in help command

@bot.event # On_Ready Event
async def on_ready():
    print(f"Bot Online: {len(bot.guilds)} Guilds")
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = f"-help | {len(bot.guilds)} servers"))

    '''
    new_embed = discord.Embed(title = "New Update", description = "A new update has just been released for CryptoTracker!\n \n• Track the current prices of *over 100* different currencies!\n• Convert between any two cryptocurrencies!\n \nSee `-help` for more information.", color = 0xF7931A)
    new_embed.set_thumbnail(url = "https://top.gg/_next/image?url=https%3A%2F%2Fimages.discordapp.net%2Favatars%2F959217021508288573%2Fbe32b88c989d1efcd06d81e54ca03cc1.png%3Fsize%3D128&w=128&q=75")

    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:

                if member.guild_permissions.administrator:
                    try:
                        await member.send(embed = new_embed)
                        print(f"Sent Direct Message: {member.name}")
                    except:
                        print(f"Couldn't Send Direct Message: {member.name}")
    '''

@bot.event # On_Guild_Join Event
async def on_guild_join(guild):
    now = datetime.now(timezone("America/Toronto"))
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}] Joined Guild: {guild.name} ({len(bot.guilds)} Total)")

@bot.event # On_Guild_Remove Event
async def on_guild_remove(guild):
    now = datetime.now(timezone("America/Toronto"))
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}] Left Guild: {guild.name} ({len(bot.guilds)} Total)")

@bot.command() # Help Command
async def help(ctx: commands.context):
    print(f"{ctx.message.author} Issued a Command: -help") # Issued a Command Message
    await ctx.trigger_typing()

    help_embed = discord.Embed(title = "Need Help?", description = "", color = 0x232529)
    help_embed.add_field(name = "Price", value = "Get the current price of any currency in USD.\n• Usage: `-price <currency code>`", inline = False)
    help_embed.add_field(name = "Convert", value = "Convert any amount to its equivalent value in another currency.\n• Usage: `-convert <amount> <currency code #1> to <currency code #2>`\n• Aliases: `conv`", inline = False)
    help_embed.add_field(name = "About", value = "Get information about this bot.\n• Usage: `-about`", inline = False)
    await ctx.reply(embed = help_embed, mention_author = False)

@bot.command() # About Command
async def about(ctx: commands.context):
    print(f"{ctx.message.author} Issued a Command: -about") # Issued a Command Message
    await ctx.trigger_typing()

    help_embed = discord.Embed(title = "About", description = "Track the current prices of *over 100* different cryptocurrencies!\n \n• Get current cryptocurrency prices,\n• Convert between any currency,\n... and more!\n \nOfficial Discord: https://discord.gg/vucnFUwvP3\nBot Page: https://top.gg/bot/959217021508288573\n \n*Source of Prices: https://www.coingecko.com/*", color = 0x232529)
    help_embed.add_field(name = "Support Me", value = "Donate BTC: `bc1qzwkl5q0h9dhh4y0xgk8z233re8dfxytl3elt9t`\nDonate ETH: `0xCe72aC7C2Ce17F8a735726e637C6863C46C6B308`")
    await ctx.reply(embed = help_embed, mention_author = False)

# Load Cogs
bot.load_extension("Cogs.error_handler")
bot.load_extension("Cogs.commands")

# Run Bot
bot.run(os.getenv("TOKEN"))
