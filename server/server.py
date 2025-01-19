#!/usr/bin/env python3

from flask import Flask, request, jsonify
from create_files import create_files_from_json
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/create_files", methods=["POST"])
def create_files():
    """
    Endpoint that expects an array of JSON objects like:
    [
      {"id": 123, "path": "/tmp/test.py", "code": "..."},
      ...
    ]
    """

    try:
        entries = request.json
        # print(request.headers)
        # print(request.json)
        # print(request.data)
        if not isinstance(entries, list):
            return jsonify({"error": "Invalid data format. Must be a list."}), 400

        # ensure that each list entry is a dictionary with keys "id", "path", and "code"
        for entry in entries:
            if not isinstance(entry, dict):
                return jsonify({"error": "Invalid data format. List entries must be dictionaries."}), 400
            if not all(k in entry for k in ("id", "path", "code")):
                return jsonify(
                    {"error": "Invalid data format. List entries must have 'id', 'path', and 'code' keys."}), 400
        # write the data to a json file in the data directory.
        # Encode a time / date stamp in the filename.
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        fname = f"data/{ts}_code_files.json"
        with open(fname, 'w', encoding='utf-8') as f:
            json.dump(entries, f)
        print(f"Data written to {fname}")
        create_files_from_json(fname)
        return jsonify({"status": "Success", "files_created": len(entries)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run on localhost:5000 by default
    app.run(port=5000, debug=True)
