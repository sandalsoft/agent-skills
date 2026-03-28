#!/usr/bin/env python3
"""
Load coherent banking data into PostgreSQL database.

Usage:
    export DATABASE_URL="postgresql://user:password@host:port/database"
    python load_data.py

Or:
    DATABASE_URL="postgresql://user:password@host:port/database" python load_data.py
"""

import os
import sys
import csv
from pathlib import Path
from urllib.parse import urlparse
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch


def parse_database_url(url: str) -> dict:
    """Parse DATABASE_URL into connection parameters."""
    parsed = urlparse(url)

    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path[1:],  # Remove leading slash
        'user': parsed.username,
        'password': parsed.password,
    }


def get_table_order():
    """
    Return tables in dependency order (parents before children).
    This ensures foreign key constraints are satisfied during loading.
    """
    return [
        'customers',
        'accounts',
        'loans',
        'wealth_management_accounts',
        'cards',
        'card_transactions',
        'wire_transfers',
        'bill_payments',
        'investment_transactions',
        'atm_transactions',
        'loan_payments',
    ]


def load_csv_file(conn, table_name: str, csv_path: Path, batch_size: int = 1000):
    """Load a CSV file into a PostgreSQL table using COPY or batch INSERT."""
    cursor = conn.cursor()

    print(f"\n📊 Loading {table_name}...")

    # Read CSV file
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            print(f"   ⚠️  No data in {csv_path.name}")
            return

        columns = list(rows[0].keys())
        total_rows = len(rows)

        # Try COPY first (fastest method)
        try:
            # Reset file pointer
            f.seek(0)
            # Skip header
            next(f)

            # Use COPY for bulk loading
            cursor.copy_expert(
                sql.SQL("COPY {} ({}) FROM STDIN WITH CSV").format(
                    sql.Identifier(table_name),
                    sql.SQL(', ').join(map(sql.Identifier, columns))
                ),
                f
            )
            conn.commit()
            print(f"   ✅ Loaded {total_rows:,} rows using COPY")
            return

        except Exception as e:
            print(f"   ⚠️  COPY failed ({str(e)[:50]}...), falling back to INSERT")
            conn.rollback()

            # Fall back to batch INSERT
            try:
                # Convert None strings to actual None
                processed_rows = []
                for row in rows:
                    processed_row = {}
                    for key, value in row.items():
                        if value == '' or value is None:
                            processed_row[key] = None
                        else:
                            processed_row[key] = value
                    processed_rows.append(processed_row)

                # Build INSERT statement
                insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(', ').join(map(sql.Identifier, columns)),
                    sql.SQL(', ').join(sql.Placeholder() * len(columns))
                )

                # Execute in batches
                loaded = 0
                for i in range(0, len(processed_rows), batch_size):
                    batch = processed_rows[i:i + batch_size]
                    batch_values = [[row[col] for col in columns] for row in batch]

                    execute_batch(cursor, insert_query, batch_values, page_size=batch_size)
                    loaded += len(batch)

                    if loaded % 10000 == 0:
                        print(f"   Loaded {loaded:,}/{total_rows:,} rows...")

                conn.commit()
                print(f"   ✅ Loaded {total_rows:,} rows using batch INSERT")

            except Exception as e:
                conn.rollback()
                print(f"   ❌ Failed to load {table_name}: {str(e)}")
                raise


