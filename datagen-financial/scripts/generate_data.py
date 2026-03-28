#!/usr/bin/env python3
"""
Synthetic Financial Data Generator

Generates realistic, referentially-integral financial transaction data
for credit card processing networks.
"""

import json
import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple
import argparse
import sys


class RealisticNameGenerator:
    """Generates realistic names using frequency distributions."""
    
    def __init__(self, distributions_path: str):
        with open(distributions_path, 'r') as f:
            data = json.load(f)
        
        self.male_first = data['first_names']['male']
        self.female_first = data['first_names']['female']
        self.last_names = data['last_names']
        
        # Create weighted lists for sampling
        self.male_names = self._create_weighted_list(self.male_first)
        self.female_names = self._create_weighted_list(self.female_first)
        self.surnames = self._create_weighted_list(self.last_names)
        
        # Track generated names to ensure uniqueness
        self.used_names = set()
    
    def _create_weighted_list(self, items: List[Dict]) -> List[str]:
        """Create a weighted list based on frequency."""
        weighted = []
        for item in items:
            count = max(1, int(item['frequency'] * 100))
            weighted.extend([item['name']] * count)
        return weighted
    
    def generate_unique_name(self, gender: str = None) -> Tuple[str, str]:
        """Generate a unique first and last name combination."""
        max_attempts = 1000
        for _ in range(max_attempts):
            if gender == 'male' or (gender is None and random.random() < 0.49):
                first = random.choice(self.male_names)
            else:
                first = random.choice(self.female_names)
            
            last = random.choice(self.surnames)
            full_name = f"{first} {last}"
            
            if full_name not in self.used_names:
                self.used_names.add(full_name)
                return first, last
        
        # If we can't find unique, add a middle initial
        first, last = self.generate_unique_name(gender)
        middle_initial = chr(random.randint(65, 90))
        self.used_names.add(f"{first} {middle_initial}. {last}")
        return f"{first} {middle_initial}.", last


class LocationGenerator:
    """Generates realistic US continental locations."""
    
    def __init__(self, merchant_data_path: str):
        with open(merchant_data_path, 'r') as f:
            data = json.load(f)
        
        self.cities = data['major_cities']
        self.bounds = data['us_continental_coordinates']
        
        # Create weighted city list
        self.weighted_cities = []
        for city in self.cities:
            weight = int(city['population_weight'] * 10)
            self.weighted_cities.extend([city] * weight)
    
    def generate_location(self) -> Dict[str, Any]:
        """Generate a realistic US location."""
        city_data = random.choice(self.weighted_cities)
        
        # Add some randomness around the city center
        lat_offset = random.uniform(-0.5, 0.5)
        lon_offset = random.uniform(-0.5, 0.5)
        
        return {
            'city': city_data['city'],
            'state': city_data['state'],
            'latitude': round(city_data['lat'] + lat_offset, 7),
            'longitude': round(city_data['lon'] + lon_offset, 7),
            'zip_code': self._generate_realistic_zip(city_data['state'])
        }
    
    def _generate_realistic_zip(self, state: str) -> str:
        """Generate a realistic ZIP code for a state."""
        # Simplified - real implementation would use actual ZIP ranges
        state_zip_prefixes = {
            'NY': ['100', '101', '102', '103', '104', '105'],
            'CA': ['900', '901', '902', '903', '904', '905', '906', '907', '908'],
            'TX': ['750', '751', '752', '753', '754', '755', '756', '757', '758', '759'],
            'FL': ['320', '321', '322', '323', '324', '325', '326', '327', '328', '329'],
            'IL': ['600', '601', '602', '603', '604', '605', '606', '607', '608', '609'],
            'PA': ['150', '151', '152', '153', '154', '155', '156', '157', '158', '159'],
            'OH': ['430', '431', '432', '433', '434', '435', '436', '437', '438', '439'],
            'AZ': ['850', '851', '852', '853', '854', '855', '856', '857'],
            'MA': ['010', '011', '012', '013', '014', '015', '016', '017', '018', '019'],
            'WA': ['980', '981', '982', '983', '984', '985', '986'],
        }
        prefix = random.choice(state_zip_prefixes.get(state, ['999']))
        return f"{prefix}{random.randint(10, 99)}"


