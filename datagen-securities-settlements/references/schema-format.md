# Securities Settlement Schema Format

## Overview

This document describes the JSON schema format used by the securities settlement data generator.

## Schema Structure

```json
{
  "schema_version": "1.0",
  "description": "Brief description of the schema purpose",
  "tables": {
    "table_name": {
      "description": "Table purpose",
      "columns": { ... },
      "row_count": 1000
    }
  },
  "temporal_constraints": { ... },
  "data_generation_period": { ... }
}
```

## Top-Level Fields

### schema_version

**Type**: String
**Required**: Yes
**Description**: Version of the schema format

**Example**:
```json
"schema_version": "1.0"
```

### description

**Type**: String
**Required**: Yes
**Description**: High-level description of what this schema represents

**Example**:
```json
"description": "Securities settlements schema with focus on settlement fails"
```

### tables

**Type**: Object
**Required**: Yes
**Description**: Dictionary of table definitions, keyed by table name

### temporal_constraints

**Type**: Object
**Required**: No
**Description**: Timing rules and constraints between tables

### data_generation_period

**Type**: Object
**Required**: Yes
**Description**: Date range for generated data

## Table Definition

Each table in the `tables` object follows this structure:

```json
"table_name": {
  "description": "Table description",
  "columns": {
    "column_name": {
      "type": "varchar(255)",
      "nullable": false,
      "primary_key": false,
      "foreign_key": "other_table.other_column",
      "unique": false,
      "default": "value",
      "values": ["option1", "option2"],
      "distribution": {
        "option1": 0.7,
        "option2": 0.3
      },
      "generator": "generator_name",
      "depends_on": ["other_column"],
      "description": "Column purpose"
    }
  },
  "row_count": 100000
}
```

### Table Fields

#### description

**Type**: String
**Required**: Yes
**Description**: What this table stores

#### columns

**Type**: Object
**Required**: Yes
**Description**: Column definitions

#### row_count

**Type**: Integer
**Required**: Yes
**Description**: Number of rows to generate for this table

**Important**: This is REQUIRED for every table

## Column Definition

### Core Properties

#### type

**Type**: String
**Required**: Yes
**Description**: PostgreSQL data type

**Supported Types**:
- `uuid` - UUID primary keys
- `varchar(n)` - Variable-length string
- `char(n)` - Fixed-length string
- `text` - Unlimited text
- `integer` - 32-bit integer
- `bigint` - 64-bit integer
- `smallint` - 16-bit integer
- `numeric(p,s)` - Decimal with precision and scale
- `date` - Date (no time)
- `timestamp` - Date and time
- `boolean` - True/false
- `json` - JSON data

**Examples**:
```json
"type": "uuid"
"type": "varchar(255)"
"type": "numeric(15,2)"
"type": "timestamp"
```

#### nullable

**Type**: Boolean
**Required**: No (default: true)
**Description**: Whether column can contain NULL values

**Example**:
```json
"nullable": false
```

#### primary_key

**Type**: Boolean
**Required**: No (default: false)
**Description**: Whether this column is the primary key

**Example**:
```json
"primary_key": true
```

**Note**: Only one column per table should be primary key

#### foreign_key

**Type**: String
**Required**: No
**Description**: References another table's column

**Format**: `"table_name.column_name"`

**Example**:
```json
"foreign_key": "securities.security_id"
```

#### unique

**Type**: Boolean
**Required**: No (default: false)
**Description**: Whether values must be unique across table

**Example**:
```json
"unique": true
```

**Use Case**: Email addresses, account numbers, identifiers

#### default

**Type**: String
**Required**: No
**Description**: Default value for column

**Examples**:
```json
"default": "USD"
"default": "active"
"default": "0.00"
"default": "now()"
```

### Value Constraints

#### values

**Type**: Array of strings
**Required**: No
**Description**: Enumeration of allowed values

**Example**:
```json
"values": ["buy", "sell", "short_sell"]
```

**Use Case**: Status fields, categories, types

**Note**: Creates CHECK constraint in PostgreSQL

