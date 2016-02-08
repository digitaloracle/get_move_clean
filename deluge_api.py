#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pickle
import sys


get_torrents = {"id": 3, "method": "webapi.get_torrents", "params": []}
check_conn = {"id": 2, "method": "web.connected", "params": []}
auth_string = {"id": 1, "method": "auth.login", "params": ["dieyqqp"]}
url = 'http://127.0.0.1:8112/json'


def save_cookie(cookie_file):
    cook = auth().cookies
    with open(cookie_file, 'w') as f:
        pickle.dump(requests.utils.dict_from_cookiejar(cook), f)
    sys.stderr.write('\ncookie saved')


def load_cookie(cookie_file):
    with open(cookie_file) as f:
        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
    sys.stderr.write('\ncookie loaded')
    return cookies


def call_deluge(payload):
    res = requests.post(url, json=payload, cookies=cookies)
    return res


def auth():
    res = requests.post(url, json=auth_string)
    return res


def remove_by_hash(myhash):
    payload = {"id": "4", "method": "webapi.remove_torrent",
               "params": [myhash, False]}
    # print payload
    call_deluge(payload)


def get_torrent_status(myhash):
    payload = {"id": "5", "method": "web.get_torrent_status",
               "params": [myhash, ["name", "progress"]]}
    return call_deluge(payload)


def remove_completed():
    global cookies
    removed = list()
    save_cookie('deluge.cookie')
    cookies = load_cookie('deluge.cookie')
    if call_deluge(check_conn).status_code == 200:
        torrents = call_deluge(get_torrents).json()
        for t in torrents["result"]["torrents"]:
            torhash = t["hash"]
            torname = t["name"]
            if get_torrent_status(torhash).json()["result"]["progress"] == 100.0:
                remove_by_hash(torhash)
                removed.append(torname)
    return removed

if __name__ == '__main__':
    t = remove_completed()
    print t
