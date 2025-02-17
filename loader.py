import sqlite3

import polars as pl

def get_table_names(db_path):
    """Return a list of table names in the SQLite database."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
    return tables

def load_sqlite_db(db_path):
    """
    Load all tables from a SQLite database into a dictionary of Polars DataFrames.
    
    Args:
        db_path (str): Path to the SQLite database file.
        
    Returns:
        dict: Mapping of table name to Polars DataFrame.
    """
    tables = get_table_names(db_path)
    data = {}
    for table in tables:
        query = f"SELECT * FROM {table}"
        try:
            # Try using Polars' built-in read_database
            df = pl.read_database(query, db_path)
        except Exception as e:
            # Fallback: use sqlite3 and pandas to load data, then convert to Polars
            import pandas as pd
            with sqlite3.connect(db_path) as conn:
                pdf = pd.read_sql(query, conn)
            df = pl.from_pandas(pdf)
        data[table] = df
    return data

