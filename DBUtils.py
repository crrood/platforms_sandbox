"""
Utilities for working with stored data on accountHolders
"""
import os, json

  #####################
 ## GENERAL METHODS ##
#####################
class DBUtils():
    """
    General interface for interacting with data stored on disk

    Models should be extended from this class with the model name as the class name
    """
    @classmethod
    def list(cls):
        """
        Return list of all entity ID's stored locally
        """
        return os.listdir(f"db/{cls.__name__}")

    @classmethod
    def read(cls, entity_id):
        """
        Return dict from json file for given entity ID
        """
        try:
            with open(f"db/{cls.__name__}/{entity_id}", "r") as json_file:
                return json.loads(json_file.read())
        except FileNotFoundError:
            return f"invalid {cls.__name__} id"

    @classmethod
    def read_all(cls):
        """
        Return an array of dicts with all stored data for given entity
        """
        results = []
        for entity_id in cls.list():
            results.append(cls.read(entity_id))
        return results

    @classmethod
    def write(cls, entity_id, entity_data):
        """
        Writes entity data to disk
        """
        with open(f"db/{cls.__name__}/{entity_id}") as json_file:
            json_file.write(entity_data)
        return True

  #####################
 ## ACCOUNT HOLDERS ##
#####################
class AccountHolders(DBUtils):
    """
    Class named after AccountHolders model
    """

  ##############
 ## ACCOUNTS ##
##############
class Accounts(DBUtils):
    """
    Class named after Accounts model
    """
