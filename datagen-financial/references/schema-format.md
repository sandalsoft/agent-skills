# Schema Format Specification

This document describes the JSON schema format expected by the data generator.

## Overview

The schema format defines database tables, columns, relationships, constraints, and generation parameters.

## Top-Level Structure

```json
{
  "schema_version": "1.0",
  "description": "Human-readable description of the schema",
  "tables": { ... },
  "temporal_constraints": { ... },
  "data_generation_period": { ... }
}
```

### Required Fields

- `schema_version` (string): Version identifier
- `description` (string): Schema description
- `tables` (object): Table definitions (see below)

### Optional Fields

- `temporal_constraints` (object): Timing rules between transaction stages
- `data_generation_period` (object): Date range for generated data
  - **If not specified**: Defaults to past 18 months from execution date
  - **If specified**: Uses the provided start_date and end_date

## Table Definition

Each table is defined as a key-value pair in the `tables` object:

```json
"table_name": {
  "description": "Table purpose",
  "columns": { ... },
  "row_count": 1000000
}
```

### Table Fields

- `description` (string, optional): Human-readable table description
- `columns` (object, required): Column definitions
- `row_count` (integer, **REQUIRED**): Number of rows to generate
  - **CRITICAL**: This field is REQUIRED for every table
  - The generator will stop with an error if any table is missing row_count
  - There is NO default value - you must explicitly specify how many rows to generate

## Column Definition

Each column is defined within the table's `columns` object:

```json
"column_name": {
  "type": "varchar(100)",
  "nullable": false,
  "primary_key": true,
  "foreign_key": "other_table.column",
  "unique": true,
  "values": ["option1", "option2"],
  "default": "value",
  "description": "Column description"
}
```

### Column Fields

#### Required

- `type` (string): SQL data type (see Supported Types below)

#### Optional

- `nullable` (boolean): Allow NULL values (default: true)
- `primary_key` (boolean): Is this column the primary key? (default: false)
- `foreign_key` (string): Reference to another table's column in format `table.column`
- `unique` (boolean): Enforce uniqueness constraint (default: false)
- `values` (array): Enumerated list of allowed values (for enum-like columns)
- `default` (string/number): Default value; use `"now()"` for current timestamp
- `description` (string): Human-readable column description

### Supported Types

**UUID Types**
- `uuid`: Universally unique identifier

**String Types**
- `varchar(n)`: Variable-length string with max length
- `char(n)`: Fixed-length string
- `text`: Unlimited length text

**Numeric Types**
- `integer`, `int`: 32-bit integer
- `smallint`: 16-bit integer
- `bigint`: 64-bit integer
- `numeric(p,s)`: Decimal with precision and scale
- `decimal(p,s)`: Alias for numeric
- `float`, `real`: Floating point
- `double precision`: Double-precision floating point

**Boolean Types**
- `boolean`, `bool`: True/false value

**Date/Time Types**
- `date`: Date only (YYYY-MM-DD)
- `timestamp`, `datetime`: Date and time
- `time`: Time only

**Other Types**
- `json`, `jsonb`: JSON data

## Temporal Constraints

Define realistic timing between transaction stages:

```json
"temporal_constraints": {
  "transaction_flow": {
    "description": "Timing between stages",
    "authorization_to_clearing": {
      "min_seconds": 3600,
      "max_seconds": 86400,
      "description": "1-24 hours"
    },
    "clearing_to_settlement": {
      "min_seconds": 7200,
      "max_seconds": 172800,
      "description": "2-48 hours"
    }
  }
}
```

These constraints ensure that:
- Clearing timestamps are always after authorization
- Settlement timestamps are always after clearing
- Time differences fall within realistic ranges

## Data Generation Period

Define the time range for generated data (OPTIONAL):

```json
"data_generation_period": {
  "start_date": "2023-01-01",
  "end_date": "2024-12-31",
  "description": "Generate 2 years of data"
}
```

**Default Behavior (if not specified):**
- If `data_generation_period` is omitted or empty, the generator automatically uses:
  - `start_date`: 18 months before the execution date
  - `end_date`: Current execution date
  - Example: If run on 2025-10-24, defaults to 2024-04-24 through 2025-10-24

**When to Specify:**
- Use specific dates for historical data recreation
- Use specific dates when you need exact date ranges for testing
- Omit to always generate "recent" data relative to when the script runs

All timestamp and date fields will generate values within this range.

