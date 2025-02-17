import argparse

from loader import load_sqlite_db
from metrics import compute_metrics

def main():
    parser = argparse.ArgumentParser(description="SQLite DB Info CLI")
    parser.add_argument('--input', required=True, help="Path to the SQLite database file")
    parser.add_argument('--format', choices=['text', 'json'], default='text', help="Output format")
    args = parser.parse_args()

    db_path = args.input
    # Load all tables from the SQLite database
    data = load_sqlite_db(db_path)
    
    report = {}
    for table, df in data.items():
        metrics = compute_metrics(df)
        report[table] = metrics

    # Output the report in the selected format
    if args.format == 'text':
        for table, metrics in report.items():
            print(f"Table: {table}")
            print("-" * (len(table) + 7))
            print(f"Total Rows: {metrics['row_count']}")
            print("Columns:")
            for col, dtype in metrics['datatypes'].items():
                null_pct = metrics['null_percentages'][col]
                print(f"  - {col}: {dtype} (Null%: {null_pct:.2f}%)")
            print(f"Duplicate Rows: {metrics['duplicate_percentage']:.2f}%")
            print()
    else:
        import json
        print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()

