from src.configuration.mongodb_connection import MongoDatabaseClient

if __name__ == '__main__':
    mongo_db_client = MongoDatabaseClient()
    print(mongo_db_client.database.list_collection_names()) # type: ignore
