#!/usr/bin/env python3
"""
PostgreSQL Schema Creator

Generates CREATE TABLE statements with proper constraints, indices,
primary keys, and foreign keys from schema definition.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Set


class PostgreSQLSchemaGenerator:
    """Generate PostgreSQL DDL from schema definition."""
    
    def __init__(self, schema_path: str):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        
        self.type_mapping = {
            'uuid': 'UUID',
            'varchar': 'VARCHAR',
            'char': 'CHAR',
            'text': 'TEXT',
            'int': 'INTEGER',
            'integer': 'INTEGER',
            'smallint': 'SMALLINT',
            'bigint': 'BIGINT',
            'numeric': 'NUMERIC',
            'decimal': 'DECIMAL',
            'float': 'REAL',
            'double': 'DOUBLE PRECISION',
            'boolean': 'BOOLEAN',
            'bool': 'BOOLEAN',
            'date': 'DATE',
            'timestamp': 'TIMESTAMP',
            'datetime': 'TIMESTAMP',
            'time': 'TIME',
            'json': 'JSONB',
            'jsonb': 'JSONB'
        }
    
    def generate_ddl(self) -> str:
        """Generate complete DDL script."""
        ddl_parts = []
        
        # Add header
        ddl_parts.append(self._generate_header())
        
        # Determine table creation order (respecting foreign keys)
        table_order = self._determine_creation_order()
        
        # Generate CREATE TABLE statements
        for table_name in table_order:
            ddl_parts.append(self._generate_create_table(table_name))
        
        # Generate indices
        ddl_parts.append(self._generate_indices())
        
        # Generate foreign keys (added after all tables exist)
        ddl_parts.append(self._generate_foreign_keys())
        
        # Add footer with helpful comments
        ddl_parts.append(self._generate_footer())
        
        return '\n\n'.join(filter(None, ddl_parts))
    
    def _generate_header(self) -> str:
        """Generate SQL script header."""
        return f"""-- Generated PostgreSQL Schema
-- Schema Version: {self.schema.get('schema_version', 'unknown')}
-- Description: {self.schema.get('description', 'No description')}
-- Generated: {Path(__file__).name}

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop existing tables (careful in production!)
-- Uncomment the following lines if you want to recreate tables
-- DROP TABLE IF EXISTS {', '.join(self.schema['tables'].keys())} CASCADE;
"""
    
    def _generate_create_table(self, table_name: str) -> str:
        """Generate CREATE TABLE statement for a single table."""
        table_def = self.schema['tables'][table_name]
        
        lines = [f"-- {table_def.get('description', table_name)}"]
        lines.append(f"CREATE TABLE {table_name} (")
        
        column_defs = []
        primary_keys = []
        unique_constraints = []
        check_constraints = []
        
        for col_name, col_def in table_def['columns'].items():
            col_parts = [f"    {col_name}"]
            
            # Data type
            col_type = self._map_type(col_def['type'])
            col_parts.append(col_type)
            
            # Primary key
            if col_def.get('primary_key'):
                primary_keys.append(col_name)
            
            # Nullable
            if not col_def.get('nullable', True):
                col_parts.append('NOT NULL')
            
            # Unique
            if col_def.get('unique'):
                unique_constraints.append(col_name)
            
            # Default value
            if 'default' in col_def:
                default_val = col_def['default']
                if default_val == 'now()':
                    col_parts.append('DEFAULT NOW()')
                elif isinstance(default_val, str):
                    col_parts.append(f"DEFAULT '{default_val}'")
                else:
                    col_parts.append(f"DEFAULT {default_val}")
            
            # Check constraints for enum-like values
            if 'values' in col_def:
                values_str = "', '".join(col_def['values'])
                check_name = f"chk_{table_name}_{col_name}"
                check_constraints.append(
                    f"    CONSTRAINT {check_name} CHECK ({col_name} IN ('{values_str}'))"
                )
            
            column_defs.append(' '.join(col_parts))
        
        # Add all column definitions
        lines.append(',\n'.join(column_defs))
        
        # Add primary key constraint
        if primary_keys:
            pk_name = f"pk_{table_name}"
            pk_cols = ', '.join(primary_keys)
            lines.append(f",\n    CONSTRAINT {pk_name} PRIMARY KEY ({pk_cols})")
        
        # Add unique constraints
        for unique_col in unique_constraints:
            unique_name = f"uq_{table_name}_{unique_col}"
            lines.append(f",\n    CONSTRAINT {unique_name} UNIQUE ({unique_col})")
        
        # Add check constraints
        if check_constraints:
            lines.append(',\n' + ',\n'.join(check_constraints))
        
        lines.append(");")
        
        # Add table comment
        if 'description' in table_def:
            lines.append(f"COMMENT ON TABLE {table_name} IS '{table_def['description']}';")
        
        # Add column comments
        for col_name, col_def in table_def['columns'].items():
            if 'description' in col_def:
                lines.append(
                    f"COMMENT ON COLUMN {table_name}.{col_name} IS '{col_def['description']}';"
                )
        
        return '\n'.join(lines)
    
    def _generate_indices(self) -> str:
        """Generate CREATE INDEX statements."""
        lines = ["-- Indices for better query performance"]
        
        for table_name, table_def in self.schema['tables'].items():
            for col_name, col_def in table_def['columns'].items():
                # Create index on foreign key columns
                if 'foreign_key' in col_def:
                    idx_name = f"idx_{table_name}_{col_name}"
                    lines.append(f"CREATE INDEX {idx_name} ON {table_name}({col_name});")
                
                # Create index on timestamp columns (common query pattern)
                if 'timestamp' in col_def['type'].lower() or 'date' in col_def['type'].lower():
                    if not col_def.get('primary_key'):  # Don't double-index PKs
                        idx_name = f"idx_{table_name}_{col_name}"
                        lines.append(f"CREATE INDEX {idx_name} ON {table_name}({col_name});")
        
        return '\n'.join(lines) if len(lines) > 1 else ''
    
    def _generate_foreign_keys(self) -> str:
        """Generate ALTER TABLE statements for foreign keys."""
        lines = ["-- Foreign key constraints"]
        
        for table_name, table_def in self.schema['tables'].items():
            for col_name, col_def in table_def['columns'].items():
                if 'foreign_key' in col_def:
                    fk_ref = col_def['foreign_key']
                    ref_table, ref_column = fk_ref.split('.')
                    
                    fk_name = f"fk_{table_name}_{col_name}"
                    lines.append(
                        f"ALTER TABLE {table_name}\n"
                        f"    ADD CONSTRAINT {fk_name}\n"
                        f"    FOREIGN KEY ({col_name})\n"
                        f"    REFERENCES {ref_table}({ref_column})\n"
                        f"    ON DELETE CASCADE;"  # Adjust cascade behavior as needed
                    )
        
        return '\n'.join(lines) if len(lines) > 1 else ''
    
    def _generate_footer(self) -> str:
        """Generate helpful footer comments."""
        return """-- Schema creation complete!
