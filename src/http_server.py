from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
import os

def start_file_server():
    directory = "/tmp"

    handler = partial(
        SimpleHTTPRequestHandler,
        directory=directory
    )

    server = ThreadingHTTPServer(("0.0.0.0", 8080), handler)

    Thread(target=server.serve_forever, daemon=True).start()

    print("File server running on port 8080")