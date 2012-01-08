#!/usr/bin/env python

# XXX should reimplement this proxy in erlang!!

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def handle_one_request(self):
        print "HIHIHIIH"
        pass

PORT = 8959

server = HTTPServer(("localhost", PORT), Handler)
server.serve_forever()
