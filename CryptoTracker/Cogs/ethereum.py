import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import datetime

# Ethereum Price
def ethereum_price():
    data = requests.get("https://www.coingecko.com/en/coins/ethereum")
    soup = BeautifulSoup(data.content, "html.parser")

    us_value = soup.find("span", class_ = "tw-text-gray-900 dark:tw-text-white tw-text-3xl").text
    
    for char in "$,":
        us_value = us_value.replace(char, "")

    return float(us_value)

def address_info(eth_address):
    data = requests.get(f"https://www.blockchain.com/eth/address/{eth_address}")
    soup = BeautifulSoup(data.content, "html.parser")
    info = soup.findAll("span", class_ = "sc-1ryi78w-0 cILyoi sc-16b9dsl-1 ZwupP u3ufsr-0 eQTRKC")

    transactions = info[3].text
    balance = info[4].text

    return transactions, balance

# Ethereum Class
class Ethereum(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Base ETH Command
    @commands.group(name = "eth", invoke_without_command = True, case_insensitive = True)
    async def eth(self, ctx: commands.context, *args):
        await ctx.trigger_typing()

        if len(args) > 0:
            new_embed = discord.Embed(title = "Unknown Command", description = "Unknown command: Use `-eth` for help with ETH commands.", color = 0xff0000)
            await ctx.reply(embed = new_embed, mention_author = False, delete_after = 10)
            await ctx.message.delete(delay = 10)
        else:
            help_embed = discord.Embed(title = "Ethereum Commands", color = 0x627EEA)
            help_embed.add_field(name = "ETH ⟶ USD", value = "Convert any amount from ETH to USD.\n• Usage: `-eth toUSD <amount>`\n• Aliases: `to-usd`", inline = False)
            help_embed.add_field(name = "USD ⟶ ETH", value = "Convert any amount from USD to ETH.\n• Usage: `-eth toETH <amount>`\n• Aliases: `to-eth`", inline = False)
            help_embed.add_field(name = "Address Lookup", value = "Receive info on a wallet address.\n• Usage: `-eth addr <address>`\n• Aliases: `address`", inline = False)
            await ctx.reply(embed = help_embed, mention_author = False)
    
    # ToUSD Command
    @eth.command(name = "tousd", aliases = ["to-usd"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def eth_tousd(self, ctx: commands.context, amount: float = 1.0):
        await ctx.trigger_typing()

        eth_value = round(amount, 8)
        us_value = round(ethereum_price() * eth_value, 2)

        eth_price = "{:,}".format(eth_value) + " ETH" # Format Price
        us_price = "$" + "{:,.2f}".format(us_value) + " USD" # Format Price

        new_embed = discord.Embed(title = "ETH ⟶ USD", description = f"{eth_price} ≈ {us_price}", timestamp = datetime.datetime.utcnow(), color = 0x627EEA)
        await ctx.reply(embed = new_embed, mention_author = False)

    # ToETH Command
    @eth.command(name = "toeth", aliases = ["to-eth"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def eth_toeth(self, ctx: commands.context, amount: float = 1.0):
        await ctx.trigger_typing()

        us_value = round(amount, 2)
        eth_value = round(us_value / ethereum_price(), 8)

        us_price = "$" + "{:,.2f}".format(us_value) + " USD" # Format Price
        eth_price = "{:,}".format(eth_value) + " ETH" # Format Price

        new_embed = discord.Embed(title = "USD ⟶ ETH", description = f"{us_price} ≈ {eth_price}", timestamp = datetime.datetime.utcnow(), color = 0x627EEA)
        await ctx.reply(embed = new_embed, mention_author = False)

    # Address Lookup Command
    @eth.command(name = "addr", aliases = ["address"])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def eth_addr(self, ctx: commands.context, eth_address):
        await ctx.trigger_typing()

        try:
            transactions, balance = address_info(eth_address)

            new_embed = discord.Embed(title = "Address Lookup", timestamp = datetime.datetime.utcnow(), color = 0x627EEA)
            new_embed.add_field(name = "Total Transactions:", value = transactions, inline = False)
            new_embed.add_field(name = "Current Balance:", value = balance, inline = False)
            await ctx.reply(embed = new_embed, mention_author = False)

        except:
            errorEmbed = discord.Embed(title = "Invalid Address", description = "Address could not be found.", color = 0xff0000)
            await ctx.reply(embed = errorEmbed, mention_author = False, delete_after = 10)
            await ctx.message.delete(delay = 10)

# Add Cog
def setup(bot: commands.Bot):
    bot.add_cog(Ethereum(bot))