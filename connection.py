
import socket

class Connection(object):
    def __init__(self,
                    address:str,    # Hostname / ip of server.
                    port: int,      # Port of server.
                    useSSL: bool,   # Use SSL 
                    verify: bool=True, # Verify SSL Certificate, set to false for self-signed certificates.
                ) -> None:
        self._address : str = address
        self._port : int = port
        self.baseUrl : str  # Base url for requests.
        if (useSSL == True):
            self.baseUrl = "https://%s:%i/webapi/" % (address, port)
        else:
            self.baseUrl = "http://%s:%i/webapi/" % (address, port)
        self.verify : bool = verify
        return

    def test(self) -> tuple[bool, int, str]:
    # Create socket:
        testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Try to connect:
        try:
            testSocket.connect((self._address, self._port))
            testSocket.close()
        except OSError as e:
            errorMessage = 'Connection error: %s' % (e.args[1])
            return (False, e.args[0], errorMessage)
        except ConnectionError as e:
            errorMessage = 'Connection error: %s' % (e.args[1])
            return (False, e.args[0], errorMessage)
        return (True, 0, 'No error')
