# GPT Filer

Ease the process of getting code results from ChatGPT onto your filesystem.

### Overview

* Our prompt will include instructions to return code fragments as JSON objects, in the following form:

    ```json
    {
    "id": 123,
    "path": "/full/path/to/file.py",
    "code": "def my_function():\n    pass\n"
    }
    ```

* We'll have a browser extension to find these json fragments and send them to a service worker.

The service worker will POST the JSON to a local server, which will write the code to the specified path.


### Run

```bash
python scripts/create_files.py data/code_files.json
```

### Tests

```bash
python -m unittest discover tests
```