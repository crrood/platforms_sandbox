# utilities
import json

# Flask
from flask import Flask, render_template, send_from_directory, request

# utilities for working with persistent data
from DBUtils import AccountHolders, Accounts

# utilities for sending requests
from ServerUtils import ServerUtils
server_utils = ServerUtils("Flask")

# flask app
app = Flask(__name__)

# app routes
@app.route("/")
def index():
    """
    Main page
    """
    server_utils.logger.info("receiving request to /")
    return render_template(
        "template.html",
        accountHoldersList=AccountHolders.read_all(),
        accountsList=Accounts.read_all())

@app.route("/forwardRequest", methods=["POST"])
def forward_request():
    """
    Forward a POST request from the client to the URL specified
    """
    json_data = request.read_json(force=True)

    # extract url from request data
    url = json_data["endpoint"]
    del json_data["endpoint"]
    server_utils.logger.info("forwarding request to %s", url)

    result = server_utils.send_request(url, json_data)
    return result

@app.route("/refresh")
def refresh():
    """
    Query updated data on all stored entities
    """
    # query Adyen for current data on all stored AccountHolders
    account_holders_data = []
    account_data = {}
    for account_holder_code in AccountHolders.list():
        result = server_utils.send_request(
            ServerUtils.URLS["get_account_holder"],
            {"accountHolderCode": account_holder_code})
        data = result["response"]

        # save account data to be used when refreshing account info
        for account in data["accounts"]:
            account_data[account["accountCode"]] = account

        # update stored data and create a list to return to client
        AccountHolders.write(data["accountHolderCode"], json.dumps(data))
        account_holders_data.append(data)

    # query Adyen for current data on all stored Accounts
    #
    # note that there is not a single API call to get all information
    # so you need to join the /getAccountHolder response with
    # the /accountHolderBalance response
    for account_holder_code in AccountHolders.list():
        result = server_utils.send_request(
            ServerUtils.URLS["account_holder_balance"],
            {"accountHolderCode": account_holder_code})

        # add balances to existing account data
        for account in result["response"]["balancePerAccount"]:
            account_data[account["accountCode"]].update(account)

            # write to disk
            Accounts.write(account["accountCode"], json.dumps(account_data[account["accountCode"]]))

    return {
        "AccountHolders": account_holders_data,
        "Accounts": account_data
    }

@app.route("/js/<path:path>")
def serve_js(path):
    """
    Serve static js files
    """
    return send_from_directory("js", path)

@app.route("/css/<path:path>")
def serve_css(path):
    """
    Serve static css files
    """
    return send_from_directory("css", path)

if __name__ == '__main__':
    app.run(debug=True)
