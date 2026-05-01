from flask import Flask, request, jsonify, render_template
import json
import requests
import datetime

app = Flask(__name__)

FILE = "main.json"

# Functions
def read():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save(site):
    with open(FILE, "w") as f:
         json.dump(site, f, indent=2)

@app.route('/docs')
def docs():
    return("Empty rn")

@app.route('/add', methods=["POST"])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no JSON sent"}), 400
    name = data.get("name").lower()
    url = data.get("url")
    desc = data.get("desc", "Nothing")

    info = read()

    if not name or not url:
        return jsonify({"error": "missing fields"}), 400
    
    for site in info.values():
        if site["url"] == url:
            return jsonify({"error": "url already exists"}), 400
    
    if name in info:
        return jsonify({
            "error": "already exists"
        }), 400

    info[name] = {
        "url": url,
        "desc": desc
    }

    save(info)

    return jsonify({
        "message": "added",
        "name": name
    })

@app.route('/get', methods=["GET"])
def get():
    sites = read()
    return jsonify(sites)

@app.route('/get/<name>', methods=["GET"])
def get_name(name):
    name = name.lower()
    info = read()
    if name not in info:
        return jsonify({"error": "name not found"}), 400
    
    return(info[name])

@app.route('/report/<name>', methods=["GET"])
def report(name):

    if not name:
        return jsonify({"error": "no name"}), 400
    ct = datetime.datetime.now().isoformat()
    info = {
        "name": name,
        "time": ct
    }

    requests.post(
        "https://crisapis.vercel.app/api/reportSiteV1",
        json=info
    )
    return jsonify({"message": "reported"})

if __name__ == "__main__":
    app.run(debug=True)