-- 
-- Next steps:
-- 1. Review the schema and adjust constraints as needed
-- 2. Run this script: psql -U username -d database -f schema.sql
-- 3. Generate data using generate_data.py
-- 4. Load data using insert_data.py
--
-- To verify the schema:
-- \\dt          -- List all tables
-- \\d tablename -- Describe a specific table
"""
    
    def _map_type(self, type_str: str) -> str:
        """Map schema type to PostgreSQL type."""
        # Extract base type (e.g., "varchar(100)" -> "VARCHAR(100)")
        type_lower = type_str.lower()
        
        for schema_type, pg_type in self.type_mapping.items():
            if type_lower.startswith(schema_type):
                # Preserve size specifications
                if '(' in type_str:
                    size_part = type_str[type_str.index('('):]
                    return f"{pg_type}{size_part}"
                return pg_type
        
        # If not found, return as-is (might be a custom type)
        return type_str.upper()
    
    def _determine_creation_order(self) -> List[str]:
        """Determine table creation order based on foreign key dependencies."""
        tables = self.schema['tables']
        order = []
        remaining = set(tables.keys())
        
        # Iteratively add tables with resolved dependencies
        while remaining:
            ready = []
            for table in remaining:
                deps = self._get_table_dependencies(table)
                if all(dep in order or dep == table for dep in deps):
                    ready.append(table)
            
            if not ready:
                # Circular dependency - just add remaining
                # Foreign keys will be added after all tables exist
                ready = list(remaining)
            
            order.extend(ready)
            remaining -= set(ready)
        
        return order
    
    def _get_table_dependencies(self, table_name: str) -> Set[str]:
        """Get tables that this table depends on via foreign keys."""
        deps = set()
        table_def = self.schema['tables'][table_name]
        
        for col_def in table_def['columns'].values():
            if 'foreign_key' in col_def:
                ref_table = col_def['foreign_key'].split('.')[0]
                deps.add(ref_table)
        
        return deps


def main():
    parser = argparse.ArgumentParser(description='Generate PostgreSQL schema from JSON definition')
    parser.add_argument('schema', help='Path to schema JSON file')
    parser.add_argument('--output', '-o', help='Output SQL file', default='schema.sql')
    
    args = parser.parse_args()
    
    generator = PostgreSQLSchemaGenerator(args.schema)
    ddl = generator.generate_ddl()
    
    # Write to file
    output_path = Path(args.output)
    output_path.write_text(ddl)
    
    print(f"✅ PostgreSQL schema generated: {output_path}")
    print(f"📊 Tables: {len(generator.schema['tables'])}")
    print(f"\nTo create the database schema, run:")
    print(f"    psql -U username -d database -f {output_path}")


if __name__ == '__main__':
    main()
