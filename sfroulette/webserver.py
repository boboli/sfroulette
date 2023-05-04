import os
import http.server
import random
import socketserver

from neighborhood_scraper import \
    get_neighborhoods_from_url, \
    DEFAULT_NEIGHBORHOOD_URL

from http import HTTPStatus


CENTER_FLEXBOX_STYLE = \
    "display: flex; align-items: center; justify-content: center;" \
    "height: 100%; text-align: center; font-size: 10vw;" \
    "font-family: sans-serif;"

RELOAD_BUTTON = \
    "<a style='font-size:5vw;' href='#' " \
    "onclick='window.location.reload(true);'>" \
    "REROLL?</a>"


def big_html_banner(message):
    return "<html style='height: 100%;'>" \
        "<body style='height: 100%;'>" \
        f"<div style='{CENTER_FLEXBOX_STYLE}'>" \
        f"<p>{message}</p>" \
        "</div></body></html>"


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
            msg = big_html_banner(f"Something broke :(<br>{error}")
            self.wfile.write(msg.encode())
        else:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            msg = big_html_banner(
                f"SF Roulette:<br>{answer}<br>{RELOAD_BUTTON}")
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
