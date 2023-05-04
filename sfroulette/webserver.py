import os
import http.server
import random
import socketserver

from neighborhood_scraper import \
    get_neighborhoods_from_url, \
    DEFAULT_NEIGHBORHOOD_URL

from http import HTTPStatus


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        neighborhoods = get_neighborhoods_from_url(DEFAULT_NEIGHBORHOOD_URL)
        answer = random.choice(neighborhoods)
        msg = f"<h1>SF Roulette says to go here:</h1><h1>{answer}</h1>"
        self.wfile.write(msg.encode())


port = int(os.getenv("PORT", 80))
print("Listening on port %s" % (port))
httpd = socketserver.TCPServer(("", port), Handler)
try:
    httpd.serve_forever()
except KeyboardInterrupt as e:
    print("Done listening")
    pass
