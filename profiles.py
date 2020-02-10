"""
Profiles of the project.
"""

import logging

REMOTE_URL = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'


class PROFILES():
    def __init__(self):
        # Basic profiles
        self.inventory_dir = 'ncov_inventory'
        self.remote_url = REMOTE_URL
        # Invoke logging
        self._invoke_logging()

    def _invoke_logging(self):
        logging.basicConfig(filename='log_ncov.log',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')


profiles = PROFILES()


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
