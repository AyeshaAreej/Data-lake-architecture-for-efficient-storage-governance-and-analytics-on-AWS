import boto3
import json
import time
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Load config
with open('config.json') as f:
    config = json.load(f)

# Boto3 Athena client
athena = boto3.client(
    'athena',
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

def run_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': config['database']},
        ResultConfiguration={'OutputLocation': config['output_location']},
        WorkGroup=config['workgroup']
    )

    query_execution_id = response['QueryExecutionId']

    # Wait for query to complete
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)

    if status == 'SUCCEEDED':
        print("Query succeeded")
        return athena.get_query_results(QueryExecutionId=query_execution_id)
    else:
        print(f"Query failed with status: {status}")
        return None

# Example query
sql = "SELECT * FROM your_table_name LIMIT 10;"
results = run_query(sql)

# Print results
if results:
    for row in results['ResultSet']['Rows'][1:]:  # Skip header
        print([col.get('VarCharValue', '') for col in row['Data']])
