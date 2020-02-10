"""
Fetch last counts from internet.
    JSON_FILENAME: filename of fetched counting as json file.
"""

import os
import time
import json
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from profiles import profiles, getTimeStamp, getAreaStat

logging.info('Start fetch last counts.')

JSON_FILENAME = os.path.join(profiles.inventory_dir,
                             'ncov_counts_{}.json')


def fetch():
    """
    Begin to fetch lastest counts from internet.
    yield:
        Will write json file as JSON_FILENAME
    """
    # Request from internet
    response = requests.get(profiles.remote_url)
    HTML = response.text.encode(response.encoding).decode()
    soup = BeautifulSoup(HTML, features='lxml')
    text = soup.contents[1].text

    # Get timeStamp
    try:
        timeStamp = getTimeStamp(text)
        logging.info('TimeStamp read from response.')
    except:
        timeStamp = time.time()
        logging.warning(
            'TimeStamp can not be read from response. Using current timeStamp instead.')
    logging.info(f'TimeStamp is {timeStamp}.')

    # Get counting
    counting_json = json.loads(getAreaStat(text))

    # Make counting_df
    counting_df = pd.read_json(json.dumps(counting_json))
    print(counting_df)

    # Save counting_df
    fpath = JSON_FILENAME.format(time.strftime(
        '%Y%m%d-%H%M%S', time.localtime(timeStamp)))
    counting_df.to_json(fpath)
    logging.info(f'Save json file {fpath}.')


if __name__ == '__main__':
    fetch()