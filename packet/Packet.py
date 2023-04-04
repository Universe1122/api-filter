import unicodedata
from urlparse import urlparse, parse_qs

class Packet: 
    
    def __init__(self, helpers, IHttpRequestResponse):
        request_data = helpers.analyzeRequest(IHttpRequestResponse.getRequest())
        request_body = IHttpRequestResponse.getRequest()[request_data.getBodyOffset() : ]
        response_data = helpers.analyzeResponse(IHttpRequestResponse.getResponse())

        self.request = self.Request(request_data, IHttpRequestResponse.getHttpService(), request_body)

    class Request:
        def __init__(self, request_data, http_service, body):
            """
                Args:
                    request_data    (IRequestInfo): parsed value of callback.getHelpers().analyzeRequest()
                    http_service    (IHttpService): https://portswigger.net/burp/extender/api/burp/ihttpservice.html
                    body            (byte)
            """

            self.method = None
            self.protocol = None
            self.http_version = None
            self.headers = {}
            self.url = None
            self.port = None
            self.body = ""

            self._parse(request_data, http_service, body)


        def _parse(self, request_data, http_service, body):
            """
            _parse() function is parsed request_data and make to Object request.
                Args:
                    request_data (IRequestInfo): parsed value of callback.getHelpers().analyzeRequest()
                    http_service (IHttpService): https://portswigger.net/burp/extender/api/burp/ihttpservice.html
                    body         (byte)
                Retruns:
                    None
            """
            headers = request_data.getHeaders()

            first_header = headers[0].split(" ")
            self.method = first_header[0]
            self.url = urlparse(first_header[1])
            self.protocol = http_service.getProtocol()
            self.http_version = first_header[2]
            self.port = http_service.getPort()

            ############ Set Header #################
            if http_service.getHost() != "":
                if self.port == 80 or self.port == 443:
                    self.headers["Host"] = http_service.getHost()
                else:
                    self.headers["Host"] = "{0}:{1}".format(http_service.getHost(), self.port)

            for header in headers[1:]:
                header_info = header.split(": ")
                self.headers[header_info[0]] = header_info[1]
            ########################################


            ############## Set Body ###############
            try:
                body = body.tolist()
                for c in body:
                    self.body += chr(c)
            except Exception as e:
                print(e)
            #######################################


        def toString(self):
            """
            toString() function is return Object request to string.
                Args:
                    None
                Retruns:
                    None
            """
            return """{0} {1} {2}\n{3}\n\n{4}""".format(self.method, self.urlToString(), self.http_version, self.headerToString(), self.body)


        def urlToString(self):
            """
            urlToString() function is return url to string.
                Args:
                    None
                Retruns:
                    None
            """
            result = self.url.path

            if self.url.params != "":
                result += ";" + self.url.params
            if self.url.query != "":
                result += "?" + self.url.query
            if self.url.fragment != "":
                result += "#" + self.url.fragment
            
            return result
        

        def headerToString(self):
            """
            headerToString() function is return headers to string.
                Args:
                    None
                Retruns:
                    None
            """
            headers = list()

            for key in self.headers.keys():
                ## NOTICE, key and value type is unicode
                headers.append("{0}: {1}".format(key, self.headers[key]))
            
            return "\n".join(headers)

        #     ## TODO body parse

    class Response:
        def __init__(self, response_data):
            pass
