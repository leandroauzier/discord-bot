from distutils.log import info
from subprocess import list2cmdline
import requests
import time
import logging
from env_search import BEARER_PUBLIC_API

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
    headers = {
        "Authorization": f"Bearer {BEARER_PUBLIC_API}"
    }
    return headers


@retry
def list_of_collections(limit, offset):
    resp = requests.get(url=f"https://dev-apexgopublicapi.com/v1/collections?limit={limit}&offset={offset}", headers=base_data())
    pag = resp.json()['paging']['pages']
    if offset <= pag*limit:
        return resp.json()['response']
    else:
        return None

@retry
def list_of_transactions(collection, days):
    resp = requests.get(url=f"https://dev-apexgopublicapi.com/v1/transactions?collection_name={collection}&interval_days={days}", headers=base_data())
    return resp.json()

@retry
def info_from_collection(collection):
    resp = requests.get(url=f"https://dev-apexgopublicapi.com/v1/collection?collection_name={collection}", headers=base_data())
    return resp.json()