#### distribution

**Type**: Object
**Required**: No (must be paired with `values`)
**Description**: Probability distribution for each value

**Example**:
```json
"values": ["small_cap", "mid_cap", "large_cap"],
"distribution": {
  "small_cap": 0.30,
  "mid_cap": 0.40,
  "large_cap": 0.30
}
```

**Important**: Distribution values must sum to 1.0

### Generation Directives

#### generator

**Type**: String
**Required**: No
**Description**: Name of the generator function to use

**Example**:
```json
"generator": "cusip_identifier"
```

**Common Generators**:
- `cusip_identifier` - Valid 9-character CUSIP
- `isin_identifier` - Valid 12-character ISIN
- `stock_ticker` - Stock ticker symbol
- `trade_reference_number` - Unique trade reference
- `settlement_date_for_trade` - T+1 or T+2 settlement date
- `timestamp_in_period` - Random timestamp in generation period
- `fail_reason` - Realistic fail reason based on category

#### depends_on

**Type**: Array of strings
**Required**: No
**Description**: Columns that this column's value depends on

**Example**:
```json
"generator": "settlement_date_for_trade",
"depends_on": ["trade_date", "security_id"]
```

**Use Case**: When generator needs values from other columns

**Important**: Referenced columns must be generated first (earlier in column order)

### Documentation

#### description

**Type**: String
**Required**: No (but highly recommended)
**Description**: Explanation of column purpose and any special notes

**Example**:
```json
"description": "T+1 for US markets, T+2 for Japan and Europe"
```

## Data Generation Period

```json
"data_generation_period": {
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "description": "One year of settlement data"
}
```

### Fields

#### start_date

**Type**: String (ISO date format)
**Required**: Yes
**Description**: First date for generated data

#### end_date

**Type**: String (ISO date format)
**Required**: Yes
**Description**: Last date for generated data

#### description

**Type**: String
**Required**: No
**Description**: Explanation of the time period

## Temporal Constraints

```json
"temporal_constraints": {
  "settlement_flow": {
    "description": "Settlement timing rules",
    "trade_to_settlement": {
      "us_t_plus_1": {
        "business_days": 1,
        "description": "US markets settle T+1"
      },
      "jp_t_plus_2": {
        "business_days": 2,
        "description": "Japan settles T+2"
      }
    }
  }
}
```

### Purpose

Defines timing relationships between events (trade → settlement → fail → charge)

### Structure

Free-form nested objects describing timing rules

**Use Case**: Document expected timing patterns for validation

## Complete Example

```json
{
  "schema_version": "1.0",
  "description": "Securities settlement fail tracking",
  "tables": {
    "securities": {
      "description": "Equity securities",
      "columns": {
        "security_id": {
          "type": "uuid",
          "primary_key": true,
          "description": "Unique identifier"
        },
        "ticker": {
          "type": "varchar(10)",
          "nullable": false,
          "generator": "stock_ticker",
          "depends_on": ["market"]
        },
        "market": {
          "type": "varchar(10)",
          "nullable": false,
          "values": ["US", "JP", "EU"],
          "distribution": {
            "US": 0.60,
            "JP": 0.20,
            "EU": 0.20
          }
        },
        "cusip": {
          "type": "char(9)",
          "nullable": true,
          "unique": true,
          "generator": "cusip_identifier",
          "depends_on": ["market"],
          "description": "CUSIP for US securities only"
        },
        "isin": {
          "type": "char(12)",
          "nullable": false,
          "unique": true,
          "generator": "isin_identifier",
          "depends_on": ["market", "cusip"]
        }
      },
      "row_count": 5000
    },
    "trades": {
      "description": "Trade executions",
      "columns": {
        "trade_id": {
          "type": "uuid",
          "primary_key": true
        },
        "security_id": {
          "type": "uuid",
          "nullable": false,
          "foreign_key": "securities.security_id"
        },
        "trade_date": {
          "type": "date",
          "nullable": false,
          "generator": "trade_date_in_period"
        },
        "settlement_date": {
          "type": "date",
          "nullable": false,
          "generator": "settlement_date_for_trade",
          "depends_on": ["trade_date", "security_id"],
          "description": "T+1 for US, T+2 for JP/EU"
        }
      },
      "row_count": 100000
    }
  },
  "data_generation_period": {
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "description": "One year of data"
  }
}
```

