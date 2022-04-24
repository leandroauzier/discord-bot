import time
import discord
import logging
from env_search import DISCORD_TOKEN
from public_api import list_of_collections

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_collections():
    print('Entered Function!')
    myReq = list_of_collections()
    reformed = []
    for coll in myReq:
        if coll is not None:
            reformed.append(coll['name'])
    return reformed


class ApexClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} is ready for use on Discord!')

    async def on_message(self, message):
        if message.content == '!help' or message.content == '!Help' or message.content == '!HELP:':
            dm = (f"{message.author.name}, Here are some commands you can type (always use '!'):\n"
            "- !help [bot returns you this command list again]\n"
            "- !hello [bot returns you a hello text]\n"
            "- !rules [returns you the rules that this server demands from its integrants]\n"
            "- !api [returns you the link of ApexGO's Public API documentation]\n")
            await message.channel.send(dm)
        elif message.content == '!hello' or message.content == '!Hello' or message.content == '!HELLO':
            await message.channel.send(f'!Hello, {message.author.name}')
        elif message.content == '!rules' or message.content == '!Rules' or message.content == '!RULES':
            await message.channel.send(f":rotating_light: {message.author.name}, Check out our server rules: :rotating_light:\n\n1-Be respectful\n" # noqa:
                                    f"2- Sending any harmful material such as malwares or harmware results in an immediate and permanent ban.\n" # noqa:
                                    f"3- Use English grammar and spelling and don't spam.\n"
                                    f"4- Post content in the correct channels.\n"
                                    f"5- Don't post someone's personal information without permission.\n"
                                    f"6- Do not post NSFW content.\n\n"
                                    f"If you have any doubts or questions, please contact the Admins")
        elif message.content == '!api':
            await message.channel.send(f"{message.author.name}, here's the link of ApexGo API:\nhttps://apexgo.io/extension/")
        elif message.content == '!transaction tbc':
            await message.author.send(f"Last 50 transactions of Tron Bull Club:\n")
        elif message.content == '!collections':
            collections = get_collections()
            coll_list = ""
            for c in collections:
                if len(c) + len(coll_list) <= 2000:
                    coll_list += c +'\n'
                    print(c)
                elif len(c) + len(coll_list) > 2000:
                    print('this is the list: %s',coll_list)
                    await message.author.send(coll_list)
                    coll_list = ""
                    print('sleeping for 5 seconds...')
                    time.sleep(5)
            await message.author.send(f"\nThis are the collections that you can search by using '!transactions <collection name>':")

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            message = f'{member.mention} just entered on {guild.name}'
            dm = (f"{member.mention}, Here are some commands you can type (always use '!'):\n"
            "- !help [bot returns you this command list again]\n"
            "- !hello [bot returns you a hello text]\n"
            "- !rules [returns you the rules that this server demands from its integrants]\n"
            "- !api [returns you the link of ApexGO's Public API documentation]\n")
            await guild.system_channel.send(message) and await member.send(dm)
            
try:
    intents = discord.Intents.default()
    intents.members = True
    client = ApexClient(intents=intents)
    client.run(DISCORD_TOKEN)
except Exception as e:
    logger.error('BIG ERROR')
    raise e
