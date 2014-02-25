#!/usr/bin/env python3

import urllib.request
import urllib.response
import re

REPLAYS_PAGE = 'http://www.teamliquid.net/replay/index.php?player1=&player2=&team1_race=1&team2_race=&description=&uploader=&map=&search=1&currentpage={}'

DOWNLOAD_URL = 'http://www.teamliquid.net/replay/download.php?replay={}'

REPLAY_ID_REGEXP = re.compile('replay/download\.php\?replay=([0-9]+)')

def get_all_replays(page_number):
  page = urllib.request.urlopen(REPLAYS_PAGE % page_number)
  return extract_replay_ids(page)

def extract_replay_ids(page):
  return REPLAY_ID_REGEXP.findall(page)


