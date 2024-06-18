import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from urllib.parse import quote_plus

from src.utils.logging_config import CustomLogger

logger = CustomLogger().logger

class MongoDB():
    def __init__(self, collection_name):
        """Initialize the MongoDB with the database and collection names.

        Args:
        - collection_name (str): Name of the collection within the database.
        """
        self.collection = None
        self.collection_name = collection_name
        self.__set_mongo_uri()
        self.__mongo_connect()

    def __set_mongo_uri(self):
        """
        Load MongoDB configuration from environment variables.

        The function retrieves the MongoDB URL and token from
        environment variables using the `dotenv` module.

        Raises:
            EnvironmentError: If the required MongoDB configuration is not found.
        """
        # Load URL and token from environment variables
        load_dotenv()
        mongodb_username = os.getenv("MONGODB_USERNAME")
        mongodb_password = os.getenv("MONGODB_PASSWORD")
        mongodb_cluster_name = os.getenv("MONGODB_CLUSTER_NAME")
        mongodb_database_name = os.getenv("MONGODB_DATABASE_NAME")
        
        # Escape the mongodb_username and mongodb_password
        mongodb_escaped_username = quote_plus(mongodb_username)
        mongodb_escaped_password = quote_plus(mongodb_password)

        # Extract MongoDB URI from payload data
        mongo_uri = f"mongodb+srv://{mongodb_escaped_username}:{mongodb_escaped_password}@{mongodb_cluster_name}"

        self.mongo_uri = mongo_uri
        self.db_name = mongodb_database_name

        # If any of the required configuration is not found, handle the situation
        if not mongodb_username or not mongodb_password or not mongodb_cluster_name or not mongodb_database_name or not self.collection_name:
            # Log an error, raise an exception, or provide further instructions
            logger.error("MongoDB configuration data is not provided or not found in environment variables.")
            raise EnvironmentError("MongoDB configuration is incomplete. Please provide the necessary information.")

    def __mongo_connect(self):
        """Connect to the MongoDB server and database, and get the specified collection."""
        try:
            # mongo config
            logger.info(self.mongo_uri)

            self.client = MongoClient(self.mongo_uri)
            # Test the connection by accessing a database (e.g., admin)
            # self.client.admin.command('ismaster')

            logger.info("MongoDB Server Connected.")

            # Access the database
            db = self.client[self.db_name]

            # Check if the database exists
            db_list = self.client.list_database_names()
            if self.db_name in db_list:
                logger.info(f"The {self.db_name} database exists.")
            else:
                logger.critical(f"The {self.db_name} database does not exist.")
                logger.info(f"Creating {self.db_name} database.")
                db = self.client[self.db_name]

            # Access the collection
            collection = db[self.collection_name]

            # Check if the collection exists
            collection_list = db.list_collection_names()
            if self.collection_name in collection_list:
                logger.info(f"The {self.collection_name} collection exists.")
            else:
                logger.critical(f"The {self.collection_name} collection does not exist.")
                logger.info(f"Creating {self.collection_name} collection.")
                db.create_collection(self.collection_name)
                logger.info("Created collection '{}'.\n".format(self.collection_name))

            self.collection = collection

            logger.info("success!")
            return {"result": True, "message": "Success!"}

        except ServerSelectionTimeoutError as err:
            logger.error("MongoDB Server Connection Error:", err)
            return {"result": False, "message": "MongoDB Server Connection Error: " + str(err)}
        except OperationFailure as e:
            logger.error("An error occurred while creating the index:", e)
            return {"result": False, "message": "An error occurred while creating the index: " + str(e)}
        except Exception as e:
            logger.error("An error occurred:", e)
            return {"result": False, "message": "An error occurred: " + str(e)}
    
    def insert_many_data(self, data):
        self.collection.insert_many(data)

    def insert_data(self, data):
        return self.collection.insert_one(data)
    
    def get_data(self, search_params=None, sort_by=None, limit=None):
        # Build the query based on the provided options
        query = {}
        if search_params:
            query.update(search_params)

        # Perform sorting if sort_by is provided
        if sort_by:
            sort_field, sort_order = sort_by
            results = self.collection.find(query).sort(sort_field, sort_order)
        else:
            results = self.collection.find(query)

        # Limit the number of results if limit is provided
        if limit:
            results = results.limit(limit)
            
        return list(results)
    
        # Example usage
        # query_params = {
        #     "key1": "value1",
        #     "key2": "value2",
        #     # Add more keys and values as needed
        # }

        # sort_option = ("field_to_sort", pymongo.ASCENDING)  # or pymongo.DESCENDING
        # limit_option = 10

        # # Call the function with the desired options
        # query_mongodb("your_collection_name", search_params=query_params, sort_by=sort_option, limit=limit_option)
    
    def update_document(self, query, update_data):
        # Update the document that matches the query with the provided update data
        result = self.collection.update_one(query, {"$set": update_data})

        return result
    
        # # Example usage
        # query = {"key1": "value1"}  # Specify the query to find the document to update
        # update_data = {"$set": {"key2": "updated_value2"}}  # Specify the update data

        # # Call the function to update the document
        # update_result = update_document("your_collection_name", query, update_data)

        # if update_result.modified_count > 0:
        #     print("Document updated successfully.")
        # else:
        #     print("No document was updated.")