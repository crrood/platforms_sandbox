# Flask
from flask import Flask, render_template, send_from_directory, request

# utilities for working with persistent data
import DBUtils

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
        accountHoldersList=DBUtils.get_all_account_holders(),
        accountsList=DBUtils.get_all_accounts())

@app.route("/forwardRequest", methods=["POST"])
def forward_request():
    """
    Forward a POST request from the client to the URL specified
    """
    json_data = request.get_json(force=True)

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
    account_holders_data = []
    for account_holder_code in DBUtils.get_account_holders_list():
        result = server_utils.send_request(
            ServerUtils.URLS["get_account_holder"],
            {"accountHolderCode": account_holder_code})
        account_holders_data.append(result["response"])
    server_utils.logger.info(account_holders_data)
    return account_holders_data

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
