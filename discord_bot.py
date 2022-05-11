from secrets import token_bytes
import time
import math
import discord
import logging
from env_search import DISCORD_TOKEN
from public_api import list_of_collections, list_of_transactions, info_from_collection
from query import get_collection_from_db, set_collection_server_id

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
        if message.author == client.user:
            return
        if message.content == '!configbot':
            await message.channel.send('Type the number for configuration:\n1-Set Collection')
            response = await client.wait_for('message')
            print(response.content)
            if response.content == '1' and message.author == self.user:
                await message.channel.send('Please insert the contract of your collection:')
                contract = await client.wait_for('message')
                if set_collection_server_id(contract.content, message.guild.id) == False:
                    await message.channel.send('This collection was already set up!')
            else:
                print("Don't match any option")
        
        elif message.content == '!help':
            dm = (f":wave: {message.author.name}, Here are some commands you can type (always use '!'):\n\n"
            "- !help [bot returns you this command list again]\n"
            "- !hello [bot returns you a hello text]\n"
            "- !rules [returns you the rules that this server demands from its members]\n"
            "- !api [returns you the link of ApexGO's Public API documentation]\n"
            "- !transactions <days> [returns you the last 20 transactions in the input days, (7, 15 ,30)]\n")
            await message.channel.send(dm)
        elif message.content == '!hello':
            await message.channel.send(f'!Hello, {message.author.name}')
        elif message.content == '!rules':
            await message.channel.send(f":rotating_light: {message.author.name}, Check out our server rules: :rotating_light:\n\n1-Be respectful\n" # noqa:
                                    f"2- Sending any harmful material such as malwares or harmware results in an immediate and permanent ban.\n" # noqa:
                                    f"3- Use English grammar and spelling and don't spam.\n"
                                    f"4- Post content in the correct channels.\n"
                                    f"5- Don't post someone's personal information without permission.\n"
                                    f"6- Do not post NSFW content.\n\n"
                                    f"If you have any doubts or questions, please contact the Admins")
        elif message.content == '!api':
            await message.channel.send(f"@{message.author.name}, here's the link of ApexGo API:\nhttps://apexgo.io/extension/")
          
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
                    await message.channel.send(f"\n:triangular_flag_on_post: This was the last {count_trans} Transaction of {slct_collection} in the last {days} days\n:arrow_forward: The Floor Price has value of {lowest_t} {lowest_coin}\n:arrow_forward: The Celling Price has value of {highest_t} {highest_coin}")
                elif count_trans > 1:
                    await message.channel.send(f"\n:triangular_flag_on_post: These were the last {count_trans} Transactions of {slct_collection} in the last {days} days\n:arrow_forward: The Floor Price has value of {lowest_t} {lowest_coin}\n:arrow_forward: The celling Price has value of {highest_t} {highest_coin}")
            else:
                no_transactions_msg = f"There were no {slct_collection} Transactions in the last {days} days!"
                await message.channel.send(no_transactions_msg)
                
        elif message.content == f'!nft':
            await message.channel.send(f"{message.author.mention}, Please insert the ID of the NFT you want to know more about:")
            token_id = await client.wait_for('message')
            cur_server_id = message.guild.id
            slct_collection = get_collection_from_db(cur_server_id)
            nft_info = info_from_collection(slct_collection)
            await message.channel.send(f"{message.author.mention}, Here's the info about the NFT you requested:\n\n")
            msg = ''
            for i in nft_info['response']['nfts']:
                if i['nft_id'] == token_id:
                    for k,v in i.items():
                        if k in ['D_token_ID', 'nft_id','name','image','meta_score','rarity_score',
                                'score','ranking', 'adjusted_meta_score', 'adjusted_rarity_score', 
                                'adjusted_score', 'adjusted_ranking', 'last_price', 'owner'] and v not in [None, '']:
                            msg+=f'{k}: {v}'+'\n'
                            if k in 'image':
                                img = v
                    await message.channel.send(img)

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
