class Request:
    def __init__(self, request_data):
        self.method = ""
        self.protocol = ""
        self.headers = {}
        self.url = None             ## https://docs.oracle.com/javase/8/docs/api/java/net/URL.html
        self.body = ""
        self.parameter = None       ## https://portswigger.net/burp/extender/api/burp/iparameter.html

        self.parse(request_data)


    def parse(self, request_data):
        headers = request_data.getHeaders()

        self.url = request_data.getUrl()
        self.protocol = self.url.getProtocol()
        self.method = request_data.getMethod()
        self.parameter = request.getParamters()

        for header in headers[1:]:
            header_info = header.split(": ")
            self.haeders[header_info[0]] = header_info[1]


    def toString(self):
        headers = list()

        for key in self.headers.keys():
            print(key, self.headers[key])
            # headers.append(f"{key}: {self.headers[key]}")
        
        # headers = "\n".join(headers)

        # return f"{self.method} {self.url.toString()} {self.protocol}\n{headers}\n\n{self.body}"

        ## TODO body parse

class Response:
    def __init__(self, response_data):
        pass