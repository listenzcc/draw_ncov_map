"""
Fetch last counts from internet.
    JSON_FILENAME: filename of fetched counting as json file.
"""

import os
import time
import json
import logging
import pandas as pd
from local_profiles import profiles
from local_toolbox import getRemoteText, getTimeStamp, getAreaStat

logging.info('Start fetch last counts.')

JSON_FILENAME = os.path.join(profiles.inventory_dir,
                             'ncov_counts_{}.json')


def fetch():
    """
    Begin to fetch lastest counts from internet.
    yield:
        Will write json file as JSON_FILENAME
    """
    # Get remote text
    text = getRemoteText()

    # Get timeStamp
    try:
        timeStamp = getTimeStamp(text)
        logging.info('TimeStamp read from response.')
    except:
        timeStamp = time.time()
        logging.warning(
            'TimeStamp can not be read from response. Using current timeStamp instead.')
        print('TimeStamp can not be read from response, Using current timestamp instead. So DO NOT UPDATE again.')
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