
import logging
import os
from pymongo import MongoClient, errors

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

try: 
    uri = os.environ["MONGO_URI"]
    base_db_name = os.environ["MONGO_BASE_DB_NAME"]
    users_db_name = os.environ["MONGO_USERS_DB_NAME"]
    users_coll_name = os.environ["MONGO_USERS_COLL_NAME"]
except KeyError as e: 
    logger.error(f"Error parsing mongo params: {e}")

client = None
collection = None

def get_client(connection_string: str = uri): 
    global client

    if client is not None: 
        return client
    
    try: 
        logger.info("Creating MongoClient")
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)

        return client
    
    except errors.ServerSelectionTimeoutError as Argument:
        logger.warning(f"MongoDB not reachable: {Argument}")
        raise
    except Exception as e: 
        logger.warning(f"Unexpected error creating client: {e}")
        raise

def get_collection(username: str, collection_name: str): 
    global client

    try: 
        if client is None: 
            client = get_client()

        database_name = f"{username}-{base_db_name}"
        db = client[database_name]
        collection = db[collection_name]
        logger.info(f"Accessed collection: {collection_name}")

        return collection
    
    except errors.ServerSelectionTimeoutError as Argument:
        logger.error(f"MongoDB not reachable: {Argument}")
        raise
    except Exception as e: 
        logger.error(f"Unexpected error creating client: {e}")
        raise   

def get_users_coll(): 
    global client

    try: 
        if client is None: 
            client = get_client()

        collection = client[users_db_name][users_coll_name]
        logger.info(f"Accessed collection: {users_coll_name}")

        return collection
        
    except errors.ServerSelectionTimeoutError as Argument:
        logger.error(f"MongoDB not reachable: {Argument}")
        raise
    except Exception as e: 
        logger.error(f"Unexpected error creating client: {e}")
        raise  
