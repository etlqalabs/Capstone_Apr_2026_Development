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


class DataTransformation:

    def transform_Filter_Sales(self,source_query,source_database_connection,target_table,target_database_connection):
        logger.info("Data Transformation for sales has started...")
        try:
            read_database_and_write_to_database(source_query, source_database_connection, target_table,
                                            target_database_connection)

            logger.info("Data Transformation for sales has completed...")
        except Exception as e:
            logger.error(f"Error encountered while sales data Transformation,{e},exc_info=True")


    def transform_Router_High_Sales(self, source_query, source_database_connection, target_table,
                                                target_database_connection):
        logger.info("Router- High - Data Transformation for sales has started...")
        try:
            read_database_and_write_to_database(source_query, source_database_connection, target_table,
                                                target_database_connection)

            logger.info("Router- High - Data Transformation for sales has completed...")
        except Exception as e:
            logger.error(f"Error encountered while Router- High - sales - data Transformation,{e},exc_info=True")


    def transform_Router_Low_Sales(self, source_query, source_database_connection, target_table,
                                    target_database_connection):
        logger.info("Router- Low - Data Transformation for sales has started...")
        try:
            read_database_and_write_to_database(source_query, source_database_connection, target_table,
                                                target_database_connection)

            logger.info("Router- Low - Data Transformation for sales has completed...")
        except Exception as e:
            logger.error(f"Error encountered while Router- Low - sales - data Transformation,{e},exc_info=True")


    def transform_Aggregator_Sales(self, source_query, source_database_connection, target_table,
                                    target_database_connection):
        logger.info("Aggregator- Data Transformation for sales has started...")
        try:
            read_database_and_write_to_database(source_query, source_database_connection, target_table,
                                                target_database_connection)

            logger.info("Aggregator- Data Transformation for sales has completed..")
        except Exception as e:
            logger.error(f"Error encountered while Aggregator- Data Transformation,{e},exc_info=True")


    def transform_joiner_sales_product_stores(self, source_query, source_database_connection, target_table,
                                    target_database_connection):
        logger.info("Joiner ator- Data Transformation for sales has started...")
        try:
            read_database_and_write_to_database(source_query, source_database_connection, target_table,
                                                target_database_connection)

            logger.info("Joiner- Data Transformation for sales has completed..")
        except Exception as e:
            logger.error(f"Error encountered while Joiner- Data Transformation,{e},exc_info=True")


    def transform_Aggregator_Inventory(self, source_query, source_database_connection, target_table,
                                    target_database_connection):
        logger.info("Aggregator- Inventory- Data Transformation for Inventory has started...")
        try:
            read_database_and_write_to_database(source_query, source_database_connection, target_table,
                                                target_database_connection)

            logger.info("Aggregator- Inventory- Data Transformation for Inventory has completed..")
        except Exception as e:
            logger.error(f"Error encountered while Aggregator-Inventory-  Data Transformation,{e},exc_info=True")





if __name__ == "__main__":
    dt = DataTransformation()


    sales_filter_source_query = """select * from stag_sales where sale_date>='2024-09-10'"""
    dt.transform_Filter_Sales(sales_filter_source_query, mysql_conn, "filtered_sales", mysql_conn)


    sales_router_high_source_query = """select * from filtered_sales where region='High'"""
    dt.transform_Router_High_Sales(sales_router_high_source_query, mysql_conn, "high_sales", mysql_conn)


    sales_router_low_source_query = """select * from filtered_sales where region='Low'"""
    dt.transform_Router_Low_Sales(sales_router_low_source_query, mysql_conn, "low_sales", mysql_conn)


    sales_aggregator_source_query = """select fs.product_id,year(fs.sale_date) as year,month(fs.sale_date) as month, sum(fs.price*fs.quantity) as total_sales 
                                    from filtered_sales as fs group by fs.product_id,year(fs.sale_date),month(fs.sale_date)"""
    dt.transform_Aggregator_Sales(sales_aggregator_source_query, mysql_conn, "monthly_sales_summary_source", mysql_conn)



    sales_product_stores_joiner_source_query ="""select fs.sales_id,fs.quantity,fs.price,fs.quantity*fs.price as sales_amount,fs.sale_date,
                                    p.product_id,p.product_name,s.store_id,s.store_name
                                    from filtered_sales as fs inner join stag_products as p on fs.product_id = p.product_id
                                    inner join stag_stores as s on fs.store_id = s.store_id"""
    dt.transform_joiner_sales_product_stores(sales_product_stores_joiner_source_query, mysql_conn, "sales_with_details", mysql_conn)




    inventory_aggregator_source_query = """select store_id,sum(quantity_on_hand) astotal_inventory from stag_inventory group by store_id"""
    dt.transform_Aggregator_Inventory(inventory_aggregator_source_query, mysql_conn, "aggregated_inventory_level", mysql_conn)






