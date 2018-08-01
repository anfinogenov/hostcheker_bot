import json
import time
import util
import requests


class TelegramBot:
    VERSION = "0.2d"
    CONNECTION_LOST_TIMEOUT = 60

    def __init__(self, token, proxies=None):
        print("Telegram Bot API-class {}. © Maxim Anfinogenov, 2017-2018".format(self.VERSION))
        self.token = token
        self.url = "https://api.telegram.org/bot{}/".format(self.token)
        self.update_id = 0
        self.proxies = proxies
        self._check_token()
        print("Connected to Telegram API")

    def _check_token(self):
        r = util.nothrow_get(self.url + "getMe", proxies=self.proxies)
        if r == None:
            raise ValueError("Can't connect!")

        if r.status_code == 200 and r.json()['ok'] == True:
            return True
        else:
            raise ValueError("Invalid token!")

    def get_messages(self):
        out = []
        r = util.nothrow_get("{}getUpdates?offset={}".format(self.url, self.update_id),
                             timeout=self.CONNECTION_LOST_TIMEOUT,
                             proxies=self.proxies)
        if r == None:
            return out
        else:
            r = r.json()

        if r['ok'] and 'result' in r.keys():
            for i in r['result']:
                if 'message' in i.keys() and 'text' in i['message'].keys():
                    out.append(i['message'])
                if i['update_id'] >= self.update_id:
                    self.update_id = i['update_id']+1
        return out

    def send_message(self, chat_id, text, parse_mode=''):
        try:
            r = requests.post("{}sendMessage".format(self.url),
                              data={'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode},
                              timeout=self.CONNECTION_LOST_TIMEOUT,
                              proxies=self.proxies)
        except requests.exceptions.RequestException as e:
            print("{} | Error while sending message:".format(int(time.time())), e)
            return None
        except Exception as e:
            print("Unknown exception caught:", e)

        return r
