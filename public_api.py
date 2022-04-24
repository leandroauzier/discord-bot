import requests
import time
import logging
from env_search import BEARER_PUBLIC_API, PUBLIC_API

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def retry(func, retries=4):
    def retry_wrapper(*args, **kwargs):
        attempts = 1
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                logger.error("RequestException - number of attempts: %d", attempts)
                time.sleep(2)
                attempts += 1
            if attempts >= retries:
                return 'Couldn establish conection!'
    return retry_wrapper

def base_data():
    base = PUBLIC_API
    headers = {
        "Authorization": f"Bearer {BEARER_PUBLIC_API}"
    }
    return base, headers


@retry
def list_of_collections():
    base, headers = base_data()
    resp = requests.get(url='https://apexgoapi.com/v1/collections?limit=100', headers=headers)
    return resp.json()

@retry
def list_of_transactions(collection):
    base, headers = base_data()
    resp = requests.get(url='https://apexgoapi.com/v1/transactions?collection_name={collection}&offset=50', headers=headers)
    return resp.json()