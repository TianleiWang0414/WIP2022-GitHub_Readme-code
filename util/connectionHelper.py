import pycurl

from io import BytesIO
import certifi


class connector:
    """
    constructor takes url, your token and your gitHub username
    """

    def __init__(self, url: str, token: str, name: str):
        self.url = url
        self.token = token
        self.tokenHolder = name
        self.response_code = -1
        self.headerResponse=""

    """
    returns the url response in bytes
    """
    def getResponse(self):
        response = None
        buffer = BytesIO()
        header_buffer=BytesIO()
        ##Some curl stuff you don't need to worry about
        c = pycurl.Curl()
        c.setopt(pycurl.URL, self.url)
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(pycurl.USERPWD, '%s:%s' % (self.tokenHolder, self.token))
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.HEADERFUNCTION, header_buffer.write)
        c.perform()
        ## just in case we want to check response code
        response_code = c.getinfo(c.RESPONSE_CODE)
        self.response_code = response_code
        c.close()
        if response_code == 200 or response_code == 301:  ##if we get any response
            response = buffer.getvalue()
            self.headerResponse=header_buffer.getvalue()
        return response
