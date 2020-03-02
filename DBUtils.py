"""
Utilities for working with stored data on accountHolders
"""
import os, json

  #####################
 ## GENERAL METHODS ##
#####################
def get_entity(entity_type, entity_id):
    """
    Return dict from json file for given entity ID
    """
    try:
        with open(f"db/{entity_type}/{entity_id}", "r") as json_file:
            return json.loads(json_file.read())
    except FileNotFoundError:
        return f"invalid {entity_type} id"

def get_entity_list(entity_type):
    """
    Return list of all entity ID's stored locally
    """
    return os.listdir(f"db/{entity_type}")

def get_all_entities(entity_type):
    """
    Return an array of dicts with all stored data for given entity
    """
    results = []
    for entity_id in get_entity_list(entity_type):
        results.append(get_entity(entity_type, entity_id))
    return results

  #####################
 ## ACCOUNT HOLDERS ##
#####################
def get_account_holder(account_holder_id):
    """
    Return dict from json file for given accountHolder ID
    """
    return get_entity("AccountHolders", account_holder_id)

def get_account_holders_list():
    """
    Return list of all accountHolder IDs stored locally
    """
    return get_entity_list("AccountHolders")

def get_all_account_holders():
    """
    Return an array of dicts with all stored accountHolder data
    """
    return get_all_entities("AccountHolders")

  ##############
 ## ACCOUNTS ##
##############
def get_account(account_id):
    """
    Return dict from json file for given account ID
    """
    return get_entity("Accounts", account_id)

def get_accounts_list():
    """
    Return list of all account IDs stored locally
    """
    return get_entity_list("Accounts")

def get_all_accounts():
    """
    Return an array of dicts with all stored account data
    """
    return get_all_entities("Accounts")
