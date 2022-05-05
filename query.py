import os
import mysql.connector
import logging
from env_search import DB_STRING

connection_list = [i.split("=") for i in os.environ.get("DB_STRING").split("+")]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def conn():
    try:
        discord_db = mysql.connector.connect(
        host= connection_list[0][1],
        user= connection_list[1][1],
        password= connection_list[2][1],
        database= connection_list[3][1]        
        )
        discord_db.commit()
        logger.info('Connected to the database')
        return discord_db
    except Exception as e:
        logger.error("Couldn't connect to database", exc_info=True)
        raise e
    
def get_from_db():
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
        
def get_collection_from_db(server_id):
    try:
        cn = conn()
        cs = cn.cursor()
        cs.execute(f"SELECT Collection FROM acronyms WHERE server_id = {str(server_id)}")
        result = cs.fetchall()
        response = result[0][0]
        print(f'Result: {response}')
        return response
    except Exception as e:
        logger.error("There was an error fetching server_id!", exc_info=True)
        raise e
    finally:
        cn.close()


def set_collection_server_id(contract, server_id):
    print(f'Contract: {contract}')
    print(f'Server_ID: {server_id}')
    print('ENTERED QUERY')
    c_list = get_from_db()
    for c in c_list:
        print(c)
        if contract != c[3]:
            pass
        elif contract == c[3]:
            return False
    try:
        cn = conn()
        cs = cn.cursor()
        cs.execute(f"INSERT INTO acronyms (server_id, contract) Value ({server_id}, {contract});")
        print('QUERY EXECUTED!')
        result = cs.fetchall()
    except Exception as e:
        logger.error("There was an error inserting collection!", exc_info=True)
        raise e
    finally:
        cn.close()