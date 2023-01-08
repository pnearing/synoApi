from typing import Optional
import requests
requests.packages.urllib3.disable_warnings()
import socket
import json
from datetime import datetime

ERROR_MESSAGES : dict[int, str] = {
        000: 'No error',
          1: 'Connection error',
          2: 'Timeout error',
          3: 'Malformed JSON',
        100: 'Unknown error',
        101: 'Invalid parameter',
        102: 'The requested API does not exist',
        103: 'The requested method does not exist',
        104: 'The requested version does not support the functionality',
        105: 'The logged in session does not have permission',
        106: 'Session timeout',
        107: 'Session interrupted by duplicate login',
        400: 'File upload failed',
        401: 'Max number of tasks reached',
        402: 'Destination denied',
        403: 'Destination does not exist',
        404: 'Invalid task id',
        405: 'Invalid task action',
        406: 'No default destination',
        407: 'Set destination failed',
        408: 'File does not exist',
}


class Connection(object):
    def __init__(self,
                    address:str,
                    port: int,
                    useSSL: bool,
                ) -> None:
        self._address : str = address
        self._port : int = port
        self.baseUrl : str
        if (useSSL == True):
            self.baseUrl = "https://%s:%i/webapi/" % (address, port)
        else:
            self.baseUrl = "http://%s:%i/webapi/" % (address, port)
        return

    def test(self) -> tuple[bool, int, str]:
        testSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            testSocket.connect((self._address, self._port))
        except OSError as e:
            errorMessage = 'Connection error: %s' % (e.args[1])
            return (False, e.args[0], errorMessage)
        except ConnectionError as e:
            errorMessage = 'Connection error: %s' % (e.args[1])
            return (False, e.args[0], errorMessage)
        return (True, 0, 'No error')

class ApiInfo(object):
    def __init__(self, connection: Connection) -> None:
        self._url = connection.baseUrl + 'query.cgi?api=SYNO.API.Info&version=1&method=query&query=ALL'
        try:
            response = requests.get(url=self._url, verify=False)
        except requests.ConnectionError as e:
            errorMessage = "Connection error: %s" % (str(e.args))
            raise RuntimeError(errorMessage)
        except requests.ConnectTimeout as e:
            errorMessage = "Timeout error: %s" % (str(e.args))
            raise RuntimeError(errorMessage)
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            errorMessage = "Malformed response: %s" % (str(e.args))
            raise RuntimeError(errorMessage)
        print("DEBUG: ", json.dumps(data, indent=4))
        return



# class Authentication(object):
#     def __init__(self, username, password) -> None:
#         self._url = self.baseUrl + '/webapi/auth.cgi?api=SYNO.API.Auth&version=2'
#         self.username : str = username
#         self.password : str = password
#         self.sid : Optional[int] = None
#         self.apiInfo : dict[str, object]
#         try:
#             url = self.baseUrl + '/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=ALL'
#             response = requests.get(url=url, verify=False)
#             self.apiInfo = response.json()
#         except requests.ConnectionError as e:
#             errorMessage = "Failed to connect to DownloadStation: '%s' : %s" % (self.baseUrl, str(e.args))
#             raise RuntimeError(errorMessage)
#         except requests.ConnectTimeout as e:
#             errorMessage = "Failed to connect to DownloadStation: '%s' : Connection timed out."
#             raise RuntimeError(errorMessage)
#         except json.JSONDecodeError as e:
#             errorMessage = "DownloadStation responded with malformed JSON: '%s' : '%s'" % (e.msg, str(e.args))
#             raise RuntimeError(errorMessage)
#         print("DEBUG: ", json.dumps(self.apiInfo, indent=4))
#         return

#     def login(self) -> tuple[bool, int, str]:
#         url = self._url + '&method=login&'
#         url = url + 'account=%s' % self.username
#         url = url + '&passwd=%s' % self.password
#         url = url + '&session=DownloadStation&format=sid'
#         response = requests.get(url=url, verify=False)
#         data = response.json()
#         if (data['success'] == True):
#             self.sid = data['data']['sid']
#             message = ERROR_MESSAGES[0]
#             return (True, 0, message)
#         return 

#     def logout(self) -> bool:
#         url = self._url + '/webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=DownloadStation'
#         response = requests.get(url=url, verify=False)
#         data : dict[str, object] = response.json()
#         if (data['success'] == True):
#             self.sid = None
#             return True
#         return False

#     def isLoggedIn(self) -> bool:
#         return (self.sid != None)

# class File(object):
#     def __init__(self, rawFile:dict[str, object]) -> None:
#         self.fileName : str = rawFile['filename']
#         self.index : int = rawFile['index']
#         self.priority : str = rawFile['priority']
#         self.size : int = rawFile['size']
#         self.downloaded : int = rawFile['size_downloaded']
#         self.wanted : bool = rawFile['wanted']
#         return


# class Peer(object):
#     def __init__(self, rawPeer:dict[str, object]) -> None:
#         self.address = rawPeer['address']
#         self.agent = rawPeer['agent']
#         self.progress : float = rawPeer['progress']
#         self.download_speed : int = rawPeer['speed_download']
#         self.upload_speed : int = rawPeer['speed_upload']
#         return

# class Tracker(object):
#     def __init__(self, rawTracker: dict[str, object]) -> None:
#         self.peers : int = rawTracker['peers']
#         self.seeds : int = rawTracker['seeds']
#         self.status : str = rawTracker['status']
#         self.update_timer : int = rawTracker['update_timer']
#         self.url : str = rawTracker['url']
#         return

