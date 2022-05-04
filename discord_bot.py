import time
import math
import discord
import logging
from env_search import DISCORD_TOKEN
from public_api import list_of_collections, list_of_transactions
from query import get_from_db, get_collection_from_db, set_collection_server_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_collections():
    myReq = list_of_collections()
    reformed = []
    for coll in myReq:
        if coll is not None:
            reformed.append((coll['name'], coll['acronym']))
    return reformed


class ApexClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} is ready for use on Discord!')
    async def on_message(self, message):
        if message.content == '!configbot':
            print('START CONFIGBOT')
            await message.channel.send('Type the number for configuration:\n1-Set Collection')
            response = await client.wait_for('message')
            print(response.content)
            if response.content == '1':
                print('ENTERED 1')
                await message.channel.send('Please insert the contract of your collection:')
                contract = await client.wait_for('message')
                if set_collection_server_id(contract.content, message.guild.id) == False:
                    await message.channel.send('This collection was already set up!')
                print('FUNCTION FINISHED!')
            else:
                print("Don't match any option")
        
        elif message.content == '!help' or message.content == '!Help' or message.content == '!HELP:':
            dm = (f"{message.author.name}, Here are some commands you can type (always use '!'):\n"
            "- !help [bot returns you this command list again]\n"
            "- !hello [bot returns you a hello text]\n"
            "- !rules [returns you the rules that this server demands from its members]\n"
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
          
        elif message.content in ['!transactions 7','!transactions 15','!transactions 30']:  
            days = 0
            if message.content == f'!transactions 7':
                days = 7
            elif message.content == f'!transactions 15':
                days = 15
            elif message.content == f'!transactions 30':
                days = 30
            cur_server_id = message.guild.id
            slct_collection = get_collection_from_db(cur_server_id)            
            full_transactions = list_of_transactions(slct_collection,days)
            print(full_transactions)
            transactions = []
            for i in full_transactions:
                if len(transactions) < 20:
                    transactions.append(i)
            print(len(transactions))
            print(transactions)
            waitsec = 1
            count_trans = 0
            current_highest = 0
            current_lowest = 999999999999999999999
            curr_lowest_coin = ""
            curr_highest_coin = ""
            highest_t = 0
            lowest_t = 0
            if len(transactions) > 0:
                embed = discord.Embed()
                for t in transactions:
                    embed.description = '# ID: ' + "[" + t['token_id']+"]"+"(https://apexgo.io/nft/"+t['collection_name']+'/'+t['token_id']+')' + ' , value: ' + str(int(t['price'])/ pow(10, 18)) + ' ' + t['coin_symbol']
                    if len(str(t)) <= 2000:
                        await message.channel.send(embed=embed)
                        count_trans += 1
                        if int(t['price']) > current_highest:
                            current_highest = int(t['price'])
                            curr_highest_coin = t['coin_name']
                        if int(t['price']) < current_lowest:
                            current_lowest = int(t['price'])
                            curr_lowest_coin = t['coin_name']
                    else:
                        print('The length was greater than 2000')
                lowest_t = current_lowest / pow(10, 18)
                lowest_coin = curr_lowest_coin
                highest_t = current_highest / pow(10, 18)
                highest_coin = curr_highest_coin
                await message.channel.send(f"\n:point_up: Check out the NFT on Apexgo.io by clicking on ID Number :point_up: ")
                if count_trans == 1:
                    await message.channel.send(f"\n:triangular_flag_on_post: This was the last {count_trans} Transaction of {slct_collection} in the last {days} days\n:arrow_forward: The Floor Price has value of {lowest_t} {lowest_coin}\n:arrow_forward: The Highest Price has value of {highest_t} {highest_coin}")
                elif count_trans > 1:
                    await message.channel.send(f"\n:triangular_flag_on_post: These were the last {count_trans} Transactions of {slct_collection} in the last {days} days\n:arrow_forward: The Floor Price has value of {lowest_t} {lowest_coin}\n:arrow_forward: The Highest Price has value of {highest_t} {highest_coin}")
            else:
                no_transactions_msg = f"There were no {slct_collection} Transactions in the last {days} days!"
                await message.channel.send(no_transactions_msg)
                
        elif message.content == '!dev:collections':
            collections = get_from_db()
            waitsec = 1
            coll_list = ""
            for c in collections:
                if int(math.log10(c[0]))+1 + len(c[1]) + len(c[2]) + len(coll_list) <= 2000:
                    coll_list += c[1] + ' - ' + c[2] +'\n'
                elif int(math.log10(c[0]))+1 + len(c[1]) + len(c[2]) + len(coll_list) > 2000:
                    await message.author.send(coll_list)
                    coll_list = ""
                    coll_list += c[1] + ' - ' + c[2] +'\n'
                    print(f'sleeping for {waitsec} seconds...')
                    time.sleep(waitsec)
            if len(coll_list) > 0:
                print(coll_list)
                await message.author.send(coll_list)
            await message.author.send(f"\n:arrow_up: :arrow_up: This are the collections that you can search by using '!transactions <acronym>' :arrow_up: :arrow_up: ")

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
