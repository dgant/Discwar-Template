#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import simplejson
import sys
import player

#Based on DJudd's work from the Connect 4 tournament

ai = None

def get_move(data):
    global ai

    if ai is None:
        ai = player.Player()

    return ai.get_move(data)

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print 'METHOD: post'
        print
        content_length = self.headers['content-length']
        print 'CONTENT_LENGTH: ' + content_length
        print
        post_body = self.rfile.read(int(content_length))
        print 'POST_BODY: ' + post_body
        print
        input_json_dict = simplejson.loads(post_body)
        print 'INPUT_JSON: ' + str(input_json_dict)
        print
        move = get_move(input_json)
        print 'MOVE: ' + str(move)
        print
        output_json_string = '{"r":%f, "th":%f}' % move
        print 'OUTPUT_JSON: ' + output_json_string
        print

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.end_headers()
        self.wfile.write(output_json_string)

def serve(port):
    try:
        server = HTTPServer(('',port), MyHandler)
        print 'Starting server...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server...'
        server.socket.close()
    except Exception:
        #Lazy
        server.socket.close()
        serve(port)

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        print "Usage: server.py <port>"    
        exit(-1)
    serve(port)

