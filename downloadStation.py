# DownloadStation:


# Lib imports:
from typing import Optional
import requests
requests.packages.urllib3.disable_warnings()
from datetime import datetime

# My imports:
from common import COMMON_ERROR_MESSAGES
from connection import Connection
from authentication import Authentication

class File(object):
    def __init__(self, rawFile:dict[str, object]) -> None:
        self.fileName : str = rawFile['filename']
        self.index : int = rawFile['index']
        self.priority : str = rawFile['priority']
        self.size : int = rawFile['size']
        self.downloaded : int = rawFile['size_downloaded']
        self.wanted : bool = rawFile['wanted']
        return


class Peer(object):
    def __init__(self, rawPeer:dict[str, object]) -> None:
        self.address = rawPeer['address']
        self.agent = rawPeer['agent']
        self.progress : float = rawPeer['progress']
        self.download_speed : int = rawPeer['speed_download']
        self.upload_speed : int = rawPeer['speed_upload']
        return

class Tracker(object):
    def __init__(self, rawTracker: dict[str, object]) -> None:
        self.peers : int = rawTracker['peers']
        self.seeds : int = rawTracker['seeds']
        self.status : str = rawTracker['status']
        self.update_timer : int = rawTracker['update_timer']
        self.url : str = rawTracker['url']
        return

class Task(object):
    def __init__(self,
                    connection: Connection,
                    rawTask: dict[str, object],
                ) -> None:
        self._url = connection.baseUrl + '/webapi/DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&'
        self._sid = connection.sid
        self.taskId : str = rawTask['id']
        self.status : str = rawTask['status']
        self.size : int = rawTask['size']
        self.title : str = rawTask['title']
        self.type : str = rawTask['type']
        self.user : str = rawTask['username']
        self.completed_time : datetime = datetime.fromtimestamp(rawTask['additional']['detail']['completed_time'])
        self.connected_leechers : int = rawTask['additional']['detail']['connected_leechers']
        self.connected_peers : int = rawTask['additional']['detail']['connected_peers']
        self.connected_seeders : int = rawTask['additional']['detail']['connected_seeders']
        self.create_time : datetime = datetime.fromtimestamp(rawTask['additional']['detail']['create_time'])
        self.destination : str = rawTask['additional']['detail']['destination']
        self.seed_elapsed : int = rawTask['additional']['detail']['seedelapsed']
        self.started_time : datetime = datetime.fromtimestamp(rawTask['additional']['detail']['started_time'])
        self.total_peers : int = rawTask['additional']['detail']['total_peers']
        self.total_pieces : int = rawTask['additional']['detail']['total_pieces']
        self.unzip_password : str = rawTask['additional']['detail']['unzip_password']
        self.uri : str = rawTask['additional']['detail']['uri']
        self.waiting_seconds : int = rawTask['additional']['detail']['waiting_seconds']
        self.files : list[File] = []
        for rawFile in rawTask['additional']['file']:
            self.files.append( File(rawFile) )
        self.peers : list[Peer] = []
        for rawPeer in rawTask['additional']['peer']:
            self.peers.append( Peer(rawPeer) )
        self.trackers : list[Tracker] = []
        for rawTracker in rawTask['additional']['tracker']:
            self.trackers.append( Tracker(rawTracker) )
        self.downloaded_pieces : int = rawTask['additional']['transfer']['downloaded_pieces']
        self.size_downloaded : int = rawTask['additional']['transfer']['size_downloaded']
        self.size_uploaded : int = rawTask['additional']['transfer']['size_uploaded']
        self.speed_download : int = rawTask['additional']['transfer']['speed_download']
        self.speed_upload : int = rawTask['additional']['transfer']['speed_upload']
        return

    def remove(self, forceComplete:bool=False) -> tuple[bool, int, str]:
        url = self._url + 'method=delete&id=%s&force_complete=%s&_sid=%s' % (
                                                                        self.taskId,
                                                                        str(forceComplete).lower(),
                                                                        self._sid
                                                                    )
        try:
            response = requests.get(url=url, verify=False)
        except requests.ConnectionError as e:
            errorMessage = "Connection error: %s" % (str(e.args))
            return (False, 1, errorMessage)
        except requests.ConnectTimeout as e:
            errorMessage = "Timeout error: %s" % (str(e.args))
            return (False, 2, errorMessage)
        data = response.json()
        if (data['success'] == False):
            errorCode = data['error']['code']
            errorMessage = COMMON_ERROR_MESSAGES[errorCode]
            return (False, errorCode, errorMessage)
        else:
            errorCode = data['data']['error']
            errorMessage = COMMON_ERROR_MESSAGES[errorCode]
            if (errorCode == 0):
                return (True, errorCode, errorMessage)
            else:
                return (False, errorCode, errorMessage)
    
    def move(self, destination:str) -> tuple[bool, int, str]:
        url = self._url + 'method=edit&id=%s&destination=%s&sid=%s' % (
                                                                        self.taskId,
                                                                        destination,
                                                                        self._sid
                                                                    )
        try:
            response = requests.get(url=url, verify=False)
        except requests.ConnectionError as e:
            errorMessage = "Connection error: %s" % (str(e.args))
            return (False, 1, errorMessage)
        except requests.ConnectTimeout as e:
            errorMessage = "Timeout error: %s" % (str(e.args))
            return (False, 2, errorMessage)
        data = response.json()
        if (data['success'] == False):
            errorCode = data['error']['code']
            errorMessage = COMMON_ERROR_MESSAGES[errorCode]
            return (False, errorCode, errorMessage)
        else:
            errorCode = data['data']['error']
            errorMessage = COMMON_ERROR_MESSAGES[errorCode]
            if (errorCode == 0):
                return (True, errorCode, errorMessage)
            else:
                return (False, errorCode, errorMessage)

