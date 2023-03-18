import pymongo
import os
from src.constant.database import DATABASE_NAME
import certifi

ca = certifi.where()


class MongoDatabaseClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDatabaseClient.client is None:
                mongodb_url = os.getenv('MONGODB_PATH')
                MongoDatabaseClient.client = pymongo.MongoClient(
                    mongodb_url, tlsCAFile=ca
                )
            self.client = MongoDatabaseClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e

