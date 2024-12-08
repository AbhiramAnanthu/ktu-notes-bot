from flask import Flask, request, jsonify
from handle_automate import HandleAutomation

app = Flask(__name__)


@app.route("/api/data", methods=["POST"])
def gdrive_links():
    data = request.json
    auto = HandleAutomation()
    gdrive_url = auto.extract_urls(subject=data)

    return jsonify(gdrive_url)


if __name__ == "__main__":
    app.run(debug=True)
