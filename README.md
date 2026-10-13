# DSS150P Laboratory Activity 1: Local Data Engineering Workspace and Source Assessment

**Full Name:** GALIT, ASHLEY E.
**Student Number:** 2024106930
**Course:** DSS150P - FUNDAMENTALS OF DATA ENGINEERING, Mapua University School of Information Technology

## Purpose of the Laboratory

This laboratory prepares a reproducible local data engineering workspace and a first technical assessment of five source systems: a CSV file, a JSON file, a Parquet file, a REST API and a PostgreSQL table. The work covers environment setup, a data engineering lifecycle map, source profiling, API and database inspection, a basic PostgreSQL schema, and a data contract for orders.json.

## Software Requirements

- Python 3.x
- Git
- Docker Desktop (or Docker Engine) with Docker Compose
- Visual Studio Code or another code editor
- A terminal (PowerShell on Windows)
- Internet access for the REST API and for installing packages

Python packages (in requirements.txt): pandas, pyarrow, requests, sqlalchemy, psycopg2-binary.

## Repository Structure

```
data/raw/        customers.csv, orders.json, products.parquet, api_snapshot.json
data/evidence/   screenshots and output files
docs/            lifecycle_map.md, source_inventory.md, source_profile.md, data_contract.yaml, reflection.md
sql/             01_create_schema.sql, seed_support_tickets.sql, inspect_support_tickets.sql, inspect_lab_schema.sql
src/             verify_environment.py, profile_sources.py, inspect_api.py
docker-compose.yml, requirements.txt, .gitignore, README.md
```

## Steps to Reproduce the Environment

Commands are for Windows PowerShell and are run from the repository root.

1. Clone the repository and open the folder:
```
   git clone <https://github.com/aegalit/DSS150P_Lab01_Galit_Ashley.git>
   cd DSS150P_Lab01_Galit_Ashley
```
2. Create and activate the virtual environment:
```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
```
   On macOS or Linux use `python3 -m venv .venv` and `source .venv/bin/activate`.
3. Install the dependencies:
```
   pip install -r requirements.txt
```
4. Start PostgreSQL and confirm that the container is running:
```
   docker compose up -d
   docker ps
```
5. Load the instructor-provided sample table (support_tickets):
```
   Get-Content sql\seed_support_tickets.sql -Raw | docker exec -i dss150p-postgres psql -U dss150p -d dss150p_lab
```
   On macOS or Linux: `docker exec -i dss150p-postgres psql -U dss150p -d dss150p_lab < sql/seed_support_tickets.sql`
6. Create the lab schema and the orders table:
```
   Get-Content sql\01_create_schema.sql -Raw | docker exec -i dss150p-postgres psql -U dss150p -d dss150p_lab
```

The database is published on host port 5433 instead of 5432, because port 5432 was already used by another PostgreSQL container on the development computer. Connection settings: host localhost, port 5433, database dss150p_lab, user dss150p, password dss150p_lab. These credentials are for local development only.

## Start and Stop PostgreSQL

- Start: `docker compose up -d`
- Check status: `docker ps`
- Stop (keeps the data): `docker compose stop`
- Start again after stopping: `docker compose start`
- Remove the container but keep the data volume: `docker compose down`
- Remove the container and delete the data volume: `docker compose down -v`

## How to Run Each Script

Activate the virtual environment first. Run all scripts from the repository root.

- `python src\verify_environment.py` connects to PostgreSQL and prints the version and the current database.
- `python src\profile_sources.py` profiles customers.csv, orders.json and products.parquet. It prints the profile and saves it to data/evidence/profile_report.txt.
- `python src\inspect_api.py` requests the REST API, prints the status, content type, structure, record count and a sample record, and saves the response to data/raw/api_snapshot.json. It prints the retrieval time in UTC. An optional URL can be given as the first argument.

The SQL files in sql/ are run with the same `Get-Content ... | docker exec -i ...` pattern shown above. The files inspect_support_tickets.sql and inspect_lab_schema.sql only read metadata.

## Description of Each Source

- **customers.csv:** CSV file with 250 rows and 7 columns about customers. It has duplicate customer_id values and some missing email and city values.
- **orders.json:** JSON file with 250 orders and 9 fields. The shipping field is a nested object with region and method. order_id is unique. This is the source selected for the data contract and the lab.orders table.
- **products.parquet:** Parquet file with 200 products and 7 typed columns. It has no missing values and a unique product_id.
- **REST API:** The public JSONPlaceholder posts endpoint (https://jsonplaceholder.typicode.com/posts). It returns a JSON list of 100 records. The snapshot is saved in data/raw/api_snapshot.json.
- **PostgreSQL table support_tickets:** Sample table with 250 support tickets, loaded from sql/seed_support_tickets.sql into the public schema. The primary key is ticket_id.

Details are in docs/source_inventory.md and docs/source_profile.md.

## Known Limitations and Unresolved Questions

- The lab.orders table is created but not loaded, because the laboratory instructions say not to bulk-load the file.
- customer_id in customers.csv is not unique, so no primary key can be defined for that source until the duplicates are resolved.
- Five orders refer to customer IDs that are not in customers.csv, and order_timestamp has no time zone.
- The owners and update schedules of the sources are unknown and need confirmation.
- The REST API is a public demonstration service, so the snapshot is only a copy from one point in time.
- PostgreSQL uses host port 5433 on the development computer. Change the port mapping in docker-compose.yml and the connection URL in src/verify_environment.py if port 5432 is free and preferred.