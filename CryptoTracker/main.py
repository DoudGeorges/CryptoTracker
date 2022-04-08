import discord
from discord.ext import commands
import os
from datetime import datetime
from pytz import timezone

from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix = "-", case_insensitive = True)

bot.remove_command("help")

# On_Ready Event
@bot.event
async def on_ready():
    print(f"Bot Online: {len(bot.guilds)} Guilds")

# On_Guild_Join Event
@bot.event
async def on_guild_join(guild):
    now = datetime.now(timezone("America/Toronto"))
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}] Joined Guild: {guild.name} ({len(bot.guilds)} Total)")

# On_Guild_Remove Event
@bot.event
async def on_guild_remove(guild):
    now = datetime.now(timezone("America/Toronto"))
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}] Left Guild: {guild.name} ({len(bot.guilds)} Total)")

# Help Command
@bot.command()
async def help(ctx: commands.context):
    await ctx.trigger_typing()

    help_embed = discord.Embed(title = "Need Help?", description = "• Use `-btc` for help with BTC commands.\n• Use `-eth` for help with ETH commands.\n• Use `-about` for info about this bot.", color = 0x232529)
    await ctx.reply(embed = help_embed, mention_author = False)

# About Command
@bot.command()
async def about(ctx: commands.context):
    await ctx.trigger_typing()

    help_embed = discord.Embed(title = "About", description = "The simplest and quickest way to track current prices of Bitcoin and Ethereum! CryptoTracker adds a wide range of features to your server. For example:\n \n• Get current cryptocurrency prices,\n• Convert between currencies,\n• Receive info on a wallet address,\n... and more!\n \nType -help to get started!\nOfficial Server: https://discord.gg/vucnFUwvP3", color = 0x232529)
    help_embed.add_field(name = "Support Me?", value = "Donate BTC: `bc1qzwkl5q0h9dhh4y0xgk8z233re8dfxytl3elt9t`\nDonate ETH: `0xCe72aC7C2Ce17F8a735726e637C6863C46C6B308`")
    await ctx.reply(embed = help_embed, mention_author = False)

# Load Cogs
bot.load_extension("Cogs.error_handler")
bot.load_extension("Cogs.bitcoin")
bot.load_extension("Cogs.ethereum")

# Run Bot
bot.run(os.getenv("TOKEN"))