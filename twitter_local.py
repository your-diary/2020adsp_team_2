#!/usr/bin/env python3

#-------------------------------------#

### Imports ###

# import copy
# import itertools
# import json
# import locale
# import math
# import os
# import pickle
# import random
# import re
# import signal
# import subprocess
import sys
# import time

# import numpy as np

import modules.json_local as json_local
import modules.twitter_local as twitter_local

#-------------------------------------#

### Parameteres ###

prm: dict = json_local.json_loadf('./config.json')

is_dryrun_mode: bool = bool(prm['is_dryrun_mode'])
is_debug_mode:  bool = bool(prm['is_debug_mode'])
twitter_credentials_file: str = prm['twitter_credentials_file']

if (is_debug_mode):
    print('----- Parameters -----')
    print(f'{is_dryrun_mode = }')
    print(f'{is_debug_mode = }')
    print(f'{twitter_credentials_file = }')
    print('----------------------')

#-------------------------------------#

### Command-Line Options ###

def print_usage() -> None:
    print('Usage: ./twitter_local.py <tweet content>')

if (len(sys.argv) != 2):
    print_usage()
    sys.exit(0)

tweet_content: str = sys.argv[1]

#-------------------------------------#

### main ###

tw: twitter_local.Twitter = twitter_local.Twitter(twitter_credentials_file)

print(f'Tweeting [ {tweet_content} ]...')
tw.post_tweet(tweet_content)
print('Done.')

#-------------------------------------#

