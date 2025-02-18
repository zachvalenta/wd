# things to use instead

* Datawrangler
* better IDE like Scripton https://news.ycombinator.com/item?id=43090214
* Visidata

# design

🧠
* https://chatgpt.com/g/g-p-67b39a5d3a24819195a762124c226bdb-wa-dong/project
* https://claude.ai/project/23a89ee8-80ea-4800-b659-ec53133f9270

Attempt at a CLI you can point at a single CSV or at multiple CSVs or a SQLite database and get the following info:

ROWS
* total
* column datatypes

RELATIONSIPS
* _PK_: list of primary keys
* _FK_: list of foreign keys, with examples from tables that they're joined to!
* _instrinsic_: cols owned by table that define its characteristics

DATA INTEGRITY
* null %
* distinct %
* dupes https://claude.ai/chat/2b1b9f45-cb54-4cd5-a435-5b65fe3af73f

# implementation

I'd like to do all this with Polars under the hood:
```python
df = pl.read_database("SELECT * FROM my_table", "path/to/db.sqlite")
```

# usage

* generate sample data: `python gen.py`
* load sample data into SQLite
```sh
sqlite-utils insert db.sqlite customers data/customers.csv --csv
sqlite-utils insert db.sqlite order_items data/order_items.csv --csv
sqlite-utils insert db.sqlite orders data/orders.csv --csv
sqlite-utils insert db.sqlite products data/products.csv --csv
```
```sh
.schema
+------------------------------+
| sql                          |
+------------------------------+
| CREATE TABLE [customers] (   |
|    [customer_id] TEXT,       |
|    [email] TEXT,             |
|    [name] TEXT,              |
|    [join_date] TEXT          |
| )                            |
| CREATE TABLE [order_items] ( |
|    [order_id] TEXT,          |
|    [product_id] TEXT,        |
|    [quantity] TEXT,          |
|    [price_at_time] TEXT      |
| )                            |
| CREATE TABLE [orders] (      |
|    [order_id] TEXT,          |
|    [customer_id] TEXT,       |
|    [order_date] TEXT,        |
|    [status] TEXT             |
| )                            |
| CREATE TABLE [products] (    |
|    [product_id] TEXT,        |
|    [name] TEXT,              |
|    [category] TEXT,          |
|    [price] TEXT              |
| )                            |
+------------------------------+
```
