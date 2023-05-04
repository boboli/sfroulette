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
        try:
            neighborhoods = get_neighborhoods_from_url(
                DEFAULT_NEIGHBORHOOD_URL)
            answer = random.choice(neighborhoods)
        except Exception as error:
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            msg = f"<h1>Something broke :(</h1><p>{error}</p>"
            self.wfile.write(msg.encode())
        else:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            msg = f"<h1>SF Roulette says to go here:</h1><h1>{answer}</h1>"
            self.wfile.write(msg.encode())


if __name__ == "__main__":
    port = int(os.getenv("PORT", 80))
    print(f"Listening on port {port}")
    try:
        with socketserver.TCPServer(("", port), Handler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        print("Done listening")
        pass
