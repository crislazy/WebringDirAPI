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

# ------------------------------------

# Main pages
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/docs')
def docs():
    return render_template("docs.html")

@app.route('/web')
def web():
    return render_template("web.html")

@app.route('/rules')
def rules():
    return render_template("rules.html")

# ------------------------------------

# API

@app.route('/add', methods=["POST"])
def add():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no JSON sent"}), 400
    name = data.get("name")
    url = data.get("url")
    desc = data.get("desc", "empty")

    db = read()

    if not name or not url:
        return jsonify({"error": "missing fields"}), 400
    
    name = name.lower()
    
    for site in db.values():
        if site["url"] == url:
            return jsonify({"error": "url already exists"}), 400
    
    if name in db:
        return jsonify({"error": "name already exists"}), 400

    db[name] = {
        "url": url,
        "desc": desc
    }

    save(db)

    return jsonify({
        "message": "added",
        "name": name
    })

@app.route('/get', methods=["GET"])
def get():
    db = read()
    return jsonify(db)

@app.route('/get/<name>', methods=["GET"])
def get_name(name):
    name = name.lower()
    db = read()
    if not name in db:
        return jsonify({"error": "name not found"}), 400
    
    return jsonify(db[name])

@app.route('/report/<name>', methods=["GET"])
def report(name):
    db = read()
    if not name in db:
        return jsonify({"error": "name not found"}), 400
    else:
        ct = datetime.datetime.now().isoformat()
        info = {
            "name": name,
            "time": ct
        }
        try:
            requests.post(
                "https://crisapis.vercel.app/api/reportSiteV1",
                json=info,
                timeout=3
            )
            return jsonify({"message": "reported"})
        except:
            return jsonify({"error": "report failed"}), 500

# ------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)