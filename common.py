
# Common Vars / Functions:

# Common error Codes taken from:
#   https://global.download.synology.com/download/Document/Software/DeveloperGuide/Os/DSM/All/enu/DSM_Login_Web_API_Guide_enu.pdf

# My error codes:
ERROR_CONNECTION_ERROR = 1
ERROR_TIMEOUT_ERROR = 2
ERROR_MALFORMED_JSON = 3
ERROR_HTTP_ERROR = 4
ERROR_SSL_ERROR = 5

# Synology / My errors error messages:
COMMON_ERROR_MESSAGES : dict[int, str] = {
# Unknown error code:
     -1: '<UNKNOWN ERROR>', # My error code.
# Success / No error:
      0: 'No error',    # Synology.
# My Error Codes:
      1: 'Connection error',    # My error code.
      2: 'Timeout error',   # My error code.
      3: 'Malformed JSON',  # My error code.
      4: 'HTTP error',      # My error code.
      5: 'SSL certificate error',   # My error code.
# Synoloogy Common Error Codes:
    100: 'Unknown error',   # Synology. Unknown.
    101: 'Invalid parameter',   # Synology.
    102: 'The requested API does not exist',    # Synology.
    103: 'The requested method does not exist', # Synology.
    104: 'The requested version does not support the functionality',    # Synology.
    105: 'The logged in session does not have permission',  # Synology.
    106: 'Session timeout', # Synology.
    107: 'Session interrupted by duplicate login',  # Synology.
    108: 'Failed to upload the file.', # Synology.
    109: 'The network connection is unstable or the system is busy.', # Synology.
    110: 'The network connection is unstable or the system is busy.', # Synology.
    111: 'The network connection is unstable or the system is busy.', # Synology.
    112: 'Preserve for other purpose.', # Synology.
    113: 'Preserve for other purpose.', # Synology.
    114: 'Lost parameters for this API.', # Synology.
    115: 'Not allowed to upload a file.', # Synology.
    116: 'Not allowed to perform for a demo site.', # Synology.
    117: 'The network connection is unstable or the system is busy.', # Synology.
    118: 'The network connection is unstable or the system is busy.', # Synology.
    119: 'Invalid session.', # Synology.
# Error codes 120 - 149 Are reserved for other purpooses.
    150: 'Request source IP does not match the login IP.', # Synology.
}
# undefined Error Codes: 6 - 99
for i in range(6, 99 + 1):
    COMMON_ERROR_MESSAGES[i] = '<UNDEFINED>'
# Synology Reserved ErrorCodes: 120-149
for i in range(120, 149 + 1):
    COMMON_ERROR_MESSAGES[i] = 'Preserve for other purpose.'

# Download Station error codes taken from:
#   https://global.download.synology.com/download/Document/Software/DeveloperGuide/Package/DownloadStation/All/enu/Synology_Download_Station_Web_API.pdf



def buildUrl(
        baseUrl : str,  # Base url including protocol ie: https://server:port/webapi/.
        path : str,     # Path specified by ApiData object ie: query.cgi.
        api : str,      # api name ie: SYNO.API.Info.
        version: int,   # Version of api, ie: 1.
        method : str    # Method name ie: query.
    ) -> str:

    url = baseUrl + path
    url = url + "?api=%s&version=%i&method=%s" % (api, version, method)
    return url
