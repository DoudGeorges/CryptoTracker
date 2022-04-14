import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import datetime
import csv
import ast

name_exceptions = { # Currency names with exceptions
    "near-protocol" : "near",
    "ceth" : "compound-ether",
    "cusdc" : "compound-usd-coin",
    "kucoin-token" : "kucoin-shares",
    "trueusd" : "true-usd",
    "humans.ai" : "humans-ai",
    "celsius-network" : "celsius-network-token",
}

# Open 'crypto_data.csv'
with open("Data\crypto_data.csv", "r") as csv_file:
    reader = csv.reader(csv_file, delimiter = ';')
    crypto_data = dict(reader)

# Crypto_Info Function
def crypto_info(currency_name):
    if currency_name == "USD":
        value = 1
        image_url = "https://cdn-icons-png.flaticon.com/64/2150/2150150.png"

    else:
        url_name = currency_name.replace(" ", "-").lower()

        if url_name in name_exceptions:
            url_name = name_exceptions[url_name]

        data = requests.get(f"https://www.coingecko.com/en/coins/{url_name}") # All cryptocurrency prices are from coingecko.com - HUGE thanks to them! <3
        soup = BeautifulSoup(data.content, "html.parser")

        value = soup.find("span", class_ = "tw-text-gray-900 dark:tw-text-white tw-text-3xl").text
        image_url = soup.find("img", class_ = "tw-rounded-full")["src"]

        for char in "$,":
            value = value.replace(char, "")

    return float(value), image_url

## Commands Class ##
class Commands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ## Price Command ##

    @commands.command(name = "price")
    @commands.cooldown(1, 1, commands.BucketType.user) # 1 second cooldown
    async def price(self, ctx: commands.context, code: str):
        await ctx.trigger_typing()

        code = code.upper()

        if code in crypto_data:
            print(f"{ctx.message.author} Issued a Command: -price {code}") # Issued a Command Message

            # Currency variables
            data_list = ast.literal_eval(crypto_data[code]) # Get value as list

            crypto_name = data_list[0]
            crypto_color = int(data_list[1], 16)

            value, image_url = crypto_info(crypto_name)

            # Format values as prices
            decimals = len(str(value).split(".")[-1])
            decimals = 8 if decimals > 8 else 2 if decimals < 2 else decimals

            price = "${:,.{}f}".format(value, decimals) + f" USD"
            
            new_embed = discord.Embed(title = f"{crypto_name} Price", description = f"1.0 {code} ≈ {price}", timestamp = datetime.datetime.utcnow(), color = crypto_color)
            new_embed.set_thumbnail(url = image_url)
            await ctx.reply(embed = new_embed, mention_author = False)

        else:
            errorEmbed = discord.Embed(title = "Invalid Cryptocurrency", description = "That cryptocurrency isn't supported by this bot or it doesn't exist.", color = 0xff0000)
            await ctx.reply(embed = errorEmbed, mention_author = False, delete_after = 10)
            await ctx.message.delete(delay = 10)

    ## Convert Command ##

    @commands.command(name = "convert", aliases = ["conv"])
    @commands.cooldown(1, 3, commands.BucketType.user) # 3 second cooldown
    async def convert(self, ctx: commands.context, amount: float, code_1: str, keyword: str = "to", code_2: str = "USD"):
        await ctx.trigger_typing()

        code_1 = code_1.upper()
        code_2 = code_2.upper()

        if code_1 in crypto_data and code_2 in crypto_data:
            if keyword.lower() == "to":
                print(f"{ctx.message.author} Issued a Command: -convert {amount} {code_1} to {code_2}") # Issued a Command Message

                # Variables for first currency
                data_list_1 = ast.literal_eval(crypto_data[code_1])

                crypto_name_1 = data_list_1[0]
                cryoto_color_1 = int(data_list_1[1], 16)
                value_1, image_url_1 = crypto_info(crypto_name_1)

                # Variables for second currency
                data_list_2 = ast.literal_eval(crypto_data[code_2])

                crypto_name_2 = data_list_2[0]
                value_2, image_url_2 = crypto_info(crypto_name_2)

                value_2 = amount * value_1 / value_2

                # Format values as prices
                decimals_1 = len(str(value_1).split(".")[-1])
                decimals_1 = 8 if decimals_1 > 8 else 2 if decimals_1 < 2 else decimals_1

                decimals_2 = len(str(value_2).split(".")[-1])
                decimals_2 = 8 if decimals_2 > 8 else 2 if decimals_2 < 2 else decimals_2
            
                price_1 = "{:,.{}f}".format(amount, decimals_1).rstrip("0").rstrip(".") + f" {code_1}"
                price_2 = "{:,.{}f}".format(value_2, decimals_2).rstrip("0").rstrip(".") + f" {code_2}"

                if code_1 == "USD":
                    price_1 = f"${price_1}"
                
                if code_2 == "USD":
                    price_2 = f"${price_2}"

                new_embed = discord.Embed(title = f"{code_1} ⟶ {code_2}", description = f"{price_1} ≈ {price_2}", timestamp = datetime.datetime.utcnow(), color = cryoto_color_1)
                new_embed.set_thumbnail(url = image_url_1)
                await ctx.reply(embed = new_embed, mention_author = False)

            else:
                errorEmbed = discord.Embed(title = "Invalid Usage", description = "Incorrect usage of that command (don't forget the keyword 'to').", color = 0xff0000)
                await ctx.reply(embed = errorEmbed, mention_author = False, delete_after = 10)
                await ctx.message.delete(delay = 10)

        else:
            errorEmbed = discord.Embed(title = "Invalid Currency", description = "That currency isn't supported by this bot or it doesn't exist.", color = 0xff0000)
            await ctx.reply(embed = errorEmbed, mention_author = False, delete_after = 10)
            await ctx.message.delete(delay = 10)

# Add Cog
def setup(bot: commands.Bot):
    bot.add_cog(Commands(bot))