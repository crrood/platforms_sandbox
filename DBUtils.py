"""
Utilities for working with stored data on accountHolders
"""
import os, json

def get_all_account_holders():
    """
    Return an array of dicts with all stored accountHolder data
    """
    results = []
    for account_holder_code in get_account_holders_list():
        results.append(read_account_holder(account_holder_code))

    return results

def read_account_holder(account_holder_code):
    """
    Return dict from json file for given accountHolder code
    """
    try:
        with open(f"db/{account_holder_code}", "r") as json_file:
            return json.loads(json_file.read())
    except FileNotFoundError:
        return "invalid accountHolder code"

def get_account_holders_list():
    """
    Return list of all accountHolder codes stored locally
    """
    return os.listdir("db")