def validate_data(conn):
    """Run validation queries to check data integrity."""
    cursor = conn.cursor()

    print("\n🔍 Validating data integrity...")

    # Check row counts
    tables = get_table_order()
    print("\nRow counts:")
    total_rows = 0
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        total_rows += count
        print(f"   {table}: {count:,} rows")

    print(f"\nTotal rows loaded: {total_rows:,}")

    # Check referential integrity
    print("\nReferential integrity checks:")

    # Accounts -> Customers
    cursor.execute("""
        SELECT COUNT(*)
        FROM accounts a
        LEFT JOIN customers c ON a.customer_id = c.customer_id
        WHERE c.customer_id IS NULL
    """)
    orphaned = cursor.fetchone()[0]
    if orphaned == 0:
        print(f"   ✅ Accounts -> Customers: All valid")
    else:
        print(f"   ❌ Accounts -> Customers: {orphaned} orphaned records")

    # Cards -> Customers
    cursor.execute("""
        SELECT COUNT(*)
        FROM cards c
        LEFT JOIN customers cu ON c.customer_id = cu.customer_id
        WHERE cu.customer_id IS NULL
    """)
    orphaned = cursor.fetchone()[0]
    if orphaned == 0:
        print(f"   ✅ Cards -> Customers: All valid")
    else:
        print(f"   ❌ Cards -> Customers: {orphaned} orphaned records")

    # Card Transactions -> Cards
    cursor.execute("""
        SELECT COUNT(*)
        FROM card_transactions ct
        LEFT JOIN cards c ON ct.card_id = c.card_id
        WHERE c.card_id IS NULL
    """)
    orphaned = cursor.fetchone()[0]
    if orphaned == 0:
        print(f"   ✅ Card Transactions -> Cards: All valid")
    else:
        print(f"   ❌ Card Transactions -> Cards: {orphaned} orphaned records")

    # Sample data check
    print("\nSample data (first customer):")
    cursor.execute("""
        SELECT customer_id, customer_type, first_name, last_name, email, city, state
        FROM customers
        LIMIT 1
    """)
    row = cursor.fetchone()
    if row:
        print(f"   ID: {row[0]}")
        print(f"   Type: {row[1]}")
        print(f"   Name: {row[2]} {row[3]}")
        print(f"   Email: {row[4]}")
        print(f"   Location: {row[5]}, {row[6]}")


def main():
    # Get DATABASE_URL from environment
    database_url = os.environ.get('DATABASE_URL')

    if not database_url:
        print("❌ Error: DATABASE_URL environment variable not set")
        print("\nUsage:")
        print('  export DATABASE_URL="postgresql://user:password@host:port/database"')
        print("  python load_data.py")
        print("\nOr:")
        print('  DATABASE_URL="postgresql://user:password@host:port/database" python load_data.py')
        sys.exit(1)

    # Parse connection parameters
    try:
        conn_params = parse_database_url(database_url)
        print(f"🔗 Connecting to PostgreSQL...")
        print(f"   Host: {conn_params['host']}")
        print(f"   Port: {conn_params['port']}")
        print(f"   Database: {conn_params['database']}")
        print(f"   User: {conn_params['user']}")
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        sys.exit(1)

    # Connect to database
    try:
        conn = psycopg2.connect(**conn_params)
        print("   ✅ Connected successfully")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)

    # Set path to data directory
    data_dir = Path(__file__).parent / 'coherent_data'

    if not data_dir.exists():
        print(f"❌ Error: Data directory not found: {data_dir}")
        sys.exit(1)

    print(f"\n📁 Data directory: {data_dir}")

    try:
        # Disable user triggers temporarily for faster loading
        # Note: We can't disable system triggers (foreign key constraints) without superuser
        cursor = conn.cursor()
        print("\n⚙️  Disabling user triggers for faster loading...")

        tables = get_table_order()
        for table in tables:
            try:
                cursor.execute(f"ALTER TABLE {table} DISABLE TRIGGER USER")
                conn.commit()
            except Exception as e:
                # If we can't disable triggers, that's okay - just continue
                print(f"   Note: Could not disable triggers on {table} (continuing anyway)")
                conn.rollback()

        # Load each table in dependency order
        print("\n🚀 Starting data load...")

        for table_name in tables:
            csv_file = data_dir / f"{table_name}.csv"

            if not csv_file.exists():
                print(f"   ⚠️  Warning: {csv_file.name} not found, skipping")
                continue

            load_csv_file(conn, table_name, csv_file)

        # Re-enable user triggers
        print("\n⚙️  Re-enabling user triggers...")
        for table in tables:
            try:
                cursor.execute(f"ALTER TABLE {table} ENABLE TRIGGER USER")
                conn.commit()
            except Exception as e:
                # If we couldn't disable them, we don't need to enable them
                conn.rollback()

        # Validate data
        validate_data(conn)

        # Update sequences for auto-incrementing columns (if any)
        print("\n⚙️  Updating sequences...")
        # Note: This schema uses UUIDs, so no sequences to update
        print("   (Schema uses UUIDs, no sequences to update)")

        print("\n✅ Data load complete!")

    except Exception as e:
        print(f"\n❌ Error during data load: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            print("\n🔌 Database connection closed")


if __name__ == '__main__':
    main()
