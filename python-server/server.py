#!/usr/bin/env python3

from flask import Flask, request, jsonify
from create_files import create_files_from_json

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
        entries = request.json  # Should be a list of code objects
        if not isinstance(entries, list):
            return jsonify({"error": "Invalid data format. Must be a list."}), 400

        create_files_from_json(entries)

        return jsonify({"status": "Success", "files_created": len(entries)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run on localhost:5000 by default
    app.run(port=5000, debug=True)
