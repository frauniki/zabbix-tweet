import configparser


config = configparser.ConfigParser()
config.read('zabbix-tweet.conf')


ZABBIX_URL = config['zabbix']['url']
ZABBIX_USER = config['zabbix']['username']
ZABBIX_PASS = config['zabbix']['password']

TWITTER_MEDIA = "https://upload.twitter.com/1.1/media/upload.json"
TWITTER_STATUSES = "https://api.twitter.com/1.1/statuses/update.json"

CK = config['twitter-api']['ck']
CS = config['twitter-api']['cs']
AT = config['twitter-api']['at']
ATS = config['twitter-api']['ats']
