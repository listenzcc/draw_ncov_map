"""
Local toolbox.
"""

import os
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from local_profiles import profiles


def safeGet(df, key, method='loc'):
    """
    Safely get entry on key from df.
    inputs:
        df: DataFrame to fetch from
        key: key to fetch
        method: 'loc' or 'iloc'
    outputs:
        Fetched entry in format of DataFrame,
        None if error occurred
    """
    # Regularize method
    if method not in ['loc', 'iloc']:
        logging.warning(f"Illegal method {method} found, use 'loc' instead.")
        method = 'loc'
    # Get entry of key
    try:
        if method == 'loc':
            obj = df.loc[key]
        else:
            obj = df.iloc[key]
    except:
        message = f'Fail on safeGet. df: {df}, key: {key}, method: {method}'
        print(message)
        logging.error(message)
        return None
    # Convert Series into DataFrame
    if isinstance(obj, pd.Series):
        return pd.DataFrame(obj).T
    else:
        return obj


def readDF(path):
    """
    Read DataFrame on path
    inputs:
        path: path of json file
    outputs:
        df: DataFrame of path, None if error occurred
    """
    if not os.path.exists(path):
        err = FileNotFoundError(path)
        print(repr(err))
        logging.error(repr(err))
        return None
    logging.info(f'Reading DataFrame from {path}.')
    try:
        df = pd.read_json(path)
        return df
    except ValueError as err:
        print(repr(err))
        logging.error(repr(err))
        return None


def getRemoteText():
    """
    Require text from REMOTE_URL
    outputs:
        remote text
    """
    response = requests.get(profiles.remote_url)
    HTML = response.text.encode(response.encoding).decode()
    soup = BeautifulSoup(HTML, features='lxml')
    return soup.contents[1].text


def getTimeStamp(text):
    """
    Get time stamp from text.
    The method is specific to REMOTE_URL.
    inputs:
        text: text of response of REMOTE_URL
    outputs:
        timeStamp: time stamp parsed from text
    """
    # Fetch timeStamp as between window.timeStamp and </script>
    timeStamp = float(text.split("window.timeStamp=")[
                      1].split("</script>")[0]) / 1000
    return timeStamp


def getAreaStat(text):
    """
    Get counting from text.
    The method is specific to REMOTE_URL.
    inputs:
        text: text of response of REMOTE_URL
    outputs:
        areaStat: parsed text of counting
    """
    # Cut the text after windows.getAreaStat
    subtext = text[text.find("window.getAreaStat")::]
    subtext = subtext[subtext.find("[{")::]
    # Fetch the whole array use finite state automaton
    num = 0
    chars = []
    for c in subtext:
        chars.append(c)
        if c == '[':
            num += 1
        if c == ']':
            num -= 1
        if num == 0:
            break
    areaStat = ''.join(chars)
    return areaStat
