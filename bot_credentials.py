import discord
import logging
from env_search import DISCORD_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    guild_count = 0
    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1
    print("this bot is in " + str(guild_count) + " guilds. \n")

    for one in client.guilds:
        if one.name == 'GUILD':
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{one.name}(id: {one.id})\n'
    )

    members = '\n - '.join([member.name for member in one.members])
    print(f'Guild Members:\n - {members}')


try:
    client.run(DISCORD_TOKEN)
except Exception as e:
    logging.error('Could not connect to Discord!', exc_info=True)
    raise e
