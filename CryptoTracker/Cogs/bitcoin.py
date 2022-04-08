import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import datetime

# Bitcoin Price
def bitcoin_price():
    data = requests.get("https://www.coingecko.com/en/coins/bitcoin")
    soup = BeautifulSoup(data.content, "html.parser")

    us_value = soup.find("span", class_ = "tw-text-gray-900 dark:tw-text-white tw-text-3xl").text
    
    for char in "$,":
        us_value = us_value.replace(char, "")

    return float(us_value)

def address_info(btc_address):
    data = requests.get(f"https://www.blockchain.com/btc/address/{btc_address}")
    soup = BeautifulSoup(data.content, "html.parser")
    info = soup.findAll("span", class_ = "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC")

    transactions = info[2].text
    balance = info[5].text

    return transactions, balance

# Bitcoin Class
class Bitcoin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Base BTC Command
    @commands.group(name = "btc", invoke_without_command = True, case_insensitive = True)
    async def btc(self, ctx: commands.context, *args):
        await ctx.trigger_typing()

        if len(args) > 0:
            new_embed = discord.Embed(title = "Unknown Command", description = "Unknown command: Use `-btc` for help with BTC commands.", color = 0xff0000)
            await ctx.reply(embed = new_embed, mention_author = False, delete_after = 10)
            await ctx.message.delete(delay = 10)
        else:
            help_embed = discord.Embed(title = "Bitcoin Commands", color = 0xF7931A)
            help_embed.add_field(name = "BTC ⟶ USD", value = "Convert any amount from BTC to USD.\n• Usage: `-btc toUSD <amount>`\n• Aliases: `to-usd`", inline = False)
            help_embed.add_field(name = "USD ⟶ BTC", value = "Convert any amount from USD to BTC.\n• Usage: `-btc toBTC <amount>`\n• Aliases: `to-btc`", inline = False)
            help_embed.add_field(name = "Address Lookup", value = "Receive info on a wallet address.\n• Usage: `-btc addr <address>`\n• Aliases: `address`", inline = False)
            await ctx.reply(embed = help_embed, mention_author = False)
    
    # ToUSD Command
    @btc.command(name = "tousd", aliases = ["to-usd"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def btc_tousd(self, ctx: commands.context, amount: float = 1.0):
        await ctx.trigger_typing()

        btc_value = round(amount, 8)
        us_value = round(bitcoin_price() * btc_value, 2)

        btc_price = "{:,}".format(btc_value) + " BTC" # Format Price
        us_price = "$" + "{:,.2f}".format(us_value) + " USD" # Format Price

        new_embed = discord.Embed(title = "BTC ⟶ USD", description = f"{btc_price} ≈ {us_price}", timestamp = datetime.datetime.utcnow(), color = 0xF7931A)
        await ctx.reply(embed = new_embed, mention_author = False)

    # ToBTC Command
    @btc.command(name = "tobtc", aliases = ["to-btc"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def btc_tobtc(self, ctx: commands.context, amount: float = 1.0):
        await ctx.trigger_typing()

        us_value = round(amount, 2)
        btc_value = round(us_value / bitcoin_price(), 8)

        us_price = "$" + "{:,.2f}".format(us_value) + " USD" # Format Price
        btc_price = "{:,}".format(btc_value) + " BTC" # Format Price

        new_embed = discord.Embed(title = "USD ⟶ BTC", description = f"{us_price} ≈ {btc_price}", timestamp = datetime.datetime.utcnow(), color = 0xF7931A)
        await ctx.reply(embed = new_embed, mention_author = False)

    # Address Lookup Command
    @btc.command(name = "addr", aliases = ["address"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def btc_addr(self, ctx: commands.context, btc_address):
        await ctx.trigger_typing()

        try:
            transactions, balance = address_info(btc_address)

            new_embed = discord.Embed(title = "Address Lookup", timestamp = datetime.datetime.utcnow(), color = 0xF7931A)
            new_embed.add_field(name = "Transactions:", value = transactions, inline = False)
            new_embed.add_field(name = "Current Balance:", value = balance, inline = False)
            await ctx.reply(embed = new_embed, mention_author = False)

        except:
            errorEmbed = discord.Embed(title = "Invalid Address", description = "Address could not be found.", color = 0xff0000)
            await ctx.reply(embed = errorEmbed, mention_author = False, delete_after = 10)
            await ctx.message.delete(delay = 10)

# Add Cog
def setup(bot: commands.Bot):
    bot.add_cog(Bitcoin(bot))