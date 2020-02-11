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


