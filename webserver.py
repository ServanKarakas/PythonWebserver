import http.server
import socketserver
import sys
from flask_cors import CORS


# Corrected path with a comma
sys.path.insert(1, 'C:\\Users\\200183\\Documents\\Projektarbeit\\Workspace_test\\comm.py')

PORT = 8080
DIRECTORY = "./web"



class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

handler = Handler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    sys.stderr.write("Serving at port {}\n".format(PORT))    
#CORS(httpd)
    httpd.serve_forever()





