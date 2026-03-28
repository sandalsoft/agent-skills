#!/usr/bin/env python3
"""
PostgreSQL Data Insertion Tool

Loads CSV files into PostgreSQL tables with referential integrity validation.
"""

import argparse
import csv
import json
import psycopg2
from psycopg2 import sql
from pathlib import Path
from typing import Dict, List
import sys


class PostgreSQLDataLoader:
    """Load CSV data into PostgreSQL with validation."""
    
    def __init__(self, schema_path: str, csv_dir: str, 
                 db_host: str, db_name: str, db_user: str, db_password: str, db_port: int = 5432):
        
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        
        self.csv_dir = Path(csv_dir)
        
        # Connect to PostgreSQL
        try:
            self.conn = psycopg2.connect(
                host=db_host,
                database=db_name,
                user=db_user,
                password=db_password,
                port=db_port
            )
            self.cursor = self.conn.cursor()
            print(f"✅ Connected to PostgreSQL: {db_name}@{db_host}")
        except psycopg2.Error as e:
            print(f"❌ Failed to connect to PostgreSQL: {e}")
            sys.exit(1)
    
    def load_all_tables(self, batch_size: int = 10000):
        """Load all CSV files into their respective tables."""
        print("\n🚀 Starting data load...")
        
        # Determine load order (respect foreign keys)
        table_order = self._determine_load_order()
        
        # Disable foreign key checks temporarily for faster loading
        print("  ⚡ Temporarily disabling triggers for faster loading...")
        self._disable_triggers()
        
        total_rows = 0
        for table_name in table_order:
            csv_file = self.csv_dir / f"{table_name}.csv"
            
            if not csv_file.exists():
                print(f"  ⚠️  Skipping {table_name} - CSV file not found")
                continue
            
            rows_loaded = self.load_table(table_name, csv_file, batch_size)
            total_rows += rows_loaded
        
        # Re-enable foreign key checks
        print("  ⚡ Re-enabling triggers...")
        self._enable_triggers()
        
        # Validate referential integrity
        print("\n🔍 Validating referential integrity...")
        if self.validate_referential_integrity():
            print("  ✅ All foreign key constraints satisfied!")
        else:
            print("  ❌ Referential integrity violations found!")
            return False
        
        print(f"\n✅ Data load complete! Total rows inserted: {total_rows:,}")
        return True
    
    def load_table(self, table_name: str, csv_file: Path, batch_size: int = 10000) -> int:
        """Load a single CSV file into a table."""
        print(f"\n📊 Loading {table_name}...")
        
        table_def = self.schema['tables'][table_name]
        columns = list(table_def['columns'].keys())
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                rows = []
                total_rows = 0
                
                for row in reader:
                    # Convert None strings to actual None
                    processed_row = tuple(
                        None if val == '' or val == 'None' else val 
                        for val in (row.get(col) for col in columns)
                    )
                    rows.append(processed_row)
                    
                    # Batch insert
                    if len(rows) >= batch_size:
                        self._insert_batch(table_name, columns, rows)
                        total_rows += len(rows)
                        print(f"  Inserted {total_rows:,} rows...", end='\r')
                        rows = []
                
                # Insert remaining rows
                if rows:
                    self._insert_batch(table_name, columns, rows)
                    total_rows += len(rows)
                
                print(f"  ✅ Loaded {total_rows:,} rows into {table_name}")
                return total_rows
                
        except Exception as e:
            print(f"  ❌ Error loading {table_name}: {e}")
            self.conn.rollback()
            return 0
    
    def _insert_batch(self, table_name: str, columns: List[str], rows: List[tuple]):
        """Insert a batch of rows using COPY for performance."""
        try:
            # Use COPY for much faster bulk inserts
            cols = ', '.join(columns)
            
            # Create a temporary in-memory file for COPY
            import io
            buffer = io.StringIO()
            for row in rows:
                # Format row for COPY (tab-separated, \N for NULL)
                formatted_row = '\t'.join(
                    '\\N' if val is None else str(val).replace('\t', ' ').replace('\n', ' ')
                    for val in row
                )
                buffer.write(formatted_row + '\n')
            
            buffer.seek(0)
            
            # Execute COPY command
            self.cursor.copy_from(
                buffer,
                table_name,
                columns=columns,
                null='\\N'
            )
            self.conn.commit()
            
        except Exception as e:
            # Fallback to individual INSERTs if COPY fails
            print(f"    COPY failed, falling back to INSERT: {e}")
            self._insert_batch_fallback(table_name, columns, rows)
    
    def _insert_batch_fallback(self, table_name: str, columns: List[str], rows: List[tuple]):
        """Fallback: Insert rows using individual INSERT statements."""
        placeholders = ', '.join(['%s'] * len(columns))
        cols = ', '.join(columns)
        
        insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        
        try:
            self.cursor.executemany(insert_query, rows)
            self.conn.commit()
        except Exception as e:
            print(f"    ❌ Batch insert failed: {e}")
            self.conn.rollback()
            raise
    
    def validate_referential_integrity(self) -> bool:
        """Validate that all foreign key constraints are satisfied."""
        violations = []
        
        for table_name, table_def in self.schema['tables'].items():
            for col_name, col_def in table_def['columns'].items():
                if 'foreign_key' in col_def:
                    ref_table, ref_column = col_def['foreign_key'].split('.')
                    
                    # Check for orphaned records
                    query = f"""
                        SELECT COUNT(*)
                        FROM {table_name} t
                        WHERE t.{col_name} IS NOT NULL
                        AND NOT EXISTS (
                            SELECT 1 FROM {ref_table} r
                            WHERE r.{ref_column} = t.{col_name}
                        )
                    """
                    
                    self.cursor.execute(query)
                    orphan_count = self.cursor.fetchone()[0]
                    
                    if orphan_count > 0:
                        violations.append({
                            'table': table_name,
                            'column': col_name,
                            'references': f"{ref_table}.{ref_column}",
                            'orphan_count': orphan_count
                        })
        
        if violations:
            print("  ❌ Referential integrity violations found:")
            for v in violations:
                print(f"    - {v['table']}.{v['column']} -> {v['references']}: "
                      f"{v['orphan_count']} orphaned records")
            return False
        
        return True
    
    def _disable_triggers(self):
        """Disable triggers for faster bulk loading."""
        try:
            # This requires superuser privileges
            self.cursor.execute("SET session_replication_role = replica;")
            self.conn.commit()
        except Exception as e:
            print(f"  ⚠️  Could not disable triggers (may need superuser): {e}")
            self.conn.rollback()
    
    def _enable_triggers(self):
        """Re-enable triggers after bulk loading."""
        try:
            self.cursor.execute("SET session_replication_role = DEFAULT;")
            self.conn.commit()
        except Exception as e:
            print(f"  ⚠️  Could not re-enable triggers: {e}")
            self.conn.rollback()
    
    def _determine_load_order(self) -> List[str]:
        """Determine table load order based on foreign key dependencies."""
        tables = self.schema['tables']
        order = []
        remaining = set(tables.keys())
        
        while remaining:
            ready = []
            for table in remaining:
                deps = self._get_table_dependencies(table)
                if all(dep in order or dep == table for dep in deps):
                    ready.append(table)
            
            if not ready:
                # Circular dependency - add all remaining
                # Foreign keys will be validated after all data is loaded
                ready = list(remaining)
            
            order.extend(ready)
            remaining -= set(ready)
        
        return order
    
    def _get_table_dependencies(self, table_name: str) -> set:
        """Get tables that this table depends on via foreign keys."""
        deps = set()
        table_def = self.schema['tables'][table_name]
        
        for col_def in table_def['columns'].values():
            if 'foreign_key' in col_def:
                ref_table = col_def['foreign_key'].split('.')[0]
                deps.add(ref_table)
        
        return deps
    
    def get_table_stats(self):
        """Print statistics for all loaded tables."""
        print("\n📊 Table Statistics:")
        print("-" * 60)
        
        for table_name in self.schema['tables'].keys():
            try:
                self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = self.cursor.fetchone()[0]
                print(f"  {table_name:.<40} {count:>10,} rows")
            except Exception as e:
                print(f"  {table_name:.<40} {'ERROR':>10}")
        
        print("-" * 60)
    
    def close(self):
        """Close database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("\n👋 Database connection closed")


def main():
    parser = argparse.ArgumentParser(description='Load CSV data into PostgreSQL')
    parser.add_argument('schema', help='Path to schema JSON file')
    parser.add_argument('csv_dir', help='Directory containing CSV files')
    parser.add_argument('--host', default='localhost', help='PostgreSQL host')
    parser.add_argument('--port', type=int, default=5432, help='PostgreSQL port')
    parser.add_argument('--database', '-d', required=True, help='Database name')
    parser.add_argument('--user', '-U', required=True, help='Database user')
    parser.add_argument('--password', '-W', help='Database password')
    parser.add_argument('--batch-size', type=int, default=10000, 
                        help='Batch size for inserts (default: 10000)')
    parser.add_argument('--stats', action='store_true', 
                        help='Show table statistics after loading')
    
    args = parser.parse_args()
    
    # Prompt for password if not provided
    password = args.password
    if not password:
        import getpass
        password = getpass.getpass('Database password: ')
    
    # Create loader and load data
    loader = PostgreSQLDataLoader(
        schema_path=args.schema,
        csv_dir=args.csv_dir,
        db_host=args.host,
        db_name=args.database,
        db_user=args.user,
        db_password=password,
        db_port=args.port
    )
    
    try:
        success = loader.load_all_tables(batch_size=args.batch_size)
        
        if args.stats or success:
            loader.get_table_stats()
        
        loader.close()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Load interrupted by user")
        loader.close()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        loader.close()
        sys.exit(1)


if __name__ == '__main__':
    main()
