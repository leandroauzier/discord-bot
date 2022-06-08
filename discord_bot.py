import asyncio
import discord
import os
import logging
from env_search import DISCORD_TOKEN
from discord.ext import commands
from public_api import list_of_collections, list_of_transactions, info_from_collection
from query import Set_collections_tb, get_collection_from_acronyms_id, Set_acronyms, get_from_api
from vips import svg_conversion

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def get_collection_and_contract():
    reformed=[]
    for i in range(10):
        c = list_of_collections(150, i*150)
        if c is not None:
            page = [(coll['name'], coll['contract_address']) for coll in c]
            reformed.append(page)
        break
    print(f'Reformed: {reformed[0]}')
    return reformed

client = commands.Bot(command_prefix='!')
client.remove_command('help')

@client.command()
async def hello(ctx, *, arg):
    texto = f"Hello! you said:\n> {arg}"
    await ctx.channel.send(texto)

async def on_ready():
    print(f'Bot is ready for use on Discord!')
    
@client.command()
async def refresh(ctx, *arg):
    try:
        db = get_from_api()
        for c in db:
            Set_collections_tb(c[0],c[1])
        advise = discord.Embed("Database refreshed!")
        await ctx.member.send(advise)
    except Exception as e:
        raise e

@client.command()
async def getcollection(ctx):
    if ctx.author == client.user:
        return
    try:
    # menu = discord.Embed(title="Config your main bot collection", color=0xA7F3D0)
    # menu.description = 'Type the number for configuration:\n\n:one: - Set Collection\n:two: - Get Configured Collection'
    # await ctx.channel.send(embed=menu)
    # def check(m):
    #     return m.author == ctx.author and m.channel == ctx.channel
    # try:
    #     m = await client.wait_for('message', timeout=15.0, check=check)
    #     if m.content == '1':
    #         print('Input 1')
            # new_contract = discord.Embed(color=0xA7F3D0)
            # new_contract.description=f'{m.author}, Please insert the contract of your collection:'
            # await ctx.channel.send(embed=new_contract)
            # def confirm(contract):
            #     return m.author == ctx.author and contract.channel == ctx.channel
            # try:
            #     contract = await client.wait_for('message', check=confirm)
            #     print(f"THIS SERVER ID IS: {ctx.guild.id}")
            #     checking = Set_acronyms(str(contract.content), str(ctx.guild.id))
            #     if checking == 0:
            #         await ctx.channe.lsend('This collection was already set up!')
            #     elif checking == 1:
            #         await ctx.channel.send('Collection Updated!')
            #     elif checking == 2:
            #         await ctx.channel.send('New collection Set up!')
            # except Exception as e:
            #     raise e
            # return
    # if m.content == '2':
    #     print('Input 2')
        cur_server_id = ctx.guild.id
        print('reached')
        if await ctx.channel.send(get_collection_from_acronyms_id(cur_server_id)) is not None:
            return
        else:
            await ctx.channel.send('Invalid option, exiting...')
    except asyncio.TimeoutError:
        await ctx.channel.send(f"\n:stopwatch: {ctx.author.mention}, The timeout has reached, please try again")
        
    
@client.command()
async def help(ctx, *arg):
        embed = discord.Embed(title="Apexgo Bot Help", color=0xA7F3D0)
        embed.description = ("**__Bot commands__**:\n\n"
        "**Rank:**\n!rank\n"
        "**NFT Stats:**\n!nft <id>\n"
        "**Refresh the collection's table:**\n!refresh\n"
        "**Get current Collection:**\n!getcollection\n"
        "**Set a Collection:**\n!setcollection\n"
        "**Help:**\n!help\n"
        "**Rules:**\n!rules\n"
        "**Apexgo Extension:**\n!ext\n"
        "**Transactions**\n!transactions <days>\n")
        await ctx.channel.send(embed=embed)
