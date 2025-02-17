import polars as pl

def compute_metrics(df: pl.DataFrame):
    """
    Compute metrics for a given Polars DataFrame.
    
    Returns:
        dict: Metrics including row_count, datatypes, duplicate_percentage, and null_percentages.
    """
    row_count = df.height
    # Get datatypes from the DataFrame's schema
    datatypes = df.schema
    
    # Compute duplicate percentage: (total rows - unique rows) / total rows * 100
    unique_count = df.unique().height
    duplicate_percentage = ((row_count - unique_count) / row_count * 100) if row_count > 0 else 0.0
    
    # Compute null percentages per column
    null_percentages = {
        col: (df[col].is_null().sum() / row_count * 100 if row_count > 0 else 0.0)
        for col in df.columns
    }
    
    return {
        "row_count": row_count,
        "datatypes": datatypes,
        "duplicate_percentage": duplicate_percentage,
        "null_percentages": null_percentages
    }

