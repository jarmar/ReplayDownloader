#!/usr/bin/env python3

import urllib.request
import urllib.response
import re
import os
import sys
import shutil

REPLAYS_PAGE = 'http://www.teamliquid.net/replay/index.php?player1=&player2=&team1_race=1&team2_race=&description=&uploader=&map=&search=1&currentpage={}'

DOWNLOAD_URL = 'http://www.teamliquid.net/replay/download.php?replay={}'

REPLAY_ID_REGEXP = re.compile('download\.php\?replay=([0-9]+)')

def get_all_replays(page_number, destination_dir):
  print('Fetching page {}...'.format(page_number))
  page = urllib.request.urlopen(REPLAYS_PAGE.format(page_number))
  rep_ids = extract_replay_ids(page.read().decode('utf-8'))
  print('Found {} replay URLs.'.format(len(rep_ids)))
  rep_urls = [DOWNLOAD_URL.format(rep_id) for rep_id in rep_ids]
  for rep_url in rep_urls:
    print('Downloading "{}"...'.format(rep_url))
    fname = get_replay(rep_url, destination_dir)
    print('Saved as "{}"'.format(fname))

def get_replay(rep_url, destination_dir):
  rep = urllib.request.urlopen(rep_url)
  name = rep.geturl().rsplit('/', 1)[-1]
  fname = os.path.join(destination_dir, name)
  with open(fname, 'wb') as f:
    shutil.copyfileobj(rep, f)
  return fname

def extract_replay_ids(page):
  return REPLAY_ID_REGEXP.findall(page)

if __name__ == "__main__":
  print(get_all_replays(sys.argv[1], sys.argv[2]))


