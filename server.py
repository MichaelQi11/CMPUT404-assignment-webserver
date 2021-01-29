#  coding: utf-8 
import socketserver
import os
from pathlib import Path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, 2021 Hongru Qi
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # The method to get request url and response strucure are got from 成西风, https://blog.csdn.net/weixin_29609679
        # From CSDN
        # https://blog.csdn.net/weixin_29609679/article/details/112713885

        # Get request url
        splited = self.data.splitlines()
        request_url = splited[0].decode("utf-8")
        host = "http://127.0.0.1:8080"
        # Get request method
        method = request_url.split()[0]
        if (method != "GET"):
            response_code = "HTTP/1.1 405 Method Not Allowed\n"
            response_header = "Content-Type: text/plain" + "\n"
            response_body = "{} Method Not Allowed\n".format(method)
        
        else:
            root = os.path.abspath("www")
            filename = request_url.split()[1]
            # Set default html
            if (filename.endswith("/")):
                filename += "index.html"
            filepath = os.path.abspath("www" + filename)
            if ("." in filename):
                filetype = filename.split(".")[1]
            else:
                filetype = "plain"
            # Check if under /www
            if (root not in filepath):
                response_code = "HTTP/1.1 404 Not Found\n"
                response_header = "Content-Type: text/" + filetype + "\n"
                response_body = "The file is not found!"
            else:
                # The response structure and open file are got from 成西风, https://blog.csdn.net/weixin_29609679
                # From CSDN
                # https://blog.csdn.net/weixin_29609679/article/details/112713885
                if (os.path.isdir("www" + filename)):
                    filename += "/"
                    response_code = "HTTP/1.1 301 Moved Permanently\n"
                    # response_header = "Content-Type: text/" + filetype + "\n"
                    response_header = "Location: {0}{1}\n".format(host, filename)
                    response_body = "The URL has changed to {}\n".format(filename)
                else:
                    try:
                        file = open("www" + filename, "r")
                    except FileNotFoundError:
                        response_code = "HTTP/1.1 404 Not Found\n"
                        response_header = "Content-Type: text/" + filetype + "\n"
                        response_body = "The file is not found!"
                    else:
                        file_data = file.read()
                        file.close()
                        response_code = "HTTP/1.1 200 OK FOUND!\n"
                        response_header = "Content-Type: text/" + filetype + "\n"
                        response_body = file_data

        self.request.sendall(bytearray(response_code + response_header + "\n" + response_body, 'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
