from discord import Intents
from discord.ext import commands

import secret
from dice_rolls import dice_rolls
from encounter_map_commands import encounter_map
from informational_commands import informational_commands
from music_commands import music
from server_managment_commands import management

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    bot.add_cog(music.Music(bot))


@bot.command(help="Returns user's ping in ms")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 100)}ms")


bot.add_cog(dice_rolls.DiceRolls())
bot.add_cog(management.Management())
bot.add_cog(encounter_map.MapCommands())
bot.add_cog(informational_commands.InformationalCommands())

bot.run(secret.TOKEN)
