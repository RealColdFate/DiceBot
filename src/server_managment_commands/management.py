from discord.ext import commands
from discord.utils import get


class Management(commands.Cog):
    @commands.command(name='role', alieses=['set_role', 'choose_role', 'make_role'], pass_context=True)
    async def set_role(self, ctx, role_name):
        """
        Sets the users role to the provided role when in the "set-role" channel
        Example: .role Barbarian
        :param ctx: discord.ext.commands.context [Ignore]
        :param role_name: str [Required]
        """
        # check to see if we are in the right channel
        if ctx.channel.name != 'set-role':
            # delete user message and delete bot message after 5 seconds
            await ctx.message.delete()
            await ctx.send('set your role in the "set-role" channel', delete_after=5)
            return

        author = ctx.message.author
        role = get(author.guild.roles, name=role_name)

        # check to see if the role is valid
        if role is None:
            await ctx.send(f'Invalid Role: "{role_name}"')
            return
        # try to give the user the role
        try:
            await author.add_roles(role)
        except Exception as e:
            print('command: add_role has failed')
            print("user: ", ctx.message.author, "requesting role: ", role_name)
            print(str(e))
            await ctx.send("There was an error assigning this role")
        else:
            await ctx.send('Verified: {} now has the role "{}"'.format(author.name, role_name))
