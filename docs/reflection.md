# Reflection

**1. Which source would be easiest to integrate into a future pipeline, and why?**

products.parquet would be the easiest. Parquet stores the column types inside the file, so the pipeline does not need to guess them. The profile found no missing values and no duplicate rows, and product_id is unique across all 200 rows, which makes it a dependable key. The file can be read with one pandas call and needs no flattening. Its price, stock and weight columns also have clear value ranges that can be checked automatically.

**2. Which source presents the greatest schema or data-quality risk, and what evidence supports your answer?**

customers.csv presents the greatest risk. It has 250 rows but only 247 distinct customer_id values. Two IDs are exact duplicate rows, and C0090 appears twice with two different people, so the key cannot be trusted. Email is missing in 3 rows, city is missing in 2 rows, and 63 email values repeat across rows. CSV also carries no type information, so the reader must assign every type. Orders.json has the nested shipping object, but that risk is easier to handle than conflicting records.

**3. What could go wrong if a pipeline is built before the source schema and contract are understood?**

The pipeline could fail, or it could run without errors and load wrong data. A table that uses customer_id as the primary key would reject the duplicate customers, and a loader that expects flat columns would fail on the shipping object in orders.json. Five orders refer to customers that are not in customers.csv, so a join could silently drop revenue. Without a contract, nobody would know which time zone applies or whether cancelled orders count. Users of the data would then find these problems instead of the engineers.

**4. How do Git, virtual environments, containers, and documentation improve reproducibility for a data-engineering team?**

Git keeps the history of every change, so a teammate gets the same files and can see why something changed. The virtual environment and requirements.txt make everyone use the same Python packages. Docker gives every machine the same PostgreSQL 16 database and credentials. In this laboratory, another container already used port 5432 on my computer, so I mapped the lab database to port 5433 and wrote it in the README. Documentation records choices like this so another person can repeat the setup without guessing.