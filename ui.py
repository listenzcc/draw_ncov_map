"""
Main ui of the project.
"""

import time

t = time.time()

from local_profiles import profiles
print('{} seconds passed'.format(time.time() - t))
from local_toolbox import readDF
print('{} seconds passed'.format(time.time() - t))
from inventory_manager import INV_MANAGER
print('{} seconds passed'.format(time.time() - t))
from painter import PAINTER
print('{} seconds passed'.format(time.time() - t))
from pprint import pprint
print('{} seconds passed'.format(time.time() - t))

manager = INV_MANAGER()
painter = PAINTER()

def printer(df):
    if df is not None:
        painter.load(readDF(df['path'].values[-1]))
        print(painter.country_df)
        print(painter.provinces_df)
        painter.draw()
    else:
        print('No record selected.')

s = ''
df = None
while not s == 'q':
    if s == 'l':
        # List inventory
        manager.list_count_files()
    if s == 'u':
        # Update inventory
        manager._update_inventory()
    if s == 'p':
        # Print selected
        printer(df)
    if s.startswith('d'):
        # Get entries on data
        df = manager.get_count_file_on_date(s.split()[1])
    if s.startswith('i'):
        # Get entry on index
        df = manager.get_count_file_on_idx(int(s.split()[1]))
    s = input(f'{df}\n>> ')
print('Done.')