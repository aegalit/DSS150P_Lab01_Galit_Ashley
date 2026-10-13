# Source Inventory

This inventory lists the five source systems supplied for Laboratory Activity 1. Values marked "unknown" were not provided with the laboratory materials and need confirmation from the source owner.

## 1. customers.csv

| Field | Value |
|---|---|
| Source name | customers.csv |
| Source-system type | File export stored in data/raw/ |
| Data format | CSV |
| Structured / semi-structured / unstructured | Structured (flat table with 7 columns) |
| Expected update pattern | Unknown, requires source owner confirmation. A periodic batch export is assumed. |
| Likely acquisition method | Batch file read with pandas.read_csv from a file drop or scheduled export |
| Schema location or schema owner | No schema file was supplied. The schema is inferred from the header row. Owner unknown, requires confirmation. |
| Possible primary/business key | customer_id. It is not unique in the current file (247 distinct values in 250 rows). |
| Potential schema-evolution risk | CSV carries no type information, so a renamed, added or reordered column would not be detected by the format itself, and types must be assigned by the reader. |
| Potential data-quality risk | Duplicate customer_id values (2 exact duplicate rows and one ID with conflicting records), missing email in 3 rows, missing city in 2 rows, and repeated email values across different customers. |

## 2. orders.json

| Field | Value |
|---|---|
| Source name | orders.json |
| Source-system type | File export stored in data/raw/ |
| Data format | JSON (list of order objects) |
| Structured / semi-structured / unstructured | Semi-structured (the shipping field is a nested object) |
| Expected update pattern | Unknown, requires source owner confirmation. A batch export of orders is assumed. |
| Likely acquisition method | Batch file read with pandas.read_json or the json module, followed by flattening of the shipping field |
| Schema location or schema owner | No schema file was supplied. The structure is inferred from the records. Owner unknown, requires confirmation. |
| Possible primary/business key | order_id (complete and unique across 250 rows) |
| Potential schema-evolution risk | The nested shipping object may gain or lose keys without notice, and new nested fields would not appear as columns until the pipeline flattens them. |
| Potential data-quality risk | Five orders refer to customer IDs that are not in customers.csv (C0221, C0222, C0223), order_timestamp has no time zone, and 40 cancelled orders still carry positive amounts. |

## 3. products.parquet

| Field | Value |
|---|---|
| Source name | products.parquet |
| Source-system type | File export stored in data/raw/ |
| Data format | Parquet |
| Structured / semi-structured / unstructured | Structured (typed columnar table with 7 columns) |
| Expected update pattern | Unknown, requires source owner confirmation. A batch export of the product catalog is assumed. |
| Likely acquisition method | Batch file read with pandas.read_parquet using pyarrow |
| Schema location or schema owner | The schema is embedded in the Parquet file metadata. Owner unknown, requires confirmation. |
| Possible primary/business key | product_id (complete and unique across 200 rows) |
| Potential schema-evolution risk | The embedded schema makes changes detectable, but a changed column type (for example int32 to int64, or float to decimal) could break a loader or a target table. |
| Potential data-quality risk | No missing or duplicated rows were found. unit_price is stored as a floating point number, which can cause rounding problems, and one product has a stock quantity of 0. |

## 4. REST API (JSONPlaceholder posts)

| Field | Value |
|---|---|
| Source name | JSONPlaceholder posts endpoint, https://jsonplaceholder.typicode.com/posts |
| Source-system type | Web API (REST over HTTP) |
| Data format | JSON |
| Structured / semi-structured / unstructured | Semi-structured (a JSON list of objects) |
| Expected update pattern | Unknown, requires confirmation. The service is a public demonstration API, so it does not represent live business data. |
| Likely acquisition method | HTTP GET with the requests library and a 20-second timeout, saved as a raw snapshot in data/raw/api_snapshot.json |
| Schema location or schema owner | No schema or API contract was supplied. The provider of the public API is the owner, and the structure is inferred from the response. |
| Possible primary/business key | id |
| Potential schema-evolution risk | Without a versioned contract, the provider could change field names, types or the response structure without notice. |
| Potential data-quality risk | The API may time out, be unavailable or be rate limited, and the snapshot is only a copy from one point in time. |

Retrieval details from src/inspect_api.py:

- retrieved_at_utc: 2026-10-13T19:34:21.068153+00:00
- HTTP status: 200
- Content-Type: application/json; charset=utf-8
- Top-level structure: list with 100 records
- Sample record fields: userId, id, title, body

## 5. PostgreSQL table support_tickets

| Field | Value |
|---|---|
| Source name | support_tickets (schema public, database dss150p_lab) |
| Source-system type | Relational database, PostgreSQL 16 running in Docker (host port 5433) |
| Data format | SQL table with typed columns |
| Structured / semi-structured / unstructured | Structured |
| Expected update pattern | Unknown, requires confirmation. Rows are likely to change over time, because open tickets later receive a resolved_at value. |
| Likely acquisition method | SQL SELECT queries through SQLAlchemy or psycopg2, either as a full extract or incrementally by ticket_id or opened_at |
| Schema location or schema owner | The schema is defined by the instructor-supplied file sql/seed_support_tickets.sql and can be read from information_schema. Owner of the real system is unknown, requires confirmation. |
| Possible primary/business key | ticket_id (integer, enforced by a PRIMARY KEY constraint, 250 rows) |
| Potential schema-evolution risk | Changes to column types or to the length limits of the VARCHAR columns (priority 10, category 40, assigned_agent 80) could break loaders. The seed file also drops and recreates the table. |
| Potential data-quality risk | assigned_agent is missing in 4 tickets, resolved_at is empty for all 125 tickets with status Open or In Progress, so the meaning of null depends on status, and no foreign key links customer_id to a customers table. |

Table metadata from sql/inspect_support_tickets.sql (full output in data/evidence/postgres_inspection.txt):

| Column | SQL data type | Nullable |
|---|---|---|
| ticket_id | integer | NO |
| customer_id | character varying | NO |
| category | character varying | NO |
| priority | character varying | NO |
| assigned_agent | character varying | YES |
| opened_at | timestamp without time zone | NO |
| resolved_at | timestamp without time zone | YES |
| status | character varying | NO |

Constraints: PRIMARY KEY on ticket_id (support_tickets_pkey). Row count: 250.