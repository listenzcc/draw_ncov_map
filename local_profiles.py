"""
Profiles of the project.
"""

import os
import logging
from local_profiles import BAIDU_AK, MAPBOX_ACCESS_TOKEN

REMOTE_URL = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
inventory_dir = 'ncov_inventory'
mapper_server_dir = 'maper_server_memory'


class PROFILES():
    def __init__(self):
        # Basic profiles
        self.inventory_dir = inventory_dir
        self.mapper_server_dir = mapper_server_dir
        self.remote_url = REMOTE_URL
        self.baidu_ak = BAIDU_AK
        self.mapbox_ak = MAPBOX_ACCESS_TOKEN
        # Invoke logging
        self._invoke_logging()
        # Basic check
        self._check_dirs()

    def _invoke_logging(self):
        logging.basicConfig(filename='log_ncov.log',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _check_dirs(self):
        """
        Check dirs if they exist, make them if not.
        """
        for dir in [self.inventory_dir,
                    self.mapper_server_dir]:
            if not os.path.exists(dir):
                message = f'Dir not exists: {dir}. Make it.'
                logging.warning(message)
                os.mkdir(dir)


profiles = PROFILES()