class TransactionTimingValidator:
    """Ensures realistic temporal constraints on transactions."""
    
    def __init__(self, merchant_data_path: str):
        with open(merchant_data_path, 'r') as f:
            data = json.load(f)
        self.merchant_categories = {cat['mcc']: cat for cat in data['merchant_categories']}
        self.merchant_transaction_counts = {}  # Track transactions per merchant per time window
    
    def can_process_transaction(self, merchant_id: str, mcc: str, timestamp: datetime) -> bool:
        """Check if a merchant can realistically process a transaction at this time."""
        category = self.merchant_categories.get(mcc, {})
        max_per_day = category.get('transactions_per_day', [10, 1000])[1]
        
        # Create a time window key (merchant + hour)
        window_key = f"{merchant_id}_{timestamp.strftime('%Y%m%d%H')}"
        
        # Get current count for this window
        current_count = self.merchant_transaction_counts.get(window_key, 0)
        max_per_hour = max_per_day / 24  # Simplified - could be more sophisticated
        
        if current_count >= max_per_hour:
            return False
        
        self.merchant_transaction_counts[window_key] = current_count + 1
        return True
    
    def generate_realistic_timestamp(self, mcc: str, base_date: datetime) -> datetime:
        """Generate a realistic timestamp for a transaction based on merchant type."""
        category = self.merchant_categories.get(mcc, {})
        peak_hours = category.get('peak_hours', list(range(9, 18)))
        
        # 70% chance of being in peak hours
        if random.random() < 0.7 and peak_hours:
            hour = random.choice(peak_hours)
        else:
            hour = random.randint(6, 23)  # Most places open 6am-11pm
        
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        
        return base_date.replace(hour=hour, minute=minute, second=second)


class ConstraintEngine:
    """Applies user-defined business logic constraints."""
    
    def __init__(self, constraints_path: str = None):
        self.constraints = {}
        if constraints_path and Path(constraints_path).exists():
            with open(constraints_path, 'r') as f:
                self.constraints = json.load(f)
    
    def should_field_be_missing(self, table: str, field: str) -> bool:
        """Determine if a field should be missing based on data quality constraints."""
        dq_constraints = self.constraints.get('data_quality', [])
        for constraint in dq_constraints:
            if constraint.get('field') == f"{table}.{field}":
                missing_rate = constraint.get('missing_rate', 0)
                return random.random() < missing_rate
        return False
    
    def validate_relational_constraint(self, constraint_rule: str, **kwargs) -> bool:
        """Validate a relational constraint between fields."""
        # Parse and evaluate constraint rules
        # This is simplified - a full implementation would use a proper expression parser
        for constraint in self.constraints.get('relational', []):
            if constraint.get('rule') == constraint_rule:
                # Evaluate the constraint
                return eval(constraint_rule, kwargs)
        return True
    
    def apply_constraint_adjustments(self, table: str, field: str, value: Any) -> Any:
        """Apply any constraint-based adjustments to a value."""
        # Custom logic for constraint enforcement
        return value


