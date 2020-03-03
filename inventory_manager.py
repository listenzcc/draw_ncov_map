import os
import logging
import pandas as pd
from pprint import pprint
from local_profiles import profiles
from local_toolbox import readDF, safeGet
import fetch_last_counts


class INV_MANAGER():
    """
    A manager of ncov counts.
    """

    def __init__(self):
        """
        Builtin init method.
        yield:
            DIR: dir of inventory
        """
        logging.info('INV_MANAGER starts.')
        self.DIR = profiles.inventory_dir
        self._check_inventory()

    def list_count_files(self):
        """
        Print count files.
        """
        logging.info('List count files.')
        pprint(self.COUNT_FILE_DF)

    def get_count_file_on_date(self, date):
        """
        Get count file(s) of date.
        inputs:
            date: string of date in format of yyyymmdd
        outputs:
            df_date: DataFrame of file info, None if not found
        """
        df_date = safeGet(self.COUNT_FILE_DF, date, method='loc')
        logging.info(f'Records found on date {date}.')
        logging.info(df_date)
        return df_date

    def get_count_file_on_idx(self, idx):
        """
        Get count file(s) of idx.
        inputs:
            idx: index of interest
        outputs:
            df_idx: DataFrame of file info, None if not found
        """
        df_idx = safeGet(self.COUNT_FILE_DF, idx, method='iloc')
        logging.info(f'Record found on {idx}.')
        logging.info(df_idx)
        return df_idx

    def _update_inventory(self):
        """
        Builtin method for update inventory.
        """
        # fetch lastest counting
        fetch_last_counts.fetch()
        self._check_inventory()

    def _check_inventory(self):
        """
        Builtin init method for check ncov_counts json files in inventory.
        yield:
            self.COUNT_FILE_DF: DataFrame for files
        """
        df = pd.DataFrame()
        for name in os.listdir(self.DIR):
            if not name.startswith('ncov_counts_'):
                logging.info(f'Ignore file {name}.')
                continue
            logging.info(f'Found ncov_counts file {name}.')
            date = name[len('ncov_counts_'):len('ncov_counts_')+8]
            path = os.path.join(self.DIR, name)
            
            inside = pd.read_json(path)
            sum_confirmedCount = inside['confirmedCount'].sum().astype(int)

            se = pd.Series(data={'date': date,
                                 'path': path,
                                 'sum': sum_confirmedCount})
            df = df.append(se, ignore_index=True)

        self.COUNT_FILE_DF = df.set_index('date', drop=False)


def printer(df):
    if df is not None:
        pprint(readDF(df['path'].values[-1]))
    else:
        print('No record selected.')


if __name__ == '__main__':
    manager = INV_MANAGER()
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
