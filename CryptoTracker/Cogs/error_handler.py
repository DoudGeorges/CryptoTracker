import discord
from discord.ext import commands

# ErrorHandler Class
class ErrorHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.CommandNotFound): # CommandNotFound
            return
        
        else:
            await ctx.trigger_typing()

            if isinstance(error, commands.CommandOnCooldown): # CommandOnCooldown
                errorName = "Command Cooldown"
                errorMessage = f"Try again in {round(error.retry_after, 1)} seconds."

            elif isinstance(error, commands.MissingRequiredArgument): # MissingRequiredArgument
                errorName = "Missing Argument"
                errorMessage = f"A required argument is missing."

            elif isinstance(error, commands.BadArgument): # BadArgument
                errorName = "Invalid Argument"
                errorMessage = "At least one argument is invalid."

            elif isinstance(error, commands.UserInputError): # UserInputError
                errorName = "Invalid Usage"
                errorMessage = "Incorrect usage of that command. See `-help`."

            else: # Unexpected
                errorName = "Unknown Error"
                errorMessage = "An error occured while running that command."
                print(error)

            errorEmbed = discord.Embed(title = errorName, description = errorMessage, color = 0xff0000)
            await ctx.reply(embed = errorEmbed, mention_author = False, delete_after = 10)
            await ctx.message.delete(delay = 10)

# Add Cog
def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))