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
        file_list = os.listdir(f"db/{cls.__name__}")
        if ".DS_Store" in file_list:
            file_list.remove(".DS_Store")
        return file_list

    @classmethod
    def read(cls, entity_id):
        """
        Return dict from json file for given entity ID
        """
        file_path = f"db/{cls.__name__}/{entity_id}"
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            return f"file does not exist or is empty: {file_path}"

        try:
            with open(file_path, "r") as json_file:
                data = json_file.read()
                return json.loads(data)
        except json.decoder.JSONDecodeError:
            return f"invalid JSON: {file_path}"

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
        with open(f"db/{cls.__name__}/{entity_id}", "w") as json_file:
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
    @classmethod
    def read_all(cls):
        """
        Accounts are always referenced in the context of an AccountHolder
        so it's easier to work with them as a dict than list
        """
        accounts_list = super().read_all()
        accounts_dict = {}
        for account in accounts_list:
            accounts_dict[account["accountCode"]] = account

        return accounts_dict
