import io
import json
import requests
from datetime import datetime
from requests_oauthlib import OAuth1Session

import env


twitter = OAuth1Session(env.CK, env.CS, env.AT, env.ATS)
with open('zabbix.json', 'r') as zabbix_target:
    zabbix_targets = json.load(zabbix_target)


class ZabbixLib:
    def __init__(self, host=None, user=None, passwd=None):
        self.__auth = None
        self.__id = 1
        self.__host = host
        obj = self.__request('user.login', {
            'user': user,
            'password': passwd,
        })
        self.__auth = obj

    def __request(self, method, param):
        body = {
            'jsonrpc': '2.0',
            'method': method,
            'params': param,
            'id': self.__id,
            'auth': self.__auth,
        }

        self.__id = self.__id + 1
        res = requests.post(self.__host + '/api_jsonrpc.php', json.dumps(body), headers={
                            'Content-Type': 'application/json'})
        obj = res.json()
        return obj['result']

    def loadGraphImage(self, graphid, period=3600):
        cookies = {'zbx_sessionid': self.__auth}
        res = requests.get(self.__host + '/chart2.php?' +
                           f"graphid={graphid}", cookies=cookies)
        return res.content


def get_zabbix_graph(graphid):
    zabbix = ZabbixLib(host=env.ZABBIX_URL,
                       user=env.ZABBIX_USER, passwd=env.ZABBIX_PASS)
    img = zabbix.loadGraphImage(graphid)
    return upload_twitter(img)


def upload_twitter(image):
    data = {"media": io.BytesIO(image)}
    req_media = twitter.post(env.TWITTER_MEDIA, files=data)
    if req_media.status_code == 200:
        return json.loads(req_media.text)['media_id']
    else:
        print(f"Image upload failed.\nmsg: {req_media.text}")
        exit()


def send_tweet(target):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text = f"[Zabbix Information] <{date}> {target['host']}: {target['name']}"
    data = {"status": text, "media_ids": get_zabbix_graph(target['graphid'])}
    req = twitter.post(env.TWITTER_STATUSES, params=data)
    if req.status_code == 200:
        print("Tweet send succeed.")
    else:
        print(f"Tweet send failed.\nStatus: {req.status_code}")


if __name__ == '__main__':
    for i in zabbix_targets['targets']:
        send_tweet(i)
