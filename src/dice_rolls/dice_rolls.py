import random
import re

from discord import Color
from discord import Embed
from discord.ext import commands


def roll_dice(type_of_dice, times_rolled):
    rolls = []
    for i in range(times_rolled):
        rolls.append(random.randint(1, type_of_dice))
    return rolls


def prettify_list(nums):
    out_str = ''
    for i in range(len(nums)):
        if i % 2 != 0:
            out_str += str(nums[i]) + '\n'
        else:
            out_str += str(nums[i])
    return out_str


class DiceRolls(commands.Cog):

    @commands.command(name='roll', aliases=['r', 'roll_dice'])
    async def roll_dice(self, ctx, *, input_str):
        """
        Rolls dice given a string of the form \u03C8d\u03C9 for some integers \u03C8 and \u03C9.
        Example: .roll 1d20 2d10
        :param ctx: discord.ext.commands.context [Ignore]
        :param input_str: str [Required]
        """
        rolls = []
        embed = Embed(title='Your Rolls', color=Color.random())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

        rolls_split = input_str.split(' ')
        # check input
        for i in rolls_split:
            if re.match('[0-9]+d[0-9]', i) is None:
                await ctx.send('Roll must be of the form \u03C8d\u03C9 for some integers'
                               ' \u03C8 and \u03C9.\nExample: 1d20 3d6')
                return

        for i in rolls_split:
            d_type = int(i.split('d')[1])
            times_rolled = int(i.split('d')[0])
            rolls.append((d_type, roll_dice(d_type, times_rolled)))
        rolls_sums = [sum(i[1]) for i in rolls]

        for i in range(len(rolls)):
            name_string = 'd' + str(rolls[i][0])
            value_string = str(rolls[i][1]) + '\n' + '\u03A3: ' + str(rolls_sums[i])
            embed.add_field(name=name_string, value=value_string, inline=True)

        if len(rolls_split) > 1:
            embed.add_field(name='Total: ', value=str(sum(rolls_sums)), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='d20')
    async def roll_d20(self, ctx):
        """
        Rolls one d20
        """
        embed = Embed(title='Your Rolls', color=Color.random())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name='Roll', value=str(random.randint(1, 20)))

        await ctx.send(embed=embed)

    @commands.command(name='roll_base_stats', aliases=['roll_base'])
    async def roll_starting_stats(self, ctx):
        """
        Randomly rolls for 4 d6 taking 3 highest and returns their sum for all 6 base stats
        """
        # there are 6 base stats in D&D 5e
        number_of_base_stats = 6
        embed = Embed(title="Base Stat Rolls", color=Color.random())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        # roll 4 d6 dice
        d6_rolls = [roll_dice(6, 4) for _ in range(number_of_base_stats)]
        embed.add_field(name="Initial Rolls", value=prettify_list(d6_rolls), inline=False)
        # remove the minimum roll
        for i in d6_rolls:
            i.remove(min(i))
        sums = [sum(i) for i in d6_rolls]
        embed.add_field(name='Least Removed', value=prettify_list(d6_rolls), inline=False)
        embed.add_field(name='Roll Totals', value=str(sums), inline=False)
        await ctx.send(embed=embed)
