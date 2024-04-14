from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
from bson.objectid import ObjectId


def test_connection(db_client):
    """
    Test the connection to the MongoDB database.

    Args:
        db_client: A MongoClient instance to test the connection.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        db_client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print("Could not connect to MongoDB!")
        print(e)
        return False
    return True

def connect():
    """
    Connects to a MongoDB database using the provided credentials in the .env file.
    Returns a MongoClient instance connected to the specified database.
    """
    config = dotenv_values('.env')
    uri = f"mongodb+srv://{config['MDB_USER']}:{config['MDB_PASSWORD']}@mdscswh3.vppmp7a.mongodb.net/?retryWrites=true&w=majority&appName=mdscswh3:"
    client = MongoClient(uri, server_api=ServerApi('1'))
    test_connection(client)

    return client.mdscswh3

def add(db, name, age, features):
    """
    Adds a new cat record to the database.

    Args:
        db: The database object.
        name (str): The name of the cat.
        age (int): The age of the cat.
        features (list): List of features of the cat.

    Returns:
        The result of the insertion operation.
    """
    return db.cats.insert_one({'name': name, 'age': age, 'features': features})

def read(db):
    """
    Reads all cat records from the database and returns them as a list.

    Args:
        db: The database object.

    Returns:
        list: A list of cat records.
    """
    return list(db.cats.find({}))

def update(db, id, name, age, features):
    """
    Updates a cat record in the database based on the provided ID with new name, age, and features.

    Args:
        db: The database object.
        id: The ID of the cat record to be updated.
        name (str): The new name of the cat.
        age (int): The new age of the cat.
        features (list): The new list of features of the cat.

    Returns:
        The result of the update operation.
    """
    return db.cats.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'age': age, 'features': features}})

def delete(db, id):
    """
    Deletes a cat record from the database by its id.

    Args:
        db: The database object.
        id: The id of the cat to be deleted.

    Returns:
        The result of the deletion operation.
    """
    return db.cats.delete_one({'_id': ObjectId(id)})

def print_all_cats(cats):
    """
    Prints all cat records in the database.

    Args:
        cats: A list of cat records.
    """
    print("All cats:")
    for cat in cats:
        print(f"{cat['_id']}: {cat['name']}, {cat['age']}, {cat['features']}")

if __name__ == '__main__':
    db = connect()
    simba_id = add(db, 'Simba', 5, ['white', 'kind', 'cute']).inserted_id
    print(f"Added cat: {simba_id}")
    mint_id = add(db, 'Mint', 3, ['black', 'lazy']).inserted_id
    print(f"Added cat: {mint_id}")
    cats = read(db)
    print_all_cats(cats)
    number = update(db, mint_id, 'Mint', 4, ['black', 'lazy']).modified_count
    print(f"Updated cats: {number}")
    cats = read(db)
    print_all_cats(cats)
    number = delete(db, simba_id).deleted_count
    print(f"Deleted cats: {number}")
    cats = read(db)
    print_all_cats(cats)
