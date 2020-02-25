# Flask
from flask import Flask, render_template, send_from_directory, request

# utilities for sending requests
from ServerUtils import ServerUtils
utils = ServerUtils("Flask")

# flask app
app = Flask(__name__)

# app routes
@app.route("/")
def index():
    """
    Main page
    """
    utils.logger.info("receiving request to /")
    return render_template("template.html", accountHoldersList=[1,2])

@app.route("/forwardRequest", methods=["POST"])
def forward_request():
    """
    Forward a POST request from the client to the URL specified
    """
    json_data = request.get_json(force=True)

    # extract url from request data
    url = json_data["endpoint"]
    del json_data["endpoint"]
    utils.logger.info("forwarding request to %s", url)

    result = utils.send_request(url, json_data)
    return result

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
