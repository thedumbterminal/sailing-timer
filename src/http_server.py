from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from .temp_file import TempFile

import os

def start_file_server():
    directory = TempFile.get_temp_directory()

    handler = partial(
        SimpleHTTPRequestHandler,
        directory=directory
    )

    server = ThreadingHTTPServer(("0.0.0.0", 8080), handler)

    Thread(target=server.serve_forever, daemon=True).start()

    print("File server running on port 8080")