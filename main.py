from extract.crypto_api import extract_crypto_data
from transform.clean_crypto import transform_data
from load.to_database import load_data, create_database
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_pipeline():
    """Runs the complete ETL pipeline"""
    try:
        logging.info("Starting ETL pipeline")
        
        # Ensure database exists
        create_database()
        
        # Extract
        logging.info("Extracting data from API")
        raw_data = extract_crypto_data()
        
        # Transform
        logging.info("Transforming data")
        transformed_data = transform_data(raw_data)
        
        # Load
        logging.info("Loading data to database")
        load_data(transformed_data)
        
        logging.info("ETL pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()