## Best Practices

### Table Ordering

**Important**: Define tables in dependency order

**Correct**:
```json
{
  "tables": {
    "broker_dealers": { ... },    // No foreign keys
    "investors": { ... },          // References broker_dealers
    "securities": { ... },         // No foreign keys
    "trades": { ... }              // References investors, securities
  }
}
```

**Incorrect**:
```json
{
  "tables": {
    "trades": { ... },             // ERROR: references not-yet-defined tables
    "investors": { ... },
    "securities": { ... },
    "broker_dealers": { ... }
  }
}
```

### Column Ordering

Within a table, define columns in dependency order:

**Correct**:
```json
{
  "market": { ... },               // Independent
  "cusip": {
    "depends_on": ["market"]       // Defined after market
  },
  "isin": {
    "depends_on": ["market", "cusip"]  // Defined after both
  }
}
```

### Row Counts

**Guidelines**:
- Parent tables: Smaller row counts (100-50,000)
- Child tables: Larger row counts (100,000-1,000,000)
- Maintain realistic ratios

**Example Ratios**:
- 250 broker-dealers
- 15,000 investors (60:1 ratio)
- 5,000 securities (20:1 ratio)
- 500,000 trades (33:1 ratio per investor)
- 75,000 settlement fails (15% of trades)

### Distributions

**Important**: Distribution values must sum to 1.0

**Correct**:
```json
"distribution": {
  "US": 0.60,
  "JP": 0.20,
  "EU": 0.20
}
// Sum: 0.60 + 0.20 + 0.20 = 1.0 ✓
```

**Incorrect**:
```json
"distribution": {
  "US": 0.60,
  "JP": 0.20,
  "EU": 0.30
}
// Sum: 0.60 + 0.20 + 0.30 = 1.10 ✗
```

### Nullable vs Required

**Use `nullable: false` for**:
- Primary keys
- Foreign keys
- Business-critical fields (security name, trade quantity)
- Status fields

**Use `nullable: true` for**:
- Optional fields (phone number, middle name)
- Fields that may not apply (resolution_date for active fails)
- Conditional fields (buy_in_date only for chronic fails)

### Unique Constraints

**Use `unique: true` for**:
- Business identifiers (CUSIP, ISIN, account numbers)
- Email addresses
- Trade/settlement reference numbers

**Don't use for**:
- Names (many "John Smith" entries expected)
- Amounts (many trades for same dollar value)
- Dates (many trades on same date)

## Validation

### Required Fields Check

Every table MUST have:
- `description`
- `columns` object with at least one column
- `row_count` > 0

Every column MUST have:
- `type`

### Foreign Key Validation

Foreign keys must reference:
- An existing table (defined earlier in schema)
- A column in that table
- The primary key of that table (best practice)

### Generator Validation

If `depends_on` is specified:
- Referenced columns must exist in the same table
- Referenced columns must be defined earlier in column order

### Distribution Validation

If `distribution` is specified:
- Must have corresponding `values` array
- All `values` must have distribution entry
- Sum of all distribution values must equal 1.0 (within 0.001 tolerance)

## Error Messages

### Missing row_count

```
ERROR: Table 'trades' missing required 'row_count' field
```

**Fix**: Add `"row_count": 100000` to table definition

### Invalid foreign key

```
ERROR: Foreign key 'securities.security_id' references undefined table 'securities'
```

**Fix**: Define `securities` table before `trades` table

### Distribution sum mismatch

```
ERROR: Distribution for 'market' sums to 1.10, must equal 1.0
```

**Fix**: Adjust distribution values to sum to exactly 1.0

### Circular dependency

```
ERROR: Column 'field_a' depends on 'field_b' which depends on 'field_a'
```

**Fix**: Remove circular dependency in column ordering
