import os
import logging
import pandas as pd
from pprint import pprint
from profiles import profiles
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

    def _save_loc(self, key, method='loc'):
        """
        Builtin method to fetch entry from self.COUNT_FILE_DF as key using loc or iloc.
        inputs:
            key: key to fetch
            method: loc or iloc
        outputs:
            obj: the DataFrame being fetched
        """
        # Get df
        df = self.COUNT_FILE_DF
        # Get obj
        if method == 'loc':
            obj = df.loc[key]
        else:
            obj = df.iloc[key]
        # Transfrom Series into DataFrame
        if isinstance(obj, pd.Series):
            return pd.DataFrame(obj).T
        else:
            return obj


    def get_count_file_on_date(self, date):
        """
        Get count file(s) of date.
        inputs:
            date: string of date in format of yyyymmdd
        outputs:
            df_date: DataFrame of file info, None if not found
        """
        df_date = None 
        try:
            df_date = self._save_loc(date, method='loc') # df.loc[date]
            logging.info(f'Records found on date {date}.')
            logging.info(df_date)
        except KeyError as error:
            err = repr(error)
            logging.error(err)
            print(err)
        finally:
            return df_date

    def get_count_file_on_idx(self, idx):
        """
        Get count file(s) of idx.
        inputs:
            idx: index of interest
        outputs:
            df_idx: DataFrame of file info, None if not found
        """
        df_idx = None
        try:
            df_idx = self._save_loc(idx, method='iloc') # df.iloc[idx]
            logging.info('Record found.')
            logging.info(df_idx)
        except IndexError as error:
            err = repr(error)
            logging.error(err)
            print(err)
        finally:
            return df_idx

    def _update_inventory(self):
        """
        Builtin method for update inventory.
        """
        # fetch lastest counting
        fetch_last_counts.fetch()

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
            se = pd.Series(data={'date': date,
                                 'path': path})
            df = df.append(se, ignore_index=True)

        self.COUNT_FILE_DF = df.set_index('date', drop=False)


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
            if df is not None:
                pprint(pd.read_json(df['path'].values[0]))
        if s.startswith('d'):
            # Get entries on data
            df = manager.get_count_file_on_date(s.split()[1])
        if s.startswith('i'):
            # Get entry on index
            df = manager.get_count_file_on_idx(int(s.split()[1]))
        s = input(f'{df}\n>> ')
    print('Done.')
