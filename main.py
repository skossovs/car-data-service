## sources: https://anvileight.com/blog/posts/simple-python-http-server/
## COMMANDS
## Run Locally
##   python main.py
## Create package
##   docker build -t car-data .
## Run container and map to localhost
##   docker run -p 127.0.0.1:9000:9000 car-data-service
## http://localhost:9000/bmw/3-series/2021/2

# server.py
import http.server # Our http server handler for http requests
import socketserver # Establish the TCP Socket connections
from extractor import extractCarData
 
PORT = 9000
 
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        #parse input parameters
        paramLine = self.path
        parameters = paramLine.split("/")
        
        s = "N/A"
        if len(parameters) > 2:
            make = parameters[1]
            model = parameters[2]
            latestYear = parameters[3]
            nPagesStr = parameters[4]
            print ("Make:" + make)
            print ("Model:" + model)
            print ("Latest Year:" + latestYear)
            print ("Pages:" + nPagesStr)
            ## extract
            nPages = int(nPagesStr)
            s = extractCarData(make, model, nPages, latestYear)
            ### delme s = "{Make: " + make +", Model: " + model +"}"
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(s,"utf-8"))
 
Handler = MyHttpRequestHandler
 
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()