@client.command()
async def rules(ctx, *arg):
        embed = discord.Embed(title="Apexgo Rules", color=0xA7F3D0)
        embed.description=(f":rotating_light: Check out our server rules: :rotating_light:\n\n1-Be respectful\n" # noqa:
                                f"2- Sending any harmful material such as malwares or harmware results in an immediate and permanent ban.\n" # noqa:
                                f"3- Use English grammar and spelling and don't spam.\n"
                                f"4- Post content in the correct channels.\n"
                                f"5- Don't post someone's personal information without permission.\n"
                                f"6- Do not post NSFW content.\n\n"
                                f"If you have any doubts or questions, please contact the Admins")
        await ctx.channel.send(embed=embed)
@client.command()
async def ext(ctx, *arg):
        embed = discord.Embed(title="Apexgo Extension", color=0xA7F3D0)
        embed.description=(f"Use our of ApexGo Extension!\nhttps://apexgo.io/extension/")
        await ctx.channel.send(embed=embed)
        
@client.command()
async def transactions(ctx, *arg):
        cur_server_id = ctx.guild.id
        days = int(arg[0])
        slct_collection = get_collection_from_acronyms_id(cur_server_id)
        transactions = []
        for c in range(30):
            ft = list_of_transactions(slct_collection, days,50,c*50)
            full_transactions = ft['response']
            if full_transactions is not None:
                page = [i for i in full_transactions]
                transactions.append(page)
            break
        count_trans = 0
        # current_highest = 0
        # current_lowest = 999999999999999999999
        # curr_lowest_coin = ""
        # curr_highest_coin = ""
        # highest_t = 0
        # lowest_t = 0
        if len(transactions) > 0:
            print(len(transactions))
            embed = discord.Embed(title=f"Transactions {arg[0]}", color=0xA7F3D0)
            embed.description ="**ID**   |   **Price**   \n\n"
            for ind, t in enumerate(transactions[0]):
                # embed.add_field(name='\u200b',value='\u200b')
                # embed.add_field(name="**#**", value=f'**{ind+1}**', inline=True)
                # embed.description += f"**{ind+1}**   |   **[" + t['token_id'] +"]"+"(https://apexgo.io/nft/"+ t['collection_name'] +'/'+ t['token_id'] +')**'"   |   **"+str(int(t['price'])/ pow(10, 18)) + ' ' + t['coin_symbol']**"\n"
                # embed.add_field(name="**ID**", value="[" + t['token_id'] +"]"+"(https://apexgo.io/nft/"+ t['collection_name'] +'/'+ t['token_id'] +')', inline=True)
                # embed.add_field(name="**Price**", value=str(int(t['price'])/ pow(10, 18)) + ' ' + t['coin_symbol'], inline=True)
                # added_msg = '# **ID:** ' + "[" + t['token_id'] +"]"+"(https://apexgo.io/nft/"+ t['collection_name'] +'/'+ t['token_id'] +')' + ' , **value:** ' + str(int(t['price'])/ pow(10, 18)) + ' ' + t['coin_symbol']
                if len(embed.description) <= 2000:
                    print('entered')
                    embed.description += (f"{t['token_id']}"+"(https://apexgo.io/nft/"+ t['collection_name'] +'/'+ t['token_id'] +')   |   '+str(int(t['price'])/ pow(10, 18)) + ' ' + t['coin_symbol']+"\n")
                    count_trans += 1
                    print('added more in description')
                    # if int(t['price']) > current_highest:
                    #     current_highest = int(t['price'])
                    #     curr_highest_coin = t['coin_name']
                    # if int(t['price']) < current_lowest:
                    #     current_lowest = int(t['price'])
                    #     curr_lowest_coin = t['coin_name']
                elif len(embed.description) > 2000:
                    print('full... printing...')
                    await ctx.channel.send(embed=embed)
            await ctx.channel.send(embed=embed)
            # lowest_t = current_lowest / pow(10, 18)
            # lowest_coin = curr_lowest_coin
            # highest_t = current_highest / pow(10, 18)
            # highest_coin = curr_highest_coin
            embed.description = ''
            message = discord.Embed(title='', color=0xA7F3D0)
            message.description = ''
            message.description += f"\n:point_up: Check out the NFT on Apexgo.io by clicking on ID Number :point_up: "
            if count_trans == 1:
                embed.description += f"\n:triangular_flag_on_post: This was the last **{count_trans}** Transaction of {slct_collection} in the last **{days}** days"
                await ctx.channel.send(embed=message)
                message.description = ''
                # \n :arrow_forward: The Floor Price has value of {lowest_t} {lowest_coin}\n:arrow_forward: The Celling Price has value of {highest_t} {highest_coin}
            elif count_trans > 1:
                message.description += f"\n:triangular_flag_on_post: These were the last {count_trans} Transactions of {slct_collection} in the last {days} days :triangular_flag_on_post:"
                await ctx.channel.send(embed=message)
                message.description = ''
                # \n:arrow_forward: The Floor Price has value of {lowest_t} {lowest_coin}\n:arrow_forward: The celling Price has value of {highest_t} {highest_coin}
        else:
            no_transactions_msg = f"There were no {slct_collection} Transactions in the last {days} days!"
            await ctx.channel.send(no_transactions_msg)