class DownloadStation(object):
# Class vars:
    TASKS : Optional[list[Task]] = None     # List of Task objects.
# Download Status:
    STATUS_WAITING : str = 'waiting'
    STATUS_DOWNLOADING : str = 'downloading'
    STATUS_PAUSED : str = 'paused'
    STATUS_FINISHING : str = 'finishing'
    STATUS_FINISHED : str = 'finished'
    STATUS_HASH_CHECKING : str = 'hash_checking'
    STATUS_SEEDING : str = 'seeding'
    STATUS_FILE_HOSTING_WAITING : str = 'filehosting_waiting'
    STATUS_EXTRACTING : str = 'extracting'
    STATUS_ERROR : str = 'error'
    ERROR_MESSAGES = {
        400: 'File upload failed',  # Synology.
        401: 'Max number of tasks reached', # Synology.
        402: 'Destination denied',  # Synology.
        403: 'Destination does not exist',  # Synology.
        404: 'Invalid task id', # Synology.
        405: 'Invalid task action', # Synology.
        406: 'No default destination',  # Synology.
        407: 'Set destination failed',  # Synology.
        408: 'File does not exist', # Synology.
    }

    def __init__(self,
                    connection : Connection,
                ) -> None:
        self._connection : Connection = connection
        self._url = connection.baseUrl + 'DownloadStation/task.cgi?api=SYNO.DownloadStation.Task&version=1&'
        return
    
    def updateTasks(self) -> tuple[bool, int, str, list[Task]]:
        url = self._url + 'method=list&additional=detail,file,transfer,tracker,peer&_sid=%s' % (self._connection.sid)
        try:
            response = requests.get(url=url, verify=False)
        except requests.ConnectionError as e:
            errorMessage = "Connection error: %s" % (str(e.args))
            return (False, 1, errorMessage, [])
        except requests.ConnectTimeout as e:
            errorMessage = "Timeout error: %s" % (str(e.args))
            return (False, 2, errorMessage, [])

        data = response.json()
        if (data['success'] == True):
            taskList : list[dict[str, object]] = data['data']['tasks']
            self.TASKS = []
            for rawTask in taskList:
                self.tasks.append( Task(self._connection, rawTask) )
        else:
            self.TASKS = None
        return self.tasks
    

