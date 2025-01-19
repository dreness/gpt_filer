# GPT Filer

Proof-of-concept to ease the process of getting code results from ChatGPT onto your filesystem.

## Overview

* Your prompt should include instructions to return code fragments as an array of JSON objects in the following form:

    ```json
    {
    "id": 123,
    "path": "/full/path/to/file.py",
    "code": "def my_function():\n    pass\n"
    }
    ```

* We'll use a browser extension to find these json fragments and send them to a service worker.

* The service worker will POST the JSON to a local server, which will write the code to the specified path(s).

Here's a [short demo](https://youtu.be/ivJNyp4Qrf0)

### Setup

#### Python

Flask is the only non-standard library required. Install it with:

```bash
pip install Flask
```

#### Browser Extension

1. Open `chrome://extensions/` in Chrome.
2. Enable Developer Mode.
3. Click "Load unpacked" and select the `browser-extension` directory.
4. Pin this extension to your browser toolbar.

### Run

1. Start the server:

    ```bash
    python server/server.py
    ```

2. Load ChatGPT and make a query that returns code fragments. Your prompt should include instructions to return code fragments as an array of JSON objects in the form shown above, something like:

    > Executable code should be represented in a JSON document containing an array of dictionaries. Each dict has the keys: id, path, code, where ID is a unique identifier like an integer used to refer to a given code chunk; path is the full path to the file; and code is the executable code that will be copied into the file at the given path.

3. When the response is finished, click the extension icon in your browser toolbar to send the code fragments to the local server.

If it worked, the "proj" directory should have stuff in it, and the server console should show something like:

```text
Data written to data/20250118170542_code_files.json
Creating files from data/20250118170542_code_files.json
Changed to root directory: /Users/andre/work/gpt_filer/proj
Loaded 6 entries
Created file: run.py
Created file: app/__init__.py
Created file: app/routes.py
Created file: app/templates/index.html
Created file: app/static/style.css
Created file: requirements.txt
127.0.0.1 - - [18/Jan/2025 17:05:42] "POST /create_files HTTP/1.1" 200 -
```

### Tests

```bash
python -m unittest discover tests
```