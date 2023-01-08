# Lib imports:
from typing import Optional
import requests
requests.packages.urllib3.disable_warnings()
import json

# My lib imports:
from common import COMMON_ERROR_MESSAGES, ERROR_CONNECTION_ERROR, ERROR_MALFORMED_JSON, ERROR_TIMEOUT_ERROR, ERROR_HTTP_ERROR, ERROR_SSL_ERROR, buildUrl
from connection import Connection
from apiInfo import ApiInfo, ApiData
# Auth api error codes taken from:
#   https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/DownloadStation/All/enu/Synology_Download_Station_Web_API.pdf


class Authentication(object):

    ERROR_MESSAGES = {
        400: 'No such account or incorrect password',   # Synology
        401: 'Account disabled',    # Synology
        402: 'Permission denied',   # Synology
        403: '2-step verification code required',   # Synology
        404: 'Failed to authenticate 2-step verification code', # Synology
    }

    def __init__(self, connection:Connection, apiInfo: ApiInfo, session: str, username:str, password:str) -> None:
        self._api = "SYNO.API.Auth"
        self._connection : Connection = connection
        self._apiData : ApiData = apiInfo.apiData[self._api]
        self.session : str = session
        self.username : str = username
        self.password : str = password
        self.sid : Optional[int] = None
        return

    def login(self) -> tuple[bool, int, str]:
    # Build URL:
        url = buildUrl(self._connection.baseUrl, self._apiData.path, self._api, self._apiData.maxVersion, 'login')
        url = url + '&account=%s' % (self.username)
        url = url + '&passwd=%s' % (self.password)
        url = url + '&session=%s' % (self.session)
        url = url + '&format=sid'
    # Get and parse response from NAS:
        try:
            response = requests.get(url=url, verify=self._connection.verify)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            errorMessage = "%s: '%s'" % (COMMON_ERROR_MESSAGES[ERROR_HTTP_ERROR], str(e.args))
            return (False, ERROR_HTTP_ERROR, errorMessage)
        except requests.ConnectionError as e:
            errorMessage = "%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_CONNECTION_ERROR], str(e.args))
            return (False, ERROR_CONNECTION_ERROR, errorMessage)
        except requests.ConnectTimeout as e:
            errorMessage = "%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_TIMEOUT_ERROR], str(e.args))
            return (False, ERROR_TIMEOUT_ERROR, errorMessage)
        except requests.exceptions.SSLError as e:
            errorMessage = "%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_SSL_ERROR], str(e.args))
            return (False, ERROR_SSL_ERROR, errorMessage)
            
    # Try to parse json response:
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            errorMessage ="%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_MALFORMED_JSON], str(e.args))
            return (False, ERROR_MALFORMED_JSON, errorMessage)

        if (data['success'] == True):
            self.sid = data['data']['sid']
            message : str = COMMON_ERROR_MESSAGES[0]
            return (True, 0, message)
        else:
            self.sid = None
            errorMessage : str
            if (data['error'] <= 150):
                errorMessage = COMMON_ERROR_MESSAGES[data['error']]
            elif (data['error'] >= 400):
                errorMessage = self.ERROR_MESSAGES[data['error']]
            else:
                errorMessage = COMMON_ERROR_MESSAGES[-1] # Undefined error.
            return (False, data['error'], errorMessage)

    def logout(self) -> tuple[bool, int, str]:
        # url = self._url + '/webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=DownloadStation'
        url = buildUrl(self._connection.baseUrl, self._apiData.path, self._api, self._apiData.maxVersion, 'logout')
        url = url + '&session=%s' % (self.session)
    # Get and parse response from NAS:
        try:
            response = requests.get(url=url, verify=self._connection.verify)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            errorMessage = "%s: '%s'" % (COMMON_ERROR_MESSAGES[ERROR_HTTP_ERROR], str(e.args))
            return (False, ERROR_HTTP_ERROR, errorMessage)
        except requests.ConnectionError as e:
            errorMessage = "%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_CONNECTION_ERROR], str(e.args))
            return (False, ERROR_CONNECTION_ERROR, errorMessage)
        except requests.ConnectTimeout as e:
            errorMessage = "%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_TIMEOUT_ERROR], str(e.args))
            return (False, ERROR_TIMEOUT_ERROR, errorMessage)
        except requests.exceptions.SSLError as e:
            errorMessage = "%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_SSL_ERROR], str(e.args))
            return (False, ERROR_SSL_ERROR, errorMessage)
            
    # Try to parse json response:
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            errorMessage ="%s: %s" % (COMMON_ERROR_MESSAGES[ERROR_MALFORMED_JSON], str(e.args))
            return (False, ERROR_MALFORMED_JSON, errorMessage)
    # Parse response from NAS
        if (data['success'] == True):
            self.sid = None
            return (True, 0, COMMON_ERROR_MESSAGES[0])
        else:
            errorMessage : str
            if (data['error'] <= 150):
                errorMessage = COMMON_ERROR_MESSAGES[data['error']]
            elif (data['error'] >= 400):
                errorMessage = self.ERROR_MESSAGES[data['error']]
            else:
                errorMessage = COMMON_ERROR_MESSAGES[-1] # Undefined error.
            return (False, data['error'], errorMessage)

    def isLoggedIn(self) -> bool:
        return (self.sid != None)


if __name__ == '__main__':
    connection = Connection("192.168.1.51", 5001, True, False)
    apiInfo = ApiInfo(connection)

    auth = Authentication(
                        connection=connection,
                        apiInfo=apiInfo,
                        session='DownloadStation',
                        username='streak',
                        password='<Change Me>'
                    )
    success, statusCode, statusMessage = auth.login()
    if (success == True):
        print("Logged in successfully.")
    else:
        print("Login failed:")
        print("    Code: '%i' Message: '%s'" % (statusCode, statusMessage) )

    success, statusCode, statusMessage = auth.logout()
    if (success == True):
        print("Logged out successfully")
    else:
        print("Logout failed:")
        print("    Code: '%i' Message: '%s'" % (statusCode, statusMessage))