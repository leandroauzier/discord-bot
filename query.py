import mysql.connector
import logging
from env_search import DATABASE, HOST, PASSWORD, USER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def conn():
    try:
        discord_db = mysql.connector.connect(
        host= HOST,
        database= DATABASE,
        user= USER,
        password= PASSWORD
        )
        discord_db.commit()
        logger.info('Connected to the database')
        return discord_db
    except Exception as e:
        logger.error("Couldn't connect to database", exc_info=True)
        raise e
'''
GET FUNCTIONS
'''
    
def get_from_acronyms():
    db_query = []
    try:
        cn = conn()
        cs = cn.cursor()
        cs.execute("SELECT * FROM acronyms;")
        result = cs.fetchall()
        if result is not None:
            for r in result:
                db_query.append(r)
            return db_query
        else:
            raise Exception('Table is empty!!!')
    except Exception as e:
        logger.error("There was an error fetching acronyms!", exc_info=True)
        raise e
    finally:
        cn.close()
        
def get_collection_from_acronyms_id(server_id):
    try:
        cn = conn()
        cs = cn.cursor()
        cs.execute(f"SELECT collections.name, collections.contract, servers.server FROM collections LEFT JOIN servers ON collections.id = servers.id WHERE servers.server = '{server_id}' ORDER BY collections.id;")
        result = cs.fetchall()
        response = result[0][0]
        print(f'Result: {response}')
        return response
    except Exception as e:
        logger.error("There was an error fetching server_id!", exc_info=True)
        raise e
    finally:
        cn.close()
        

'''
SET FUNCTIONS
'''

def Set_collections_tb(name, contract):
    try:
        cn = conn()
        cs = cn.cursor()
        cs.execute(f"INSERT INTO collections (name, contract) Value ('{name}', '{contract}');")
        result = cs.fetchall()
    except Exception as e:
        logger.error("Error on inserting new Collection!", exc_info=True)
        raise e
    finally:
        cn.close()
        
def Set_server_tb(new_server):
    check = get_collection_from_acronyms_id()
    try:
        cn = conn()
        cs = cn.cursor()
        cs.execute(f"INSERT INTO servers (server) Value ('{new_server}');")
        result = cs.fetchall()
    except Exception as e:
        logger.error("Error on inserting new server!", exc_info=True)
        raise e
    finally:
        cn.close()

def Set_acronyms(collection_id, server_id):
    c_list = get_from_acronyms()
    for c in c_list:
        print(c)
        id_c = collection_id(c)
        if server_id != c[2]:
            continue
        elif server_id == c[2] and collection_id == c[3]:
            print('return 0')
            return 0
        elif server_id == c[2] and collection_id != c[3]:
                try:
                    cn = conn()
                    cs = cn.cursor()
                    cs.execute(f"UPDATE acronyms SET collection_id='{collection_id}' WHERE server_id='{server_id}';")
                    cn.commit()
                    print('UPDATED EXECUTED!')
                except Exception as e:
                    logger.error("There was an error updating collection!", exc_info=True)
                    raise e
                finally:
                    cn.close()
                    print('returned 1')
                    return 1
    try:
        cn = conn()
        cs = cn.cursor()
        cs.execute(f"INSERT INTO acronyms (server_id, collection_id) Value ('{server_id}', '{collection_id}');")
        print('QUERY EXECUTED!')
        result = cs.fetchall()
    except Exception as e:  
        logger.error("There was an error inserting collection!", exc_info=True)
        raise e
    finally:
        cn.close()
        print('returned 2')
        return 2
