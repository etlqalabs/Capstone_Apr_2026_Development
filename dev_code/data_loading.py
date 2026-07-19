import pandas as pd
import cx_Oracle
from sqlalchemy import create_engine, text
import logging
from project_configuration.etl_config import *

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
mysql_conn = create_engine(F"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}")


class DataLoading:
    def load_fact_sales(self):
        logger.info("Data loading in fact_sales table has started...")
        query = text("""insert into fact_sales(sales_id,product_id,store_id,quantity,total_sales,sale_date)
                        select sales_id,product_id,store_id,quantity,sales_amount,sale_date  from sales_with_details""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
            logger.info("Data loading in fact_sales table has completed...")

    def load_fact_inventory(self):
        logger.info("Data loading in fact_inventory table has started...")
        query = text("""insert into fact_inventory(product_id,store_id,quantity_on_hand,last_updated)
                        select product_id,store_id,quantity_on_hand,last_updated from stag_inventory""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
            logger.info("Data loading in fact_inventory table has completed...")

    def load_monthly_sales_summary(self):
        logger.info("Data loading in monthly_sales_summary table has started...")
        query = text("""insert into monthly_sales_summary(product_id,year,month,total_sales)
                        select product_id,year,month,total_sales from monthly_sales_summary_source""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
            logger.info("Data loading in monthly_sales_summary table has completed...")


    def load_inventory_level_by_stores(self):
        logger.info("Data loading in inventory_level_by_stores table has started...")
        query = text("""insert into inventory_levels_by_store(store_id,total_inventory)
                        select store_id,astotal_inventory from aggregated_inventory_level""")
        with mysql_conn.connect() as conn:
            logger.info(query)
            conn.execute(query)
            conn.commit()
            logger.info("Data loading in inventory_level_by_stores table has completed...")


if __name__ == "__main__":
    dl = DataLoading()
    dl.load_fact_sales()
    dl.load_fact_inventory()
    dl.load_monthly_sales_summary()
    dl.load_inventory_level_by_stores()
