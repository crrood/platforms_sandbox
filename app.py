# utilities
import json, configparser
import requests

# Flask
from flask import Flask
from flask_cors import CORS
from werkzeug.datastructures import Headers

# utilities for sending requests
from ServerUtils import ServerUtils
utils = ServerUtils("Flask")

# load configuration
parser = configparser.ConfigParser()
parser.read("config.ini")
config = parser["config"]

# flask app
app = Flask(__name__)

# app routes
@app.route("/")
def index():
    """
    Main page
    """
    utils.logger.info("receiving request to /")
    return "Hello World!"

@app.route("/testRequest")
def test_request():
    """
    Send a test request to postman-echo
    to make sure everything is working with ServerUtils
    """
    utils.logger.info("sending test request")
    result = utils.send_request("https://postman-echo.com/post", {"foo": "bar"})
    utils.logger.info(result)
    return result

if __name__ == '__main__':
    app.run(debug=True)
