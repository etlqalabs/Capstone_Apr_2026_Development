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


class DataExtraction:

    def extract_sales_data_from_file_to_stag(self,file_path,file_type,db_table_name,db_connection_name):
        logger.info("Data extraction for Sales has started...")
        try:
            read_file_and_write_to_database(file_path, file_type, db_table_name, db_connection_name)
            logger.info("Data extraction for Sales has completed...")
        except Exception as e:
            logger.error(f"Error encountered while Sales data extraction,{e},exc_info=True")

    def extract_stores_data_from_oracle_to_stag(self,source_query,source_database_connection,target_table,target_database_connection):
        logger.info("Data extraction for stores has started...")
        try:
            read_database_and_write_to_database(source_query, source_database_connection, target_table,
                                            target_database_connection)

            logger.info("Data extraction for stores has completed...")
        except Exception as e:
            logger.error(f"Error encountered while stores data extraction,{e},exc_info=True")


    def extract_product_data_from_file_to_stag(self,file_path,file_type,db_table_name,db_connection_name):
        logger.info("Data extraction for products has started...")
        try:
            download_file_from_linux_server()
            read_file_and_write_to_database(file_path,file_type,db_table_name,db_connection_name)
            logger.info("Data extraction for products has completed...")
        except Exception as e:
            logger.error(f"Error encountered while product data extraction,{e},exc_info=True")
            #logger.info("data extrcation failed due to file not available")


    def extract_inventory_data_from_file_to_stag(self):
        logger.info("Data extraction for Inventory has started...")
        try:
            df = pd.read_xml("Sources/inventory_data.xml",xpath=".//item")
            df.to_sql("stag_inventory", mysql_conn, index=False)
            logger.info("Data extraction for Inventory has completed...")
        except Exception as e:
            logger.error(f"Error encountered while Inventory data extraction,{e},exc_info=True")



    def extract_supplier_data_from_file_to_stag(self):
        logger.info("Data extraction for supplier has started...")
        try:
            df = pd.read_json("Sources/supplier_data.json")
            df.to_sql("stag_supplier", mysql_conn, index=False)
            logger.info("Data extraction for supplier has completed...")
        except Exception as e:
            logger.error(f"Error encountered while supplier data extraction,{e},exc_info=True")



if __name__ == "__main__":
    de = DataExtraction()

    #de.extract_product_data_from_file_to_stag("Sources/product_data_from_linux_jul18.csv", "csv", "stag_products_new",mysql_conn)
    #de.extract_sales_data_from_file_to_stag("Sources/sales_data_s3.csv", "csv", "stag_sales",mysql_conn)
    source_query = """select * from stores"""
    de.extract_stores_data_from_oracle_to_stag(source_query,oracle_conn,"stag_stores",mysql_conn)
    # df = pd.read_sql("""select * from stores""",oracle_conn)
    # df.to_sql("stag_stores", mysql_conn, index=False)

    '''
    de.extract_sales_data_from_file_to_stag()
    
    de.extract_inventory_data_from_file_to_stag()
    de.extract_supplier_data_from_file_to_stag()
    de.extract_stores_data_from_oracle_to_stag()
    '''
