from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values


def test_connection(db_client):
    """
    Test the connection to the MongoDB database.

    Args:
        db_client: A MongoClient instance to test the connection.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """
    try:
        db_client.admin.command("ping")
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
    config = dotenv_values(".env")
    uri = f"mongodb+srv://{config['MDB_USER']}:{config['MDB_PASSWORD']}@mdscswh3.vppmp7a.mongodb.net/?retryWrites=true&w=majority&appName=mdscswh3:"
    client = MongoClient(uri, server_api=ServerApi("1"))
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
    return db.cats.insert_one({"name": name, "age": age, "features": features})


def read(db, name=None):
    """
    Reads all cat records from the database and returns them as a list.

    Args:
        db: The database object.
        name (str, optional): The name of the cat. Defaults to None.

    Returns:
        list: A list of cat records.
    """

    param = {"name": name} if name else {}
    return list(db.cats.find(param))


def update(db, name, age=None, features=None):
    """
    Updates a cat record in the database based on the provided name with new age and/or features.

    Args:
        db (pymongo.MongoClient): The MongoDB client object.
        name (str): The name of the cat.
        age (int, optional): The new age of the cat. Defaults to None.
        features (list, optional): The new list of features of the cat. Defaults to None.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.
            If `features` is None and `age` is not None, the result will be the result of updating the `age` field.
            If `features` is not None, the result will be the result of updating the `features` field and possibly the `age` field.
            If both `features` and `age` are None, None will be returned.
    """

    if features is None and age is not None:
        return db.cats.update_one({"name": name}, {"$set": {"age": age}})
    if features is not None:
        old_features = db.cats.find_one({"name": name})["features"]
        set_params = {"features": old_features + features}
        if age is not None:
            set_params["age"] = age
        return db.cats.update_one({"name": name}, {"$set": set_params})
    return None


def delete(db, name=None):
    """
    Deletes a cat record from the database.

    Args:
        db (pymongo.MongoClient): The MongoDB client object.
        name (str, optional): The name of the cat to be deleted. If not provided, all cat records will be deleted.

    Returns:
        pymongo.results.DeleteResult: The result of the deletion operation. If `name` is provided, the result will be the result of deleting a single cat record by its name. If `name` is not provided, the result will be the result of deleting all cat records.
    """
    """
    Deletes a cat record from the database.

    Args:
        db (pymongo.MongoClient): The MongoDB client object.
        name (str, optional): The name of the cat to be deleted. If not provided, all cat records will be deleted.

    Returns:
        pymongo.results.DeleteResult: The result of the deletion operation. If `name` is provided, the result will be the result of deleting a single cat record by its name. If `name` is not provided, the result will be the result of deleting all cat records.
    """

    if name:
        return db.cats.delete_one({"name": name})
    return db.cats.delete_many({})


def print_all_cats(cats):
    """
    Prints all cat records in the database.

    Args:
        cats: A list of cat records.
    """
    print("Cat info:")
    for cat in cats:
        print(f"{cat['_id']}: {cat['name']}, {cat['age']}, {cat['features']}")


if __name__ == "__main__":
    db = connect()
    print("Adding records to DB...")
    add(db, "Simba", 5, ["white", "cute"])
    print(f"Added cat 'Simba'")
    add(db, "Mint", 3, ["black", "lazy"])
    print(f"Added cat 'Mint'")
    add(db, "Leon", 1, ["red", "fluffy"])
    print(f"Added cat 'Leon'")
    print("Reading DB...")
    cats = read(db)
    print_all_cats(cats)
    cat = read(db, "Simba")
    print_all_cats(cat)
    print("Updating DB...")
    update(db, "Simba", age=4)
    cats = read(db, "Simba")
    print_all_cats(cats)
    update(db, "Simba", features=["kind"])
    cats = read(db, "Simba")
    print_all_cats(cats)
    update(db, "Simba", age=3, features=["fluffy"])
    cats = read(db, "Simba")
    print_all_cats(cats)
    print("Deleting records from DB...")
    number = delete(db, "Simba")
    cats = read(db)
    print_all_cats(cats)
    number = delete(db)
    cats = read(db)
    print_all_cats(cats)
