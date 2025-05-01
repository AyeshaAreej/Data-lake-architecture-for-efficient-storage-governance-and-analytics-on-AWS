# AWS Data Lake Architecture

## Project Purpose
This project demonstrates the design and implementation of a cloud-native data lake using AWS services. It covers data ingestion, storage, cataloging, querying, and visualization, all within AWS Free Tier limits.

## Overview
- Designed a scalable and secure data lake architecture.
- Set up data ingestion pipelines and cataloging with AWS Glue.
- Managed data governance using AWS Lake Formation.
- Queried datasets using Amazon Athena.
- Visualized insights with AWS QuickSight.

## Tools & Services
- Amazon S3
- AWS Glue (Crawlers & Data Catalog)
- AWS Lake Formation
- Amazon Athena
- IAM (Identity and Access Management)
- AWS QuickSight (optional for visualization)

## Implementation Steps
### 1. Architecture Design
- Defined a use case and designed the architecture using S3, Glue, Lake Formation, and Athena.
- Created an architecture diagram illustrating the data flow.

### 2. Data Ingestion & Storage
- Collected and uploaded a small public dataset (<5GB) into S3 buckets.
- Structured S3 folders into `raw/`, `processed/`, and `curated/` zones.

### 3. Cataloging & Governance
- Registered S3 locations with AWS Lake Formation.
- Created databases and tables using AWS Glue Crawlers.
- Configured access permissions for data governance using Lake Formation and IAM policies.

### 4. Querying & Analysis
- Executed SQL queries against the datasets using Amazon Athena.
- Exported query results for offline analysis.
- Visualized key insights using AWS QuickSight dashboards.

### 5. Python-Based Athena Interface
- This Python script automates the execution of multiple SQL queries on Amazon Athena using the boto3 SDK. It:
- Retrieves data from an S3-based dataset.
- Handles query execution and status polling.
- Prints results to the console or saves them.
- Loads environment variables and configuration from external files for flexibility.
- Supports modular logging and structured output handling.
The code is pushed to the GitHub repository for this assignment.

### 6. Documentation
- Captured the full setup process, key configurations, SQL queries, and insights.
