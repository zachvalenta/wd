# design

Attempt at a CLI you can point at a single CSV or at multiple CSVs or a SQLite database and get the following info:

* foreign keys
* data quality problems e.g. this column has X percent values as string and Y percent as ints
* dupe values in a column
* columns in which all values are null | empty strings

# implementation

I'd like to do all this with Polars under the hood.

# usage

* generate sample data: `python gen.py`
* load sample data into SQLite
```sh
sqlite-utils insert db.sqlite customers data/customers.csv --csv
sqlite-utils insert db.sqlite order_items data/order_items.csv --csv
sqlite-utils insert db.sqlite orders data/orders.csv --csv
sqlite-utils insert db.sqlite products data/products.csv --csv
```
* run CLI: `python src.py`
