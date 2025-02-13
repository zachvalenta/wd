import csv
from datetime import datetime, timedelta
from pathlib import Path

def generate_customers():
    customers = [
        ['customer_id', 'email', 'name', 'join_date'],
        [1, 'alice@example.com', 'Alice Chen', '2024-01-01'],
        [2, 'bob@example.com', 'Bob Smith', '2024-01-15'],
        [3, 'carol@example.com', 'Carol Kumar', '2024-02-01']
    ]
    return customers

def generate_products():
    products = [
        ['product_id', 'name', 'category', 'price'],
        [101, 'Widget Pro', 'gadgets', 29.99],
        [102, 'Super Widget', 'gadgets', 49.99],
        [103, 'Widget Case', 'accessories', 9.99],
        [104, 'Widget Manual', 'books', 19.99]
    ]
    return products

def generate_orders():
    orders = [
        ['order_id', 'customer_id', 'order_date', 'status'],
        [1001, 1, '2024-01-15', 'completed'],
        [1002, 1, '2024-02-01', 'completed'],
        [1003, 2, '2024-02-15', 'pending'],
        [1004, 3, '2024-02-20', 'completed']
    ]
    return orders

def generate_order_items():
    order_items = [
        ['order_id', 'product_id', 'quantity', 'price_at_time'],
        [1001, 101, 2, 29.99],
        [1001, 103, 1, 9.99],
        [1002, 102, 1, 49.99],
        [1003, 101, 1, 29.99],
        [1003, 104, 1, 19.99],
        [1004, 102, 2, 49.99]
    ]
    return order_items

def write_csv(data, filename):
    path = Path(filename)
    with path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main():
    Path.cwd().joinpath('data').mkdir(exist_ok=True)
    datasets = {
        'data/customers.csv': generate_customers(),
        'data/products.csv': generate_products(),
        'data/orders.csv': generate_orders(),
        'data/order_items.csv': generate_order_items()
    }
    
    for filename, data in datasets.items():
        write_csv(data, filename)

if __name__ == '__main__':
    main()
