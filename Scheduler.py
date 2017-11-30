#!/usr/bin/python

import os
import sys
from apscheduler.schedulers.gevent import GeventScheduler
import pprint
from pyPodcastParser.Podcast import Podcast
import requests
import json
import urllib2

url_to_parse = ''
url_to_post = ''
data = ''


def parse():
    response = requests.get(url_to_parse)
    podcast = Podcast(response.content)
    urls_to_download = []
    for item in podcast.items:
        pprint.pprint(item.enclosure_url)
        print(type(item.enclosure_url))
        urls_to_download.append(item.enclosure_url)
    data = {'urls': list(urls_to_download)}
    return data


def post():
    print('The url post to is %s' % url_to_post)
    req = urllib2.Request(url_to_post)
    req.add_header('Content-Type', 'application/json')
    urllib2.urlopen(req, json.dumps(data))


def help():
    print("help message")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        help()
        sys.exit(1)
    url_to_parse = sys.argv[1]
    url_to_post = sys.argv[2]
    interval = int(sys.argv[3])
    data = parse()
    scheduler = GeventScheduler()
    scheduler.add_job(post, 'interval', seconds=10)
    g = scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass
