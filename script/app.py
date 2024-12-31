from flask import Flask, request, jsonify
from main import extract_gdrive_url
import asyncio

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return jsonify({"message": "API for ktu notes automation"})


@app.route("/get-notes-url", methods=["GET"])
def extract_url():
    sem = request.args.get("sem")
    sub_name = request.args.get("sub_name")
    dept = request.args.get("dept")
    
    gdrive_urls = asyncio.run(extract_gdrive_url(sub_name, sem, dept))
    return jsonify({"gdrive_urls": gdrive_urls})


if __name__ == "__main__":
    app.run()