class FinancialDataGenerator:
    """Main orchestrator for generating synthetic financial data."""

    def __init__(self, schema_path: str, output_dir: str,
                 distributions_path: str, merchant_data_path: str,
                 constraints_path: str = None,
                 corporate_domains_path: str = 'assets/corporate_domains.json'):

        with open(schema_path, 'r') as f:
            self.schema = json.load(f)

        # Set default date range to past 18 months if not specified
        if 'data_generation_period' not in self.schema or not self.schema['data_generation_period']:
            today = datetime.now()
            start_date = today - timedelta(days=548)  # 18 months ≈ 548 days
            self.schema['data_generation_period'] = {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': today.strftime('%Y-%m-%d'),
                'description': 'Default: past 18 months from execution date'
            }
            print(f"ℹ️  No date range specified. Using default: {self.schema['data_generation_period']['start_date']} to {self.schema['data_generation_period']['end_date']}")

        # Validate that all tables have row_count specified
        self._validate_row_counts()

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.name_gen = RealisticNameGenerator(distributions_path)
        self.location_gen = LocationGenerator(merchant_data_path)
        self.timing_validator = TransactionTimingValidator(merchant_data_path)
        self.constraint_engine = ConstraintEngine(constraints_path)

        # Load corporate domains
        self.corporate_domains = []
        if Path(corporate_domains_path).exists():
            with open(corporate_domains_path, 'r') as f:
                data = json.load(f)
                self.corporate_domains = data.get('domains', [])

        # Storage for generated entities (for referential integrity)
        self.entities = {}

        # Transaction flow tracking
        self.transaction_flow = {}

        # Track current cardholder context for proper customer type-aware generation
        self.current_cardholder_context = {}
    
    def _validate_row_counts(self):
        """Validate that all tables have row_count specified."""
        missing_row_counts = []
        for table_name, table_def in self.schema['tables'].items():
            if 'row_count' not in table_def:
                missing_row_counts.append(table_name)
        
        if missing_row_counts:
            print("\n❌ ERROR: row_count not specified for the following tables:")
            for table in missing_row_counts:
                print(f"   - {table}")
            print("\n💡 Please add 'row_count' to each table in your schema JSON file.")
            print("   Example:")
            print('   "your_table": {')
            print('     "description": "...",')
            print('     "row_count": 1000000,  // <-- Add this')
            print('     "columns": { ... }')
            print('   }')
            print("\nSee references/schema-format.md for more details.\n")
            sys.exit(1)
    
    def generate_all(self):
        """Generate all data according to schema."""
        print("🚀 Starting data generation...")
        
        # Generate in dependency order
        tables = self.schema['tables']
        generated_order = self._determine_generation_order(tables)
        
        for table_name in generated_order:
            print(f"📊 Generating {table_name}...")
            self.generate_table(table_name)
        
        print("✅ Data generation complete!")
        print(f"📁 Output files written to: {self.output_dir}")
    
    def _determine_generation_order(self, tables: Dict) -> List[str]:
        """Determine correct order to generate tables (respecting foreign keys)."""
        # Simple topological sort based on foreign key dependencies
        order = []
        remaining = set(tables.keys())
        
        while remaining:
            # Find tables with no unresolved dependencies
            ready = []
            for table in remaining:
                fk_refs = self._get_foreign_key_refs(tables[table])
                if all(ref.split('.')[0] in order or ref.split('.')[0] == table 
                       for ref in fk_refs):
                    ready.append(table)
            
            if not ready:
                # Circular dependency or error - just add remaining
                ready = list(remaining)
            
            order.extend(ready)
            remaining -= set(ready)
        
        return order
    
    def _get_foreign_key_refs(self, table_def: Dict) -> List[str]:
        """Extract foreign key references from table definition."""
        refs = []
        for col, col_def in table_def['columns'].items():
            if 'foreign_key' in col_def:
                refs.append(col_def['foreign_key'])
        return refs
    
    def generate_table(self, table_name: str):
        """Generate data for a specific table."""
        table_def = self.schema['tables'][table_name]
        row_count = table_def['row_count']  # No default - validated in __init__
        
        # Generate rows
        rows = []
        for i in range(row_count):
            if i % 10000 == 0 and i > 0:
                print(f"  Generated {i}/{row_count} rows...")
            
            row = self._generate_row(table_name, table_def)
            if row:
                rows.append(row)
        
        # Write to CSV
        output_file = self.output_dir / f"{table_name}.csv"
        self._write_csv(output_file, table_def['columns'].keys(), rows)
        
        # Store entities for referential integrity
        if 'primary_key' in str(table_def['columns']):
            pk_col = self._get_primary_key(table_def)
            self.entities[table_name] = [row[pk_col] for row in rows]
        
        print(f"  ✅ Generated {len(rows)} rows -> {output_file}")
    
    def _generate_row(self, table_name: str, table_def: Dict) -> Dict:
        """Generate a single row of data."""
        row = {}

        # For cardholders table, determine customer type first
        if table_name == 'cardholders':
            # 50/50 split between retail and corporate
            row['customer_type'] = 'corporate' if random.random() < 0.5 else 'retail'

        for col_name, col_def in table_def['columns'].items():
            # Skip customer_type if already set
            if col_name == 'customer_type' and 'customer_type' in row:
                continue

            # Check if field should be missing
            if col_def.get('nullable') and self.constraint_engine.should_field_be_missing(table_name, col_name):
                row[col_name] = None
                continue

            # Generate value based on type
            row[col_name] = self._generate_value(table_name, col_name, col_def, row)

        # Store cardholder context for later use with cards
        if table_name == 'cardholders' and 'cardholder_id' in row:
            pk_col = self._get_primary_key(table_def)
            if pk_col:
                self.current_cardholder_context[row[pk_col]] = {
                    'customer_type': row.get('customer_type', 'retail')
                }

        return row
    
    def _generate_value(self, table_name: str, col_name: str, col_def: Dict, row: Dict = None) -> Any:
        """Generate a single value based on column definition."""
        if row is None:
            row = {}

        col_type = col_def['type'].lower()

        # Handle foreign keys
        if 'foreign_key' in col_def:
            ref_table = col_def['foreign_key'].split('.')[0]
            if ref_table in self.entities and self.entities[ref_table]:
                return random.choice(self.entities[ref_table])
            return str(uuid.uuid4())  # Fallback

        # Handle primary keys
        if col_def.get('primary_key'):
            return str(uuid.uuid4())

        # Handle specific column types
        if 'uuid' in col_type:
            return str(uuid.uuid4())
        elif 'timestamp' in col_type or 'datetime' in col_type:
            return self._generate_timestamp(table_name, col_name)
        elif 'date' in col_type:
            # Special handling for date_of_birth
            if 'birth' in col_name.lower() or 'dob' in col_name.lower():
                return self._generate_date_of_birth()
            return self._generate_date()
        elif 'varchar' in col_type or 'char' in col_type:
            return self._generate_string(table_name, col_name, col_def, row)
        elif 'numeric' in col_type or 'decimal' in col_type:
            return self._generate_numeric(table_name, col_name, col_def, row)
        elif 'int' in col_type:
            return self._generate_integer(col_name, col_def)
        else:
            return ''
    
    def _generate_timestamp(self, table_name: str, col_name: str) -> str:
        """Generate a realistic timestamp."""
        start = datetime.strptime(self.schema.get('data_generation_period', {}).get('start_date', '2023-01-01'), '%Y-%m-%d')
        end = datetime.strptime(self.schema.get('data_generation_period', {}).get('end_date', '2024-12-31'), '%Y-%m-%d')
        
        delta = end - start
        random_days = random.randint(0, delta.days)
        base_date = start + timedelta(days=random_days)
        
        # Add time component
        timestamp = base_date + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def _generate_date(self) -> str:
        """Generate a realistic date."""
        start = datetime.strptime(self.schema.get('data_generation_period', {}).get('start_date', '2023-01-01'), '%Y-%m-%d')
        end = datetime.strptime(self.schema.get('data_generation_period', {}).get('end_date', '2024-12-31'), '%Y-%m-%d')

        delta = end - start
        random_days = random.randint(0, delta.days)
        date = start + timedelta(days=random_days)

        return date.strftime('%Y-%m-%d')

    def _generate_date_of_birth(self) -> str:
        """Generate a realistic date of birth (ages 18-85 years old).

        Banking regulations require customers to be at least 18 years old.
        Most active banking customers are under 85 years old.
        Distribution is weighted towards younger customers (25-55 age range).
        """
        today = datetime.now()

        # Age ranges with weights (more realistic distribution)
        # 18-25: 15%, 25-35: 25%, 35-45: 25%, 45-55: 20%, 55-65: 10%, 65-85: 5%
        age_ranges = [
            (18, 25, 0.15),
            (25, 35, 0.25),
            (35, 45, 0.25),
            (45, 55, 0.20),
            (55, 65, 0.10),
            (65, 85, 0.05)
        ]

        # Select age range based on weights
        rand = random.random()
        cumulative = 0
        selected_min, selected_max = 18, 85

        for min_age, max_age, weight in age_ranges:
            cumulative += weight
            if rand <= cumulative:
                selected_min, selected_max = min_age, max_age
                break

        # Generate random age within selected range
        age_years = random.randint(selected_min, selected_max)
        age_days = random.randint(0, 365)  # Additional days for more variation

        # Calculate birth date
        birth_date = today - timedelta(days=(age_years * 365 + age_days))

        return birth_date.strftime('%Y-%m-%d')
    
    def _generate_string(self, table_name: str, col_name: str, col_def: Dict, row: Dict = None) -> str:
        """Generate a realistic string value."""
        if row is None:
            row = {}

        if 'values' in col_def:
            return random.choice(col_def['values'])

        # Determine customer type for context-aware generation
        # Treat 'commercial' same as 'corporate' for email/address/national_id purposes
        customer_type = row.get('customer_type', 'retail')
        is_business = customer_type in ('corporate', 'commercial')

        # Name fields
        if 'first_name' in col_name.lower():
            first, _ = self.name_gen.generate_unique_name()
            return first
        elif 'last_name' in col_name.lower():
            _, last = self.name_gen.generate_unique_name()
            return last
        elif 'email' in col_name.lower():
            first, last = self.name_gen.generate_unique_name()

            # Corporate/Commercial customers get company email domains
            if is_business and self.corporate_domains:
                domain_data = random.choice(self.corporate_domains)
                domain = domain_data['domain']
            else:
                # Retail customers get public email providers
                domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com', 'hotmail.com', 'aol.com'])

            return f"{first.lower()}.{last.lower()}@{domain}"
        elif 'city' in col_name.lower():
            loc = self.location_gen.generate_location()
            return loc['city']
        elif 'state' in col_name.lower():
            loc = self.location_gen.generate_location()
            return loc['state']
        elif 'zip' in col_name.lower() or 'postal' in col_name.lower():
            loc = self.location_gen.generate_location()
            return loc['zip_code']
        elif 'address' in col_name.lower() and 'line1' in col_name.lower():
            # Business addresses for corporate/commercial customers
            if is_business:
                building_number = random.randint(1, 999)
                street_names = ['Corporate', 'Business', 'Commerce', 'Executive', 'Professional', 'Enterprise', 'Industry', 'Tech', 'Innovation']
                street_types = ['Plaza', 'Center', 'Park', 'Way', 'Drive', 'Parkway', 'Boulevard']
                return f"{building_number} {random.choice(street_names)} {random.choice(street_types)}"
            else:
                # Residential addresses for retail customers
                return f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Pine', 'Cedar', 'Elm', 'Park', 'Lake', 'Hill'])} {random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln', 'Ct', 'Way'])}"
        elif 'address' in col_name.lower() and 'line2' in col_name.lower():
            # Suite/Floor numbers for business addresses, apartment numbers for residential
            if is_business:
                # 60% chance of having suite/floor info
                if random.random() < 0.6:
                    suite_types = ['Suite', 'Floor', 'Ste']
                    return f"{random.choice(suite_types)} {random.randint(100, 2500)}"
            else:
                # 30% chance of having apartment number
                if random.random() < 0.3:
                    return f"Apt {random.randint(1, 999)}"
            return None  # nullable field
        elif 'phone' in col_name.lower():
            # Use realistic US area codes
            area_codes = ['212', '213', '214', '215', '216', '217', '303', '312', '313', '314', '404', '415', '469', '510', '512', '602', '612', '617', '619', '702', '703', '713', '714', '718', '720', '770', '773', '786', '817', '818', '858', '917', '972']
            return f"{random.choice(area_codes)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"
        elif 'card_number' in col_name.lower():
            # Generate valid-looking card number (not real Luhn algorithm)
            return f"{random.randint(4000, 5999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
        elif 'national_id' in col_name.lower():
            # Generate realistic national ID based on customer type
            # Corporate/Commercial: EIN (Employer Identification Number) format XX-XXXXXXX
            # Retail: SSN (Social Security Number) format XXX-XX-XXXX
            # Use reserved/invalid ranges to ensure these are clearly synthetic

            if is_business:
                # EIN format: XX-XXXXXXX
                # First two digits: 10-99 (avoiding some reserved ranges)
                first_two = random.randint(10, 99)
                remaining = random.randint(1000000, 9999999)
                return f"{first_two:02d}-{remaining:07d}"
            else:
                # SSN format: XXX-XX-XXXX
                # Use 900-999 range for Area Number (reserved for testing/advertising)
                # This ensures these are clearly NOT real SSNs
                area = random.randint(900, 999)  # Reserved test range
                group = random.randint(10, 99)
                serial = random.randint(1000, 9999)
                return f"{area:03d}-{group:02d}-{serial:04d}"
        else:
            return f"Value_{random.randint(1000, 9999)}"
    
    def _generate_numeric(self, table_name: str, col_name: str, col_def: Dict, row: Dict = None) -> float:
        """Generate a realistic numeric value."""
        if row is None:
            row = {}

        if 'amount' in col_name.lower():
            return round(random.uniform(5.00, 500.00), 2)
        elif 'fee' in col_name.lower():
            return round(random.uniform(0.50, 25.00), 2)
        elif 'limit' in col_name.lower() and 'credit' in col_name.lower():
            # Need to look up customer type from cardholder context for cards table
            cardholder_id = row.get('cardholder_id')
            customer_type = 'retail'  # default

            if cardholder_id and cardholder_id in self.current_cardholder_context:
                customer_type = self.current_cardholder_context[cardholder_id].get('customer_type', 'retail')

            # Corporate cards have much higher limits
            if customer_type == 'corporate':
                # Corporate: $10,000 - $500,000
                return round(random.uniform(10000.00, 500000.00), 2)
            else:
                # Retail: $500 - $50,000
                return round(random.uniform(500.00, 50000.00), 2)
        elif 'lat' in col_name.lower():
            loc = self.location_gen.generate_location()
            return loc['latitude']
        elif 'lon' in col_name.lower():
            loc = self.location_gen.generate_location()
            return loc['longitude']
        else:
            return round(random.uniform(0, 1000), 2)
    
    def _generate_integer(self, col_name: str, col_def: Dict) -> int:
        """Generate a realistic integer value."""
        if 'count' in col_name.lower():
            return random.randint(1, 10000)
        elif 'expiration_month' in col_name.lower() or 'exp_month' in col_name.lower():
            return random.randint(1, 12)
        elif 'expiration_year' in col_name.lower() or 'exp_year' in col_name.lower():
            # Card expiration dates should be 1-6 years from now
            current_year = datetime.now().year
            return random.randint(current_year + 1, current_year + 6)
        elif 'month' in col_name.lower():
            return random.randint(1, 12)
        elif 'year' in col_name.lower():
            # Generic year field - use current year +/- 2 years
            current_year = datetime.now().year
            return random.randint(current_year - 2, current_year + 2)
        else:
            return random.randint(0, 100)
    
    def _get_primary_key(self, table_def: Dict) -> str:
        """Get the primary key column name."""
        for col_name, col_def in table_def['columns'].items():
            if col_def.get('primary_key'):
                return col_name
        return None
    
    def _write_csv(self, file_path: Path, columns: List[str], rows: List[Dict]):
        """Write data to CSV file."""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description='Generate synthetic financial transaction data')
    parser.add_argument('schema', help='Path to schema JSON file')
    parser.add_argument('output_dir', help='Output directory for CSV files')
    parser.add_argument('--constraints', help='Path to constraints/rules JSON file', default=None)
    parser.add_argument('--distributions', help='Path to name distributions JSON',
                        default='assets/name_distributions.json')
    parser.add_argument('--merchants', help='Path to merchant types JSON',
                        default='assets/merchant_types.json')
    parser.add_argument('--corporate-domains', help='Path to corporate domains JSON',
                        default='assets/corporate_domains.json')

    args = parser.parse_args()

    generator = FinancialDataGenerator(
        schema_path=args.schema,
        output_dir=args.output_dir,
        distributions_path=args.distributions,
        merchant_data_path=args.merchants,
        constraints_path=args.constraints,
        corporate_domains_path=args.corporate_domains
    )

    generator.generate_all()


if __name__ == '__main__':
    main()
