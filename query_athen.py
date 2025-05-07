import boto3
import json
import time
import os
import logging
from dotenv import load_dotenv

# Setup logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__n  ame__)

# Load environment variables from .env
load_dotenv()

# Load config from config.json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except Exception as e:
    logger.error(f"Failed to load config.json: {e}")
    exit(1)

# Initialize Athena client
try:
    athena = boto3.client(
        'athena',
        region_name=os.getenv('AWS_REGION', 'us-west-2')  # or use config if you prefer
    )
except Exception as e:
    logger.error(f"Failed to initialize boto3 Athena client: {e}")
    exit(1)

def run_query(query, label):
    logger.info(f"Running {label}")
    try:
        response = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': config['database']},
            ResultConfiguration={'OutputLocation': config['output_location']},
            WorkGroup=config['workgroup']
        )

        query_execution_id = response['QueryExecutionId']
        logger.info(f"{label} started. Execution ID: {query_execution_id}")

        # Wait for query to complete
        while True:
            result = athena.get_query_execution(QueryExecutionId=query_execution_id)
            status = result['QueryExecution']['Status']['State']
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(2)

        if status == 'SUCCEEDED':
            logger.info(f"{label} succeeded.")
            return athena.get_query_results(QueryExecutionId=query_execution_id)
        else:
            reason = result['QueryExecution']['Status'].get('StateChangeReason', 'No reason provided')
            logger.error(f"{label} failed. Status: {status}. Reason: {reason}")
            return None

    except Exception as e:
        logger.exception(f"Error during {label}: {e}")
        return None

# Actual SQL queries from your assignment
queries = {
    "Query 1 - First 10 rows": "SELECT * FROM weather_data_lake_a3 LIMIT 10;",
    "Query 2 - Average MinTemp": "SELECT AVG(MinTemp) AS average_min_temp FROM weather_data_lake_a3;",
    "Query 3 - Average Rainfall": "SELECT AVG(Rainfall) AS average_rainfall FROM weather_data_lake_a3;",
    "Query 4 - WindSpeed9am > 50": "SELECT * FROM weather_data_lake_a3 WHERE WindSpeed9am > 50;",
    "Query 5 - Count WindDir9am = 'North'": "SELECT COUNT(*) AS north_wind_count FROM weather_data_lake_a3 WHERE WindDir9am = 'North';"
}

# Run and print each query
for label, sql in queries.items():
    result = run_query(sql, label)
    print(f"\n--- {label} Results ---")
    if result:
        for row in result['ResultSet']['Rows'][1:]:  # Skip header
            print([col.get('VarCharValue', '') for col in row['Data']])
    else:
        print("No data or query failed.")
