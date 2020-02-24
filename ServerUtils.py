#!/usr/local/adyen/python/bin/python3
"""
utilities for sending / receiving requests

includes logging, authentication, and response formatting
"""

import logging

# network methods
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# authentication
import configparser

# constants
ACCEPT_HEADER = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"

class ServerUtils():
    """
    class to be imported by flask app to help send requests
    """

    ########################
    #      CONSTRUCTOR     #
    ########################

    def __init__(self,
                 logger_prefix="ServerUtils",
                 config_file="config.ini"):
        self.logger = ServerUtils.get_custom_logger(logger_prefix)
        self.config = self.load_config(config_file)

    ####################
    #      LOGGING     #
    ####################
    @staticmethod
    def get_custom_logger(logger_prefix):
        """
        logger with date, time, and custom prefix
        """
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(name)s:%(levelname)s %(message)s',
            datefmt='[%d/%m/%Y %X %Z]')

        return logging.getLogger(logger_prefix)

    ############################
    #      NETWORK METHODS     #
    ############################
    """
    class methods for sending requests and responding to client
    """

    def send_request(self,
                     url,
                     request_dict):
        """
        send request to server and return dict or string response
        """
        # logging
        self.logger.info("")
        self.logger.info("sending outgoing request to %s", url)
        self.logger.info("request data: %s", request_dict)

        # add merchant account if the request contains a blank value for it
        if "merchantAccount" in request_dict.keys():
            if len(request_dict["merchantAccount"]) == 0:
                request_dict["merchantAccount"] = self.config["merchant_account"]

        # add accept header if browserInfo is present
        if "browserInfo" in request_dict.keys():
            request_dict["browserInfo"]["acceptHeader"] = ACCEPT_HEADER

        # encode data
        encoded_data = json.dumps(request_dict).encode("utf8")

        # create request object
        # TODO detect whether a request is a payment or platform operation
        request = Request(url, encoded_data, self.get_json_header())

        try:
            # make request to server
            response = urlopen(request)
            result = response.read()

            self.logger.info("response data: %s", result)

            # format and return response
            if "application/json" in response.getheader("content-type"):
                result = json.loads(result.decode("utf8"))
            elif isinstance(result, bytes):
                result = result.decode("utf8")
        except HTTPError as e:
            self.logger.warning("HTTPError")
            result = "{}".format(e)

        client_response = {}
        client_response["request"] = request_dict
        client_response["response"] = result
        client_response["endpoint"] = url

        return client_response

    ############################
    #      CONFIGURATION       #
    ############################
    @staticmethod
    def load_config(config_file):
        """
        load credentials from config.ini

        see example_config.ini for file format
        """
        parser = configparser.ConfigParser()
        parser.read(config_file)
        credentials = parser["config"]

        loaded_config = {}

        loaded_config["merchant_account"] = credentials["merchantAccount"]
        loaded_config["ws_api_key"] = credentials["webserviceApiKey"]
        loaded_config["marketplace_api_key"] = credentials["webserviceApiKey"]

        return loaded_config

    ####################
    #      HEADERS     #
    ####################
    def get_json_header(self, marketplace=False):
        """
        return a generic header for json content
        including API key
        """
        if marketplace:
            api_key = self.config["marketplace_api_key"]
        else:
            api_key = self.config["ws_api_key"]

        return {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }
