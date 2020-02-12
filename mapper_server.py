"""
My custom mapper server.
Get latitude and longitude using BAIDU API.
"""

import os
import logging
import geocoder
import pandas as pd
from local_profiles import profiles


class MAPPER_SERVER():
    def __init__(self):
        logging.info('MAPPER_SERVER starts.')
        self.memory_path = os.path.join(
            profiles.mapper_server_dir, 'memory.json')
        self._read_memory()

    def _read_memory(self):
        """
        Read memory json file as DataFrame,
        if file not exists, use empty DataFrame instead.
        yield:
            self.memory: the memory DataFrame
        """
        if os.path.exists(self.memory_path):
            logging.info(f'Get memory from {self.memory_path}')
            self.memory = pd.read_json(self.memory_path)
        else:
            logging.warning(
                f'Memory file not exists. Use empty DataFrame instead.')
            self.memory = pd.DataFrame(columns=['latitude',
                                                'longitude'])

    def solid_memory(self):
        """
        Write memory DataFrame into json file.
        yield:
            Write memory json file.
        """
        self.memory.to_json(open(self.memory_path, 'w'))

    def checkout(self, name):
        """
        Check out position of name.
        inputs:
            name: name of location
        outputs:
            lat: latitude of location
            lng: longitude of location
        yield:
            Update memory if not remembered
        """
        if name in self.memory.index:
            lat = self.memory.loc[name].latitude
            lng = self.memory.loc[name].longitude
        else:
            message = f'Search online: {name}.'
            print(message)
            logging.info(message)
            try:
                g = geocoder.baidu(name, key=profiles.baidu_ak)
                lat, lng = g.latlng
                se = pd.Series(data={'latitude': lat,
                                     'longitude': lng},
                               name=name)
                self.memory = self.memory.append(se)
            except KeyError as err:
                lat, lng = None, None
                message = repr(err)
                print(f'Error occured on checkout {name}: {message}')
                logging.error(message)
        return lat, lng


if __name__ == '__main__':
    ms = MAPPER_SERVER()
    s = 'l'
    while not s == 'q':
        if s == 'l':
            print(ms.memory)
        if s == 'r':
            ms._read_memory()
            print(ms.memory)
        if s not in ['l', 'r']:
            print(ms.checkout(s))
        s = input('>> ')
    ms.solid_memory()
