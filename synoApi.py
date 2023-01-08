# Std lib imports:
from typing import Optional
import requests
requests.packages.urllib3.disable_warnings()
import socket
import json
from datetime import datetime
from http import HTTPStatus
HTTP_STATUS_CODES = [ status.value for status in list(HTTPStatus)]

# My lib imports:
from common import COMMON_ERROR_MESSAGES
from connection import Connection
from apiInfo import ApiData, ApiInfo
from authentication import Authentication



