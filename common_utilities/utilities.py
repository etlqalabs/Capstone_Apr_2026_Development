import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine
import logging
import paramiko

# Logger configuration
from project_configuration.etl_config import *

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


def read_file_and_write_to_database(file_path,file_type,db_table_name,db_connection_name):
    try:
        if file_type == "csv":
            df = pd.read_csv(file_path)
        elif file_type == "json":
            df = pd.read_json(file_path)
        elif file_type == "xml":
            df = pd.read_xml(file_path,xpath=".//item")
        else:
            raise ValueError(f"unsupported file type passed {file_type}")
        df.to_sql(db_table_name,db_connection_name,index=False)
    except Exception as e:
        logger.error(f"exception raised while reading the file from {file_path}")


def download_file_from_linux_server():
    logger.info("Product file download from Linux server started..")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(LINUX_HOSTNAME,username=LINUX_USERNAME,password=LINUX_PASSWORD)
    sftp = ssh_client.open_sftp()
    sftp.get(LINUX_REMOTE_FILE_PATH,LOCAL_FILE_PATH)
    sftp.close()
    logger.info("Product file download from Linux server completed..")


def read_database_and_write_to_database(source_query,source_database_connection,target_table,target_database_connection):
    try:
         df = pd.read_sql(source_query,source_database_connection)
         df.to_sql(target_table,target_database_connection,index=False)
    except Exception as e:
        logger.error(f"exception raised while reading and writing in tot the tables")

