import random

from discord import Color
from discord import Embed
from discord.ext import commands

from src.informational_commands.coin_additional_functions import *
from src.informational_commands.feat_additional_functions import *
from src.informational_commands.image_search_additional_functions import *
from src.informational_commands.spell_additional_functions import *


class InformationalCommands(commands.Cog):
    spells_dict = None
    feat_dict = None

    @commands.command(name='names')
    async def generate_random_race_names_(self, ctx, *, race_type):
        """
        Takes a <race_type> and gives a list of randomly generated names for that <race_type>
        Example: .names orc
        :param ctx: discord.ext.commands.context [Ignore]
        :param race_type: str [Required]
        """
        # todo validate race_type
        names = retrieve_names_from_page(race_type.lower())
        list_first_half, list_second_half = format_name_list(names)
        embed = Embed(title="Names: ", url=FANTASY_NAME_SOURCE_SITE_URL, description=f'list of {race_type} names',
                      color=Color.random())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        thumbnail_url = random.choice(retrieve_image_urls_of_search_term('fantasy' + race_type, 10))
        embed.set_thumbnail(url=thumbnail_url)
        embed.add_field(name='_______________', value=list_first_half, inline=True)
        embed.add_field(name='_______________', value=list_second_half, inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='visualize', aliases=['viz'])
    async def get_search_images_(self, ctx, *, search_string):
        """
        Gets an image from a <search_string> and shows it to the user to aid in visualization.
        Example: .visualize beholder
        :param ctx: discord.ext.commands.context [Ignore]
        :param search_string: str [Required]
        """
        embed = Embed(title=f'Image of {search_string}', color=Color.random())
        search_string += " dnd 5e"
        # choose one of the first ten search results
        embed.set_image(url=random.choice(retrieve_image_urls_of_search_term(search_string, 10)))
        await ctx.send(embed=embed)

    @commands.command(name='spell')
    async def lookup_spell_(self, ctx, *, spell_name):
        """
        Looks up a given <spell_name> and returns its information
        Example: .spell Magic Missile
        :param ctx: discord.ext.commands.context [Ignore]
        :param spell_name: str [Required]
        """
        if self.spells_dict is None:
            self.spells_dict = read_spells_from_json()
        spell_names = get_spell_names()
        processed_spell_name = process_spell_name(spell_name)
        processed_spell_names = [process_spell_name(i) for i in spell_names]

        # todo implement auto correct suggestions
        if processed_spell_name not in processed_spell_names:
            await ctx.send(f'The spell "{spell_name}" does not appear to be valid.')
            return

        spell = compile_spell(self.spells_dict, processed_spell_name)

        embed = Embed(title=spell.name, color=Color.random())
        embed.add_field(name='Spell School', value=spell.school, inline=True)
        embed.set_thumbnail(url=SPELL_SCHOOL_ICON_MAP[spell.school.lower()])
        embed.add_field(name='Classes: ', value=get_list_list(spell.classes), inline=True)
        embed.add_field(name='Spell Information: ', value=spell.get_info_string(), inline=False)

        # embed value must be a string with len 1024 or lower
        spell_description_overflow = False
        if len(spell.description) < 1025:
            embed.add_field(name='Description: ', value=spell.description, inline=False)
        else:
            spell_description_overflow = True
        if spell.upcast_description != 'None':
            embed.add_field(name='At Higher Levels: ', value=spell.upcast_description, inline=False)
        embed.add_field(name='From: ', value=spell.ref_location, inline=False)
        await ctx.send(embed=embed)
        if spell_description_overflow:
            await ctx.send("```" + spell.name + '\nDescription:\n\t' + spell.description + "```")

    @commands.command(name='feat')
    async def lookup_feat_(self, ctx, *, feat_name):
        """
        Looks up a given <feat_name> and returns its information
        Example: .feat Actor
        :param feat_name: str [Required]
        :param ctx: discord.ext.commands.context [Ignore]
        """
        if self.feat_dict is None:
            self.feat_dict = read_feats_dict_from_json()
        processed_feat_name = feat_name.lower()
        names = get_feat_names()
        processed_names = [i.lower() for i in names]

        # todo implement auto correct suggestions
        if processed_feat_name not in processed_names:
            await ctx.send(f'The feat "{feat_name}" does not appear to be valid.')
            return
        feat = compile_feat(self.feat_dict, processed_feat_name)
        embed = Embed(title=feat.name, color=Color.random())
        embed.add_field(name='Feat Description', value=feat.description.replace('*', '> '), inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='exchange', aliases=['exc', 'trade'])
    async def exchange_currency_(self, ctx, current_money, operation, cost):
        """
        Takes an amount of money and adds or subtracts it from another amount of money from it.
        Example: .exchange 1gp - 10cp2sp
        :param cost: str A string representing the amount of money that is to be added or subtracted [Required]
        :param operation: str the operation done on the two amounts [Required]
        :param current_money: str a string representing the current money the player has [Required]
        :param ctx: discord.ext.commands.context [Ignore]
        """
        if not (valid_csegp_string(current_money) and valid_csegp_string(cost)):
            await ctx.send("INVALID FORM: type .help exchange for more.")
            return

        embed = Embed(title='Exchange Summary', color=Color.random())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name='Operation', value=current_money + ' ' + operation + ' ' + cost, inline=False)

        if operation == '-':
            value = convert_from_csegp(subtract_from_gold(current_money, cost))
            embed.add_field(name='Result', value=value)
        elif operation == '+':
            value = convert_from_csegp(add_to_gold(current_money, cost))
            embed.add_field(name='Result', value=value)
        else:
            await ctx.send(f'The operation {operation} is not valid please use "+" or "-".')
            return
        await ctx.send(embed=embed)

    @commands.command(name='compress', aliases=['compress_money', 'cMoney'])
    async def compress_currency_(self, ctx, money_amount: str):
        """
        Takes and amount of money and returns the most compressed version available
        Example: .compress 100cp2sp
        :param money_amount: str A string representing the amount of money to be compressed [Required]
        :param ctx: discord.ext.commands.context [Ignore]
        """
        if not valid_csegp_string(money_amount):
            await ctx.send("INVALID FORM: type .help compress for more.")
            return

        amount_list = convert_to_csegp(money_amount)
        copper_amount = convert_to_copper(amount_list)
        compressed_list = compress_copper(copper_amount)
        value_str = convert_from_csegp(compressed_list)

        embed = Embed(title='Exchange Summary', color=Color.random())
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name='Conversion', value=value_str)
        await ctx.send(embed=embed)
