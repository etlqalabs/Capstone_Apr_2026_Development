import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine
import logging

from common_utilities.utilities import read_file_and_write_to_database, download_file_from_linux_server, \
    read_database_and_write_to_database

# Logger configuration
logging.basicConfig(
    filename = "ETLApplicationLog/etljob.log",
    filemode = 'w',
    format = '%(asctime)s-%(levelname)s-%(message)s',
    level = logging.INFO
   )
logger = logging.getLogger(__name__)

# Database connections

mysql_conn = create_engine("mysql+pymysql://root:Admin%40143@localhost:3308/retail_dwh_apr_2026")
oracle_conn = create_engine("oracle+cx_oracle://system:admin@localhost:1521/xe")


class DataLoading:
    pass
