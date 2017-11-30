#!/usr/bin/python

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
import wget


class DownloaderHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.getheader('content-length'), 0)
        post_body = self.rfile.read(content_length)
        testdata = json.loads(post_body)
        urls_to_download = testdata["urls"]
        for item in urls_to_download:
            # get the correct url for wget
            url = str(item).split("?apikey=")[0]
            wget.download(url)
        print("the list length is %d" % len(urls_to_download))


def main():
    try:
        PORT = 8000
        httpd = HTTPServer(("", PORT), DownloaderHandler)
        print("Serving at port %s " % PORT)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('shut down http server')
        httpd.socket.close()


if __name__ == "__main__":
    main()
