

# Lib imports:
from typing import Optional
import requests
requests.packages.urllib3.disable_warnings()
import json
# My lib imports:
from common import COMMON_ERROR_MESSAGES, buildUrl
from connection import Connection


class ApiData(object):
    def __init__(self, name:str, rawData:dict[str, object]) -> None:
        self.name : str = name
        self.maxVersion : int = rawData['maxVersion']
        self.minVersion : int = rawData['minVersion']
        self.path : str = rawData['path']
        self.requestFormat : Optional[str]
        if ('requestFormat' in rawData.keys()):
            self.requestFormat = rawData['requestFormat']
        else:
            self.requestFormat = None
        return


class ApiInfo(object):
    def __init__(self, connection: Connection) -> None:
    # Set url to grab all API endpoints:
        # self._url = connection.baseUrl + 'query.cgi?api=SYNO.API.Info&version=1&method=query&query=ALL'
        self._url = buildUrl(connection.baseUrl, "query.cgi", "SYNO.API.Info", 1, "query")
        self._url = self._url + "&query=ALL"
    # Get api list, or raise error:
        try:
            response = requests.get(url=self._url, verify=connection.verify)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            errorMessage = "HTTP error: '%s'" % (str(e.args))
            raise RuntimeError(errorMessage)
        except requests.ConnectionError as e:
            errorMessage = "Connection error: %s" % (str(e.args))
            raise RuntimeError(errorMessage)
        except requests.ConnectTimeout as e:
            errorMessage = "Timeout error: %s" % (str(e.args))
            raise RuntimeError(errorMessage)
        except requests.exceptions.SSLError as e:
            errorMessage = "SSL Certificate error: %s" % (str(e.args))
            raise RuntimeError(errorMessage)
    # Parse json response:
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            errorMessage = "Malformed response: %s" % (str(e.args))
            raise RuntimeError(errorMessage)
    # Check data for error from webApi:
        if (data['success'] == False):
            statusCode : int = data['error']
            statusMessage : str = COMMON_ERROR_MESSAGES[statusCode]
            errorMessage = "API: 'SYNO.API.Info' returned error. Code: '%i'. Message: '%s'." % (statusCode, statusMessage)
            raise RuntimeError(errorMessage)
    # Build API Data dict, and name list:
        apiDict : dict[str, dict[str, object]] = data['data']
        self.nameList : list[str] = list(apiDict.keys())
        self.apiData : dict[str, ApiData]= {}
        for apiName in self.nameList:
            self.apiData[apiName] = ApiData(name=apiName, rawData=apiDict[apiName])
        return

    def search(self, value:str, caseSensitive:bool=True) -> list[ApiData]:
        results : list[ApiData] = []
        for name in self.nameList:
            searchString : str = value
            nameString : str = name
            if (caseSensitive == False):
                searchString = searchString.lower()
                nameString = nameString.lower()
            if (nameString.find(searchString) > -1):
                results.append(self.apiData[name])
        return results

if __name__ == '__main__':
    connection = Connection("192.168.1.51", 5001, True, False)
    apiInfo = ApiInfo(connection)
    results : list[ApiData] = apiInfo.search('download', caseSensitive=False)
    for result in results:
        print(result.name, ' -> ', result.path)

    pass
