import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine
import logging

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

    def extract_sales_data_from_file_to_stag(self):
        pass


    def extract_product_data_from_file_to_stag(self):
        logger.info("Data extraction for products has started...")
        try:
            df = pd.read_csv("Sources/product_data_from_linux.csv")
            df.to_sql("stag_products",mysql_conn,index=False)
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


    def extract_stores_data_from_oracle_to_stag(self):
        logger.info("Data extraction for stores has started...")
        try:
            df = pd.read_sql("""select * from stores""",oracle_conn)
            df.to_sql("stag_stores", mysql_conn, index=False)
            logger.info("Data extraction for stores has completed...")
        except Exception as e:
            logger.error(f"Error encountered while stores data extraction,{e},exc_info=True")


if __name__ == "__main__":
    de = DataExtraction()
    de.extract_sales_data_from_file_to_stag()
    de.extract_product_data_from_file_to_stag()
    de.extract_inventory_data_from_file_to_stag()
    de.extract_supplier_data_from_file_to_stag()
    de.extract_stores_data_from_oracle_to_stag()
