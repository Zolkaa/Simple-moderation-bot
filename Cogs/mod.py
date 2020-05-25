import discord
from discord.ext import commands
import json
import tracemalloc

'''
You must create a json file. Name: warns.json.
You must create a role. Name: Muted
''' 

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            '''
            Costumizable argument error
            '''

        if isinstance(error, commands.MissingPermissions):
            '''
            Costumizable permission error
            '''

        if isinstance(error, commands.CommandError):
            print (error)

    @commands.command()
    async def kick(self, msg, member: discord.Member, *, reason):
        if msg.author.guild_permissions.kick_members==True:
            await member.kick(reason=reason)
            await msg.send('I kicked <@!{}>! Reason: {}'.format(member.id, reason))

    @commands.command()
    async def ban(self, msg, member: discord.Member, *, reason):
        if msg.author.guild_permissions.kick_members==True:
            await member.ban(reason=reason)
            await msg.send('I banned <@!{}>! Reason: {}'.format(member.id, reason))

    @commands.command()
    async def unban(self, msg, memberid):
        if msg.author.guild_permissions.ban_members:
            user = await self.bot.fetch_user(memberid)
            if user is not None:
                await msg.guild.unban(user)
                await msg.send('I unbanned <@!{}>!'.format(user.id))

            else:
                await msg.send('User not found!')

    @commands.command()
    async def mute(self, msg, member:discord.Member, *, reason):
        if msg.author.guild_permissions.manage_roles==True:
            role = discord.utils.get(msg.guild.roles, name='Muted')
            await member.add_roles(role)
            await msg.send('I muted <@!{}>! Reason: {}'.format(member.id, reason))

    @commands.command()
    async def unmute(self, msg, member: discord.Member):
        if msg.author.guild_permissions.manage_roles==True:
            role = discord.utils.get(msg.guild.roles, name='Muted')
            await member.remove_roles(role)
            await msg.send('I unmuted <@!{}>!'.format(member.id))

    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason):
        if ctx.author.guild_permissions.ban_members==True:
            warn = 1
            warn = int(warn)
            with open('warns.json', 'r') as f:
                msg = json.load(f)
                f.close()

            warns = int(msg[str(member.id)])
            msg[str(member.id)] = f'{warns + warn}'

            with open('warns.json', 'w') as r:
                json.dump(msg, r, indent=4)
                f.close()

            warns = warns + warn

            await ctx.send('I warned <@!{}>! User warnings: {}. Reason: {}'.format(member.id, int(warns), reason))

            if warns == '10': #The limit of the warns
                reason = 'Automatic warn'
                await member.ban(reason=reason)
            

def setup(bot):
    bot.add_cog(Moderation(bot))