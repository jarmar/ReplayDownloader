#!/usr/bin/env python3

import urllib.request
import urllib.parse
import urllib.error
import re
import os
import sys
import shutil

from bs4 import BeautifulSoup, SoupStrainer

REPLAYS_PAGE = 'http://www.teamliquid.net/replay/index.php?player1=&player2=&team1_race=1&team2_race=&description=&uploader=&map=&search=1&currentpage={}'

DOWNLOAD_URL = 'http://www.teamliquid.net/replay/download.php?replay={}'

REPLAY_ID_REGEXP = re.compile('download\.php\?replay=([0-9]+)')

def get_all_replays(page_number, destination_dir):
  destination_dir = os.path.join(destination_dir, str(page_number))
  if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

  print('Fetching page {}...'.format(page_number))
  page = urllib.request.urlopen(REPLAYS_PAGE.format(page_number))
  rep_ids = extract_replay_ids(page.read().decode('utf-8', errors='replace'))
  print('Found {} replay URLs.'.format(len(rep_ids)))
  rep_urls = [DOWNLOAD_URL.format(rep_id) for rep_id in rep_ids]
  for rep_url in rep_urls:
    print('Downloading "{}"...'.format(rep_url))
    try:
      fname = get_replay(rep_url, destination_dir)
      print('Saved as "{}"'.format(fname))
    except urllib.error.HTTPError as e:
      print('ERROR: {}. Skipping.'.format(e), file=sys.stderr)

def get_replay(rep_url, destination_dir):
  rep = urllib.request.urlopen(rep_url)
  name = rep.geturl().rsplit('/', 1)[-1]
  name = urllib.parse.unquote(name)
  fname = os.path.join(destination_dir, name)
  with open(fname, 'wb') as f:
    shutil.copyfileobj(rep, f)
  return fname

def extract_replay_ids(page):
  return REPLAY_ID_REGEXP.findall(page)

def number_of_pages():
  page = urllib.request.urlopen(REPLAYS_PAGE.format(1))
  links = BeautifulSoup(page, parse_only=SoupStrainer('a'))
  pages = 0
  for link in links:
    match = re.match('/replay/index\.php\?.*currentpage=([0-9]+)', link['href'])
    if match:
      pagenum = int(match.group(1))
      pages = max(pages, pagenum)
  return pages

if __name__ == "__main__":
  print('Figuring out number of pages...')
  num_pages = number_of_pages()
  print('Found {} pages of replays.'.format(num_pages))
  print('Downloading all pages.')
  for page in range(1, num_pages + 1):
    get_all_replays(page, sys.argv[1])
