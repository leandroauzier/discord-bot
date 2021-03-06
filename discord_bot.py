import asyncio
import discord
import os
import logging
from env_search import DISCORD_TOKEN
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

client = commands.Bot(command_prefix='!')
client.remove_command('help')

@client.command()
async def oi(ctx):
    await ctx.channel.send(f"Olá!, {ctx.message.author.mention}")

async def on_ready():
    print(f'Bot está pronto para uso!')
    
@client.command()
async def help(ctx, *arg):
        embed = discord.Embed(title="Blackcup bot Help", color=0x4b286c)
        embed.description = ("**__Comandos do Bot__**:\n\n"
        "**O bot irá lhe mandar um olá!:**\n!oi\n"                             
        "**Help/ajuda:**\n!help\n"
        "**Regras do server:**\n!regras\n")
        await ctx.channel.send(embed=embed)
@client.command()
async def regras(ctx, *arg):
        embed = discord.Embed(title="", color=0x4b286c)
        embed.description=(f":rotating_light: Nossas regras de conduta do servidor: :rotating_light:\n\n1-Seja respeitoso\n" # noqa:
                                f"2- O envio de qualquer material nocivo, como malwares ou harmwares, resulta em uma Ban imediata e permanente.\n" # noqa:
                                f"3- Pode falar em Português-Brasil ou Inglês mas não faça spam.\n"
                                f"4- Poste conteúdo nos canais corretos.\n"
                                f"5- Não publique informações pessoais de alguém sem permissão.\n"
                                f"6- Não poste conteúdo NSFW.\n\n"
                                f"Em caso de dúvidas ou perguntas, entre em contato com os administradores")
        await ctx.channel.send(embed=embed)
        
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'Comando inválido, use **!help** para ver a lista de comandos', color=discord.Color.red()))
    
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        ctx = f'{member.mention} acabou de entrar em {guild.name}'
        embed = discord.Embed(title="Blackcup bot Help", color=0x4b286c)
        embed.description = ("__Comandos do Bot__:\n\n"
        "**oi:**\n!oi\n"
        "**Help:**\n!help\n"
        "**Regras:**\n!rules\n")
        await ctx.channel.send(ctx)
        await member.send(embed=embed)
            
try:
    client.run(DISCORD_TOKEN)
except Exception as e:
    logger.error('ERROR:Chave discord não é válida')
    raise e
