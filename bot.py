#!/usr/bin/env python3

import os
import sys
import telegram_bot
import time
import json
import util
import time
import socket
from dns import resolver
import datetime

from platform import system as system_name
from subprocess import call as system_call


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Ping command count option as function of OS
    param = '-n' if system_name().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    # Pinging
    if system_name().lower() == 'windows':
        return system_call(command, stdout=open('nul')) == 0
    else:
        return system_call(command, stdout=open('/dev/null')) == 0


def resolve(host):
    """
    Return ip as string if resolved
    else returns None
    """

    try:
        return str(resolver.query(host).rrset).split(' ')[-1]
    except:
        return None


def sock_connect(host):
    try:
        s = socket.socket()
        s.connect((host, 1080))
        s.close()
        return True
    except:
        return False


def check_all(settings):
    host = settings['host_to_check']
    out = ""
    try:
        out += settings['provider'] + "\n"
    except:
        pass
    out += "Pinging {}, result: {}".format(host, ping(host)) + "\n"
    out += "Resolving {}, result: {}".format(host, resolve(host)) + "\n"
    out += "Socket connection to {}:1080, result: {}".format(host, sock_connect(host))
    return out


def add_mailing_list(s, m):
    try:
        mlist = json.load(open(s['mailing_list']))
    except FileNotFoundError as e:
        print("Mailing list is not found, creating new!")
        mlist = {'chats': []}

    chat_id = m['chat']['id']
    if chat_id not in mlist['chats']:
        mlist['chats'].append(m['chat']['id'])
        print("Adding new chat with id {}".format(m['chat']['id']))
    json.dump(mlist, open(s['mailing_list'], 'w'), sort_keys=False, indent=4)


def get_mailing_list(s):
    return json.load(open(s['mailing_list']))['chats']


class Differ:
    def __init__(self, host):
        self.last_ping = True
        self.last_resolve = None
        self.last_sock = True
        self.host = host

    def update_ping(self):
        ans = ping(self.host)
        if self.last_ping != ans:
            self.last_ping = ans
            return True, ""
        else:
            return False, ""

    def update_resolve(self):
        ans = resolve(self.host)
        if ans != self.last_resolve:
            out = "Resolve: {} -> {}\n".format(self.last_resolve, ans)
            self.last_resolve = ans
            return True, out
        else:
            return False, ""

    def update_sock(self):
        ans = sock_connect(self.host)
        if ans != self.last_sock:
            out = "Connection: {} -> {}\n".format(self.last_sock, ans)
            self.last_sock = ans
            return True, out
        else:
            return False, ""


def main(bot, settings):
    just_launched = True
    d = Differ(settings['host_to_check'])
    while True:
        messages = bot.get_messages()
        for m in messages:
            if m['text'].startswith("/catch"):
                add_mailing_list(settings, m)
            elif m['text'].startswith("/check"):
                bot.send_message(m['chat']['id'], check_all(settings))

        status_message = ""
        updated_resolve = d.update_resolve()
        updated_sock_connect = d.update_sock()

        if updated_resolve[0]:
            status_message += updated_resolve[1]

        if updated_sock_connect[0]:
            if not d.last_sock and not ping("ya.ru"): # if ping(ya) is ok but host is not
                status_message += updated_sock_connect[1]
            elif updated_resolve[0]:
                status_message += updated_sock_connect[1]

        if status_message != "" and not just_launched:
            mlist = get_mailing_list(settings)
            for chat in mlist:
                bot.send_message(chat, status_message)

        just_launched = False
        time.sleep(settings['request_timeout'])


if __name__ == '__main__':
    if not(sys.version_info.major >= 3 and sys.version_info.minor >= 4):
        if (sys.version_info.minor < 6):
            print("Tested on Python 3.6, 3.4-3.5 work is not guaranteed")
        print("Python 3.4+ is required!")
        exit(1)

    settings = util.load_settings()

    bot_token = ""
    try:
        with open(settings['token_file']) as fin:
            bot_token = fin.read()
    except Exception as e:
        print("Cannot start bot! Error: ", e)
        exit(1)

    try:
        proxies = settings['proxies']
    except KeyError as e:
        proxies = None
        print("Proxy server isn't set!")

    try:
        bot = telegram_bot.TelegramBot(bot_token, proxies)
    except Exception as e:
        print(e)
        print("Cannot establish connection!")
        exit(2)
    print("Connected through ", proxies)

    main(bot, settings)