@client.command()
async def nft(ctx, *arg):
        if arg[0].isnumeric():
            token_id = str(arg[0])
            cur_server_id = ctx.guild.id
            slct_collection = get_collection_from_acronyms_id(cur_server_id)
            print('Got Selected collection: ' + slct_collection)
            nft_info = info_from_collection(slct_collection)
            print('Got NFT info' + nft_info['name'])
            msg = ''
            img = ''
            title = ''
            for i in nft_info['response']['nfts']:
                print(f'TOKEN:{token_id}')
                if i['nft_id'] == token_id:
                    print('YES')
                    for k,v in i.items():
                        if k in ['nft_id','name','image','meta_score','rarity_score',
                                'score','ranking', 'adjusted_meta_score', 'adjusted_rarity_score', 
                                'adjusted_score', 'adjusted_ranking', 'last_price', 'owner'] and v not in [None, '']:
                            if k == 'name':
                                title += v
                                continue
                            elif k == 'image':
                                img += v
                                continue
                            elif k == 'score':
                                v = v/100
                                msg+=f'{k}: {v}'+'\n'
                                continue
                            elif k == 'last_price':
                                v = int(v)/pow(10, 18)
                                msg+=f'{k}: {v}'+'\n'
                                continue
                            else:
                                msg+=f'{k}: {v}'+'\n'
            embed = discord.Embed(title=f'{title}' ,color=0xA7F3D0)
            embed.description = msg
            n_img = svg_conversion(img)
            await ctx.channel.send(file=discord.File(n_img))
            await ctx.channel.send(embed=embed)
            print(os.getcwd())
            if os.path.isfile(n_img):
                os.remove(n_img)
            else:
                raise Exception('File not found')
        else:
            advise = discord.Embed(title=f"ERROR:", description="Please use the a command like this:\n\n**!floor <token_id>**", color=discord.Color.red())
            await ctx.channel.send(embed=advise)
        
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await ctx.send(embed = discord.Embed(description = f'Invalid command, use **!help** to see our command list!', color=discord.Color.red()))
    
async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        ctx = f'{member.mention} just entered on {guild.name}'
        embed = discord.Embed(title="Apexgo Bot Help", color=0xA7F3D0)
        embed.description = ("__Bot commands__:\n\n"
        "**Rank:**\n!rank\n"
        "**NFT Stats:**\n!nft <id>\n"
        "**Help:**\n!help\n"
        "**Rules:**\n!rules\n"
        "**Apexgo Extension:**\n!ext\n"
        "**Transactions**\n!transactions <days>\n")
        await ctx.channel.send(ctx)
        await member.send(embed=embed)
            
try:
    # intents = discord.Intents.default()
    # intents.members = True
    # client = ApexClient(intents=intents)
    client.run(DISCORD_TOKEN)
except Exception as e:
    logger.error('ERROR: Discord key is not valid')
    raise e