## Special Column Naming Conventions

The generator recognizes certain column names and generates appropriate data:

### Name Fields
- `first_name` → Realistic first name from frequency distribution
- `last_name` → Realistic last name from frequency distribution
- `email` → Email address based on first and last name

### Address Fields
- `address`, `address_line1` → Street address
- `city` → City name
- `state` → Two-letter state code
- `zip_code`, `zip` → US ZIP code
- `latitude`, `lat` → Latitude coordinate
- `longitude`, `lon`, `lng` → Longitude coordinate

### Contact Fields
- `phone` → Phone number in format XXX-XXX-XXXX

### Financial Fields
- Columns containing `amount` → Realistic transaction amounts
- Columns containing `fee` → Realistic processing fees
- Columns containing `limit` → Credit limits

### Card Fields
- `card_number` → Credit card number (not Luhn-compliant, but realistic format)
- `cvv` → 3-digit security code
- `expiration_month` → Month 1-12
- `expiration_year` → Future year

### Date/Time Fields
- `created_at`, `issued_at`, `updated_at` → Timestamp of creation
- Columns ending in `_at` → Timestamps
- Columns ending in `_date` → Dates

### Identifier Fields
- Columns ending in `_id` or `_code` → Unique identifiers

## Foreign Key Resolution

Foreign keys are resolved during generation in dependency order:

1. **Parent tables generated first**: Tables with no foreign keys
2. **Child tables generated second**: Tables that reference parent tables
3. **Circular references**: Handled by generating all tables first, then validating

The generator automatically determines the correct generation order based on foreign key relationships.

## Example: Complete Table Definition

```json
"transactions": {
  "description": "Credit card transaction records",
  "columns": {
    "transaction_id": {
      "type": "uuid",
      "primary_key": true,
      "description": "Unique transaction identifier"
    },
    "card_id": {
      "type": "uuid",
      "nullable": false,
      "foreign_key": "cards.card_id",
      "description": "Reference to card used"
    },
    "merchant_id": {
      "type": "uuid",
      "nullable": false,
      "foreign_key": "merchants.merchant_id",
      "description": "Reference to merchant location"
    },
    "amount": {
      "type": "numeric(10,2)",
      "nullable": false,
      "description": "Transaction amount in USD"
    },
    "status": {
      "type": "varchar(20)",
      "nullable": false,
      "values": ["approved", "declined", "pending"],
      "default": "pending",
      "description": "Transaction status"
    },
    "transaction_date": {
      "type": "timestamp",
      "nullable": false,
      "default": "now()",
      "description": "When transaction occurred"
    },
    "description": {
      "type": "text",
      "nullable": true,
      "description": "Optional transaction description"
    }
  },
  "row_count": 10000000
}
```

## Validation Rules

The schema will be validated for:

- **Required fields present**: All tables have required fields
- **Type validity**: All column types are recognized
- **Foreign key validity**: All foreign key references point to existing tables/columns
- **Primary key presence**: Each table has at least one primary key
- **Circular dependency handling**: Circular foreign key references are detected

## Best Practices

### Naming Conventions

- Use `snake_case` for table and column names
- Use descriptive, singular names for columns
- Suffix foreign keys with `_id`
- Suffix date/time columns with `_at` or `_date`

### Referential Integrity

- Always define foreign keys explicitly
- Ensure parent tables are defined before child tables
- Use `ON DELETE CASCADE` behavior (handled by schema generator)

### Data Types

- Use `uuid` for primary keys (better distribution, no collisions)
- Use `varchar` with appropriate limits (saves space)
- Use `numeric` for financial amounts (exact precision)
- Use `timestamp` for transaction times (includes date + time)

### Row Counts

- Start small for testing (1,000-10,000 rows)
- Scale to realistic sizes for performance testing
- Consider table relationships (e.g., 1 million cardholders → 5 million transactions)

### Performance Considerations

- Tables with millions of rows should have indices on foreign keys
- Timestamp columns should be indexed for time-range queries
- Consider partitioning very large tables (100M+ rows)

## Advanced Features

### Computed Columns

While not directly supported in the schema format, you can:

1. Generate base data
2. Use PostgreSQL generated columns or triggers
3. Post-process CSVs before loading

### Custom Data Patterns

For highly specialized data patterns:

1. Define the schema normally
2. Create custom constraint rules (see `rule-patterns.md`)
3. Or post-process generated CSVs with custom scripts
