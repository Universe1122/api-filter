# https://portswigger.net/burp/extender#SampleExtensions

from burp import IBurpExtender
from burp import IHttpListener
from burp import IProxyListener
from burp import IScannerListener
from burp import IExtensionStateListener
from java.io import PrintWriter

import requests
import threading
from server.app import server_run
from packet.Packet import Packet

class BurpExtender(IBurpExtender, IHttpListener, IProxyListener, IScannerListener, IExtensionStateListener):
    def	registerExtenderCallbacks(self, callbacks):
        # keep a reference to our callbacks object
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        
        # set our extension name
        callbacks.setExtensionName("API Filter")
        
        # obtain our output stream
        self._stdout = PrintWriter(callbacks.getStdout(), True)

        # register ourselves as an HTTP listener
        callbacks.registerHttpListener(self)
        
        # register ourselves as a Proxy listener
        callbacks.registerProxyListener(self)
        
        # register ourselves as a Scanner listener
        callbacks.registerScannerListener(self)
        
        # register ourselves as an extension state listener
        callbacks.registerExtensionStateListener(self)
    
    # implement IProxyListener
    def processProxyMessage(self, messageIsRequest, message):
        if(messageIsRequest == False):
            packet = Packet(self._helpers, message.getMessageInfo())
            print(packet.response.toString())
            print("\n")

            # request = Request(self._helpers.analyzeRequest(message.getMessageInfo().getRequest()), message.getMessageInfo().getHttpService())
            # response_info = self._helpers.analyzeResponse(message.getMessageInfo().getResponse())
            
    
    # implement IProxyListener
    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        pass

t = threading.Thread(target=server_run)
t.start()