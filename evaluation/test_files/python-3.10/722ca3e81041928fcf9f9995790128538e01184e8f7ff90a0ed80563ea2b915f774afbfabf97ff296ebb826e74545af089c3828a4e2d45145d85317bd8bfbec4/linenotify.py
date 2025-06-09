from urequests import post
from network import WLAN
__version__ = '0.0.4'
__author__ = 'Teeraphat Kullanankanjana'

class LineNotify:
    """
    It is a MicroPython library for sending notifications to Line Notify,
    which can be used with ESP8266 and ESP32.
    Can send both text messages, stickers and images.
    """

    def __init__(self, token):
        self.__token = token
        self.__url = 'https://notify-api.line.me/api/notify'
        self.__header = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + self.__token}

    def __sendRequest(self, payload):
        """
        Posting header and payload to the Line Notify API.
        -----
        Parameter:
        (str)payload => Request parameters
        ---
        Return:
        (int)req.status_code => HTTP status code from Line server
        """
        try:
            req = post(self.__url, headers=self.__header, data=payload)
            req.close()
            return req.status_code
        except OSError as err:
            if err.errno == -202:
                print('No Internet Connection!!')
                print('Try again!!')

    def notify(self, msg):
        """
        Notify only text message to Line Notify
        -----
        Parameter:
        (str)msg => The message you want to send notifications to LINE Notify.
        ---
        Return:
        (int)httpCode => HTTP status code from Line server
        200: Success
        400: Bad request
        401: Invalid access token
        500: Failure due to server error
        Other: Processed over time or stopped
        """
        payload = 'message={}'.format(msg).encode('utf-8')
        httpCode = self.__sendRequest(payload)

    def notifySticker(self, packageID, stickerID, msg='\n'):
        """
        Notify Sticker and text message to Line Notify
        -----
        Parameter:
        (int)stickerPackageId => Sticker Package ID.
        (int)stickerID => Sticker ID.
        (str)msg => The message you want to send notifications to LINE Notify.
        ---
        Return:
        (int)httpCode => HTTP status code from Line server
        200: Success
        400: Bad request
        401: Invalid access token
        500: Failure due to server error
        Other: Processed over time or stopped
        """
        payload = 'message={}&stickerPackageId={}&stickerId={}'.format(msg, packageID, stickerID).encode('utf-8')
        httpCode = self.__sendRequest(payload)

    def notifyImageURL(self, url, msg='\n'):
        """
        Notify Image from URL and text message to Line Notify
        -----
        Parameter:
        (str)url => Image URL (HTTP/HTTPS format)
        (str)msg => The message you want to send notifications to LINE Notify.
        ---
        Return:
        (int)httpCode => HTTP status code from Line server
        200: Success
        400: Bad request
        401: Invalid access token
        500: Failure due to server error
        Other: Processed over time or stopped
        """
        self.__msg = 'message={}&imageThumbnail={}&imageFullsize={}'.format(msg, url, url).encode('utf-8')
        httpCode = self.__sendRequest(payload)