# class Task(object):
#     def __init__(self,
#                     connection: Connection,
#                     rawTask: dict[str, object],
#                 ) -> None:
#         self._url = connection.baseUrl + '/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&'
#         self._sid = connection.sid
#         self.taskId : str = rawTask['id']
#         self.status : str = rawTask['status']
#         self.size : int = rawTask['size']
#         self.title : str = rawTask['title']
#         self.type : str = rawTask['type']
#         self.user : str = rawTask['username']
#         self.completed_time : datetime = datetime.fromtimestamp(rawTask['additional']['detail']['completed_time'])
#         self.connected_leechers : int = rawTask['additional']['detail']['connected_leechers']
#         self.connected_peers : int = rawTask['additional']['detail']['connected_peers']
#         self.connected_seeders : int = rawTask['additional']['detail']['connected_seeders']
#         self.create_time : datetime = datetime.fromtimestamp(rawTask['additional']['detail']['create_time'])
#         self.destination : str = rawTask['additional']['detail']['destination']
#         self.seed_elapsed : int = rawTask['additional']['detail']['seedelapsed']
#         self.started_time : datetime = datetime.fromtimestamp(rawTask['additional']['detail']['started_time'])
#         self.total_peers : int = rawTask['additional']['detail']['total_peers']
#         self.total_pieces : int = rawTask['additional']['detail']['total_pieces']
#         self.unzip_password : str = rawTask['additional']['detail']['unzip_password']
#         self.uri : str = rawTask['additional']['detail']['uri']
#         self.waiting_seconds : int = rawTask['additional']['detail']['waiting_seconds']
#         self.files : list[File] = []
#         for rawFile in rawTask['additional']['file']:
#             self.files.append( File(rawFile) )
#         self.peers : list[Peer] = []
#         for rawPeer in rawTask['additional']['peer']:
#             self.peers.append( Peer(rawPeer) )
#         self.trackers : list[Tracker] = []
#         for rawTracker in rawTask['additional']['tracker']:
#             self.trackers.append( Tracker(rawTracker) )
#         self.downloaded_pieces : int = rawTask['additional']['transfer']['downloaded_pieces']
#         self.size_downloaded : int = rawTask['additional']['transfer']['size_downloaded']
#         self.size_uploaded : int = rawTask['additional']['transfer']['size_uploaded']
#         self.speed_download : int = rawTask['additional']['transfer']['speed_download']
#         self.speed_upload : int = rawTask['additional']['transfer']['speed_upload']
#         return

#     def remove(self, forceComplete:bool=False) -> tuple[bool, int, str]:
#         url = self._url + 'method=delete&id=%s&force_complete=%s&_sid=%s' % (
#                                                                         self.taskId,
#                                                                         str(forceComplete).lower(),
#                                                                         self._sid
#                                                                     )
#         try:
#             response = requests.get(url=url, verify=False)
#         except requests.ConnectionError as e:
#             errorMessage = "Connection error: %s" % (str(e.args))
#             return (False, 1, errorMessage)
#         except requests.ConnectTimeout as e:
#             errorMessage = "Timeout error: %s" % (str(e.args))
#             return (False, 2, errorMessage)
#         data = response.json()
#         if (data['success'] == False):
#             errorCode = data['error']['code']
#             errorMessage = ERROR_MESSAGES[errorCode]
#             return (False, errorCode, errorMessage)
#         else:
#             errorCode = data['data']['error']
#             errorMessage = ERROR_MESSAGES[errorCode]
#             if (errorCode == 0):
#                 return (True, errorCode, errorMessage)
#             else:
#                 return (False, errorCode, errorMessage)
    
#     def move(self, destination:str) -> tuple[bool, int, str]:
#         url = self._url + 'method=edit&id=%s&destination=%s&sid=%s' % (
#                                                                         self.taskId,
#                                                                         destination,
#                                                                         self._sid
#                                                                     )
#         try:
#             response = requests.get(url=url, verify=False)
#         except requests.ConnectionError as e:
#             errorMessage = "Connection error: %s" % (str(e.args))
#             return (False, 1, errorMessage)
#         except requests.ConnectTimeout as e:
#             errorMessage = "Timeout error: %s" % (str(e.args))
#             return (False, 2, errorMessage)
#         data = response.json()
#         if (data['success'] == False):
#             errorCode = data['error']['code']
#             errorMessage = ERROR_MESSAGES[errorCode]
#             return (False, errorCode, errorMessage)
#         else:
#             errorCode = data['data']['error']
#             errorMessage = ERROR_MESSAGES[errorCode]
#             if (errorCode == 0):
#                 return (True, errorCode, errorMessage)
#             else:
#                 return (False, errorCode, errorMessage)

# class DownloadStation(object):
#     TASKS : Optional[list[Task]] = None
#     def __init__(self,
#                     connection : Connection,
#                 ) -> None:
#         self._connection : Connection = connection
#         self._url = connection.baseUrl + '/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&'
#         return
    
#     def updateTasks(self) -> tuple[bool, int, str, list[Task]]:
#         url = self._url + 'method=list&additional=detail,file,transfer,tracker,peer&_sid=%s' % (self._connection.sid)
#         try:
#             response = requests.get(url=url, verify=False)
#         except requests.ConnectionError as e:
#             errorMessage = "Connection error: %s" % (str(e.args))
#             return (False, 1, errorMessage, [])
#         except requests.ConnectTimeout as e:
#             errorMessage = "Timeout error: %s" % (str(e.args))
#             return (False, 2, errorMessage, [])

#         data = response.json()
#         if (data['success'] == True):
#             taskList : list[dict[str, object]] = data['data']['tasks']
#             self.TASKS = []
#             for rawTask in taskList:
#                 self.tasks.append( Task(self._connection, rawTask) )
#         else:
#             self.TASKS = None
#         return self.tasks
    

