import os
import json
import logging
import requests
import pandas as pd
from pprint import pprint
from bs4 import BeautifulSoup


class NCOV_COUNTS_MANAGER():
    """
    A manager of ncov counts.
    """

    def __init__(self):
        """
        Builtin init method.
        """
        self._init_log()
        self.DIR = 'ncov_counts'
        self._check_inventory()

    def _init_log(self):
        """
        Built init log method.
        """
        LOG_FILENAME = 'ncov_counts_manager.log'
        LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, format=LOG_FORMAT)
        logging.info('=' * 80)
        logging.info('Manager starts.')

    def list_count_files(self):
        """
        Print count files.
        """
        logging.info('List count files.')
        pprint(self.COUNT_FILE_DF)
    
    def get_count_file_on_date(self, date):
        """
        Get count file(s) of date.
        """
        # Return records on that date.
        # Return empty if not found.
        df = self.COUNT_FILE_DF.set_index('date', drop=False)
        df_date = pd.DataFrame()
        try:
            df_date = pd.DataFrame(df.loc[date])
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
        """
        # Return the record on that index.
        # Return empty if not found.
        df = self.COUNT_FILE_DF.set_index('date', drop=False)
        df_idx = pd.DataFrame()
        try:
            df_idx = pd.DataFrame(df.iloc[idx])
            logging.info('Record found.') 
            logging.info(df_idx)
        except IndexError as error:
            err = repr(error)
            logging.error(err)
            print(err)
        finally:
            return df_idx

    def _check_inventory(self):
        """
        Builtin init method for check ncov_counts json files in inventory.
            self.COUNT_FILE_DF: DataFrame for files
        """
        self.COUNT_FILE_DF = pd.DataFrame()
        for name in os.listdir(self.DIR):
            if not name.startswith('ncov_counts_'):
                logging.info(f'Ignore file {name}.')
                continue
            logging.info(f'Found ncov_counts file {name}.')
            date = name[len('ncov_counts_'):len('ncov_counts_')+8]
            path = os.path.join(self.DIR, name)
            se = pd.Series(data={'date': date,
                                 'path': path})
            self.COUNT_FILE_DF = self.COUNT_FILE_DF.append(se, ignore_index=True)


if __name__ == '__main__':
    manager = NCOV_COUNTS_MANAGER()
    s = ''
    while not s == 'q':
        if s == 'l':
            manager.list_count_files()
        if s.startswith('d'):
            print(manager.get_count_file_on_date(s.split()[1]))
        if s.startswith('i'):
            print(manager.get_count_file_on_idx(int(s.split()[1])))
        s = input('>> ')
