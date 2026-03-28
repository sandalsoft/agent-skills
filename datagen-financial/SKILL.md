---
name: datagen-financial
description: Generate realistic, referentially-integral synthetic financial data for credit card processing networks AND comprehensive banking systems. Use when users need coherent financial data across multiple related tables (transactions, accounts, loans, investments) with 100% email-name matching, merchant-country coherence, proper referential integrity, realistic temporal/spatial constraints, and business logic enforcement. Supports both credit card processing and full banking schemas. Includes specialized banking data generator with enhanced coherence features.
---

# Financial Data Generation Skill

Generate massive volumes of realistic synthetic financial data with guaranteed referential integrity, temporal/spatial coherence, and **100% data coherence**.

## When to Use This Skill

Use this skill when the user needs to:

### Credit Card Processing
- Generate synthetic credit card transaction data at scale (thousands to millions of rows)
- Create data for credit card processing networks (POS, auth, clearing, settlement, reconciliation)
- Test fraud detection systems or payment processing pipelines

### Banking Systems (NEW!)
- Generate comprehensive banking data (customers, accounts, loans, cards, transactions)
- Ensure **100% email-name coherence** (emails match customer names exactly)
- Ensure **merchant-country coherence** (merchant names match their geographic locations)
- Create realistic banking scenarios with investments, wire transfers, bill payments
- Generate data for banking demos, development, and testing

### Common Features
- Ensure referential integrity across multiple related tables
- Maintain realistic distributions for names, locations, amounts, and timing
- Inject custom business logic and constraints
- Output CSVs for PostgreSQL insertion
- Test database performance and analytics pipelines

## Core Workflow

The skill follows a three-step process:

1. **Schema Generation**: Create PostgreSQL DDL from schema definition
2. **Data Generation**: Generate CSV files with realistic, coherent data
3. **Data Loading**: Bulk insert CSVs into PostgreSQL with validation

## Quick Start

### Step 1: Define Your Schema

First, help the user create a schema JSON file that defines their tables, columns, relationships, and row counts. Use `assets/example_schema.json` as a template:

```bash
# User provides their schema, or you help them create one based on example
cp assets/example_schema.json user_schema.json
# Edit as needed
```

**Key schema elements:**
- Tables with columns, types, constraints
- Foreign key relationships
- **Row counts per table (REQUIRED)** - Must be specified for each table
- Temporal constraints (optional)
- Data generation period (optional - defaults to past 18 months)

**CRITICAL REQUIREMENTS:**
1. **`row_count` is REQUIRED for every table** - The generator will stop and prompt the user if missing
2. **`data_generation_period` is OPTIONAL** - If not specified, defaults to the past 18 months from execution date

Example:
```json
{
  "tables": {
    "transactions": {
      "description": "Transaction records",
      "row_count": 1000000,  // REQUIRED - must specify
      "columns": { ... }
    }
  },
  "data_generation_period": {  // OPTIONAL - defaults to past 18 months
    "start_date": "2023-01-01",
    "end_date": "2024-12-31"
  }
}
```

See `references/schema-format.md` for complete schema specification.

### Step 2: Generate PostgreSQL Schema

Create the database schema (DDL) from the schema definition:

```bash
python scripts/create_postgres_schema.py user_schema.json --output schema.sql
```

This generates:
- CREATE TABLE statements with proper types
- Primary key constraints
- Unique constraints
- Check constraints (for enum-like fields)
- Foreign key constraints
- Indices on foreign keys and timestamps
- Table and column comments

User can then run: `psql -U username -d database -f schema.sql`

### Step 3: Generate Data

Generate CSV files with realistic, referentially-integral data:

```bash
python scripts/generate_data.py user_schema.json ./output_data
```

Optional flags:
- `--constraints rules.json` - Apply business logic constraints
- `--distributions assets/name_distributions.json` - Custom name distributions
- `--merchants assets/merchant_types.json` - Custom merchant data

The generator will:
1. Read the schema definition
2. Determine table generation order (respecting foreign keys)
3. Generate each table with realistic data
4. Enforce referential integrity
5. Apply temporal/spatial constraints
6. Output CSV files named `{table_name}.csv`

### Step 4: Load Data into PostgreSQL

Bulk insert the generated CSV files:

```bash
python scripts/insert_data.py user_schema.json ./output_data \
    -d database_name -U username -W password
```

Optional flags:
- `--host localhost` - Database host
- `--port 5432` - Database port
- `--batch-size 10000` - Rows per batch (default: 10000)
- `--stats` - Show table statistics after loading

The loader will:
1. Connect to PostgreSQL
2. Determine load order (respecting foreign keys)
3. Temporarily disable triggers for faster loading
4. Bulk insert using COPY (very fast)
5. Re-enable triggers
6. Validate referential integrity
7. Report statistics

## Banking Data Generation (NEW!)

For comprehensive banking systems, use the specialized coherent banking data generator:

### Quick Banking Setup

```bash
# 1. Generate coherent banking data (161K+ rows)
python scripts/generate_coherent_banking_data.py \
    assets/banking_schema_example.json \
    ./banking_data

# 2. Load into PostgreSQL using DATABASE_URL
export DATABASE_URL="postgresql://user:password@host:port/database"
python scripts/load_banking_data.py
```

This generates **161,258 rows** across 11 banking tables with:

✅ **100% Email-Name Coherence**: Every customer email matches their first/last name
- Example: `Andrew Hill` → `andrew.hill@yahoo.com`

✅ **100% Merchant-Country Coherence**: Merchant names match their locations
- US (95%): Target, Walmart, Shell, Amazon, Whole Foods
- International (5%): "International Retail - Tokyo" (Japan)

✅ **100% Referential Integrity**: All foreign keys valid, no orphaned records

✅ **0 Temporal Violations**: All dates in correct sequence
- completed_at always after initiated_at
- Settlement follows T+1 to T+3 cycles

✅ **Realistic Distributions**:
- 80% retail / 20% commercial customers
- 95% US / 5% international transactions
- Wire transfers avg: $16,913 (lognormal distribution)
- Wealth accounts avg: $367,420 (biased higher)

### Banking Tables Generated

1. **customers** (2,108 rows) - Retail and commercial customers
2. **accounts** (3,000 rows) - Checking, savings, CDs, money market
3. **loans** (2,500 rows) - Personal, auto, mortgage, business, education
4. **cards** (2,300 rows) - Debit and credit cards
5. **card_transactions** (85,000 rows) - POS and online purchases
6. **wire_transfers** (3,200 rows) - Domestic and international transfers
7. **bill_payments** (12,500 rows) - Utility and service payments
8. **wealth_management_accounts** (850 rows) - Investment portfolios
9. **investment_transactions** (4,800 rows) - Stock/bond/ETF trades
10. **atm_transactions** (18,000 rows) - ATM withdrawals and deposits
11. **loan_payments** (28,000 rows) - Monthly loan repayments

### Banking Data Features

**Coherent Merchant Names**:
- Restaurants: Olive Garden, Cheesecake Factory, Applebee's, Chili's
- Retail: Target, Walmart, Best Buy, Macy's, Home Depot
- Gas Stations: Shell, Chevron, Exxon, BP, Marathon
- Grocery: Whole Foods, Trader Joe's, Kroger, Safeway
- Online: Amazon, eBay, Netflix, Spotify

**Coherent Bill Payment Billers**:
- Electricity: Pacific Gas & Electric, Con Edison, Duke Energy
- Telecom: Verizon, AT&T, T-Mobile
- Internet: Comcast Xfinity, Spectrum, Cox Communications
- Insurance: State Farm, Geico, Progressive, Allstate

**Real Investment Securities**:
- Stocks: Apple Inc., Microsoft Corp., Tesla Inc., Amazon.com Inc.
- ETFs: SPY (S&P 500), QQQ (Nasdaq 100), VTI (Total Market)
- Bonds: US Treasury 10Y, Corporate Bond AAA, Municipal Bond

See `references/banking-data-generation.md` for complete banking data documentation.

## Realistic Data Features

This skill ensures realism across multiple dimensions:

### Name Realism

- Uses frequency-weighted distributions based on US Census data
- Common names (John Smith) appear proportionally more often
- Rare names (Xenophon Beaumont) are appropriately uncommon
- Each person gets a unique name combination
- No naive repeated names like "John Smith" appearing 20 times

### Spatial Realism

- All locations constrained to continental US (configurable)
- Population-weighted city distribution (NYC gets more activity than rural areas)
- Realistic ZIP codes for each state
- Lat/long coordinates match cities
- Geographic coherence maintained

### Temporal Realism

- Transaction timing respects merchant business hours
- Peak hours vary by merchant type (restaurants busy at lunch/dinner, gas stations at commute times)
- Rate limiting prevents unrealistic transaction bursts (gas station can't process 1500 tx in 2 minutes)
- Transaction lifecycle timestamps progress correctly (auth < clearing < settlement < reconciliation)
- Date ranges respect schema definition

### Financial Realism

- Transaction amounts follow merchant-specific distributions
- Fees calculated realistically (interchange 1.5-3%, network $0.10-0.25)
- Settlement amounts satisfy issuer > acquirer constraint
- Card network distribution matches market share (Visa 50%, Mastercard 30%, etc.)
- Approval/decline rates realistic (85-90% approved overall)

### Referential Integrity

- All foreign keys reference existing parent records
- Same transaction_id flows through all related tables
- Parent tables generated before child tables
- Validation checks confirm integrity

See `references/realistic-data-patterns.md` for complete details.

## Business Logic Injection

Inject custom constraints and business rules via a constraints file:

### Constraint Types

1. **Spatial**: Geographic restrictions (continental US only, city limits, distance constraints)
2. **Temporal**: Timing rules (business hours, rate limits, sequence constraints)
3. **Data Quality**: Missing data rates, outliers, corruption simulation
4. **Relational**: Field relationships (issuer > acquirer, conditional requirements)
5. **Custom**: Python functions for complex logic

### Example Constraints File

```json
{
  "spatial": [
    {
      "entity": "pos_locations",
      "rule": "continental_us_only"
    }
  ],
  "data_quality": [
    {
      "field": "authorization_requests.transaction_code",
      "missing_rate": 0.0002
    }
  ],
  "relational": [
    {
      "rule": "settlement_records.issuer_settlement_amount > settlement_records.acquirer_settlement_amount",
      "enforcement": "always"
    }
  ],
  "temporal": [
    {
      "entity": "gas_station",
      "max_transactions_per_minute": 25
    }
  ]
}
```

See `references/rule-patterns.md` for complete constraint specification and examples.

## Bundled Resources

### Scripts

**`generate_data.py`** - Main data generation engine
- Parses schema definitions
- Generates realistic data with proper distributions
- Enforces referential integrity
- Applies constraint rules
- Outputs CSV files

Usage: `python scripts/generate_data.py schema.json output_dir [--constraints rules.json]`

**`create_postgres_schema.py`** - PostgreSQL DDL generator
- Creates complete schema from JSON definition
- Generates primary keys, foreign keys, indices, constraints
- Handles dependency ordering
- Adds helpful comments

Usage: `python scripts/create_postgres_schema.py schema.json [--output schema.sql]`

**`insert_data.py`** - PostgreSQL bulk loader
- Loads CSV files into PostgreSQL tables
- Uses COPY for maximum performance
- Validates referential integrity
- Handles large datasets efficiently

Usage: `python scripts/insert_data.py schema.json csv_dir -d dbname -U user [-W password]`

### References

**`schema-format.md`** - Schema JSON specification
Read this to understand:
- Required and optional schema fields
- Supported data types
- Foreign key syntax
- Temporal constraints
- Special column naming conventions

**`realistic-data-patterns.md`** - Realism documentation
Read this to understand:
- How name distributions work
- Spatial constraint details
- Temporal realism rules
- Financial calculation formulas
- Coherence guarantees

**`rule-patterns.md`** - Constraint injection guide
Read this to understand:
- All five constraint types (spatial, temporal, data quality, relational, custom)
- How to write constraint files
- Common constraint patterns
- Custom Python script integration
- Enforcement levels (hard vs soft)

### Assets

**`name_distributions.json`** - US Census name frequency data
- First names (male/female) with realistic frequency weights
- Last names with realistic frequency weights
- Used by generator to create realistically distributed names
- User can provide custom distributions if needed

**`merchant_types.json`** - Merchant category configurations
- MCC codes with descriptions
- Average transaction amounts and standard deviations
- Realistic transactions-per-day ranges
- Peak business hours by category
- Major US cities with population weights
- Continental US bounding box

**`example_schema.json`** - Complete example schema
- Credit card processing network schema
- Shows proper table relationships
- Demonstrates foreign key usage
- Includes temporal constraints
- Can be used as a template

## Advanced Usage

### Generating Millions of Rows

For very large datasets:

1. Use appropriate batch sizes (10,000-50,000 rows per batch)
2. Consider partitioning in PostgreSQL for 100M+ row tables
3. Generate data in stages if memory is constrained
4. Use `--stats` flag to monitor progress

### Custom Distributions

To use custom name/merchant distributions:

```bash
python scripts/generate_data.py schema.json ./output \
    --distributions my_distributions.json \
    --merchants my_merchants.json
```

### Fraud Pattern Injection

To inject fraud patterns for ML training:

1. Create custom constraint script (see `references/rule-patterns.md`)
2. Define fraud patterns (velocity fraud, synthetic identity, etc.)
3. Apply via constraints file

### Schema Validation

Before generating millions of rows, validate your schema:

1. Start with small row counts (1,000 rows per table)
2. Generate data and load into PostgreSQL
3. Verify referential integrity
4. Check data distributions
5. Scale up to full size

## Common Patterns

### Credit Card Processing Network

For a typical credit card processing network:

Tables needed:
- `cardholders` - Account holders
- `cards` - Credit cards issued
- `merchants` - Merchant locations
- `acquirers` - Acquiring banks
- `issuers` - Issuing banks
- `authorization_requests` - POS authorizations
- `clearing_records` - Transaction clearing
- `settlement_records` - Final settlements
- `reconciliation_records` - Daily reconciliation

See `assets/example_schema.json` for complete example.

### Fraud Detection Testing

For fraud detection systems:

1. Generate baseline legitimate transactions
2. Inject fraud patterns via custom constraints
3. Label fraudulent transactions with metadata
4. Output training dataset for ML models

### Performance Testing

For database performance testing:

1. Scale row counts to target size (10M, 100M, 1B rows)
2. Generate data with realistic query patterns in mind
3. Ensure proper indices are created
4. Consider table partitioning for very large datasets

## Troubleshooting

### "ERROR: row_count not specified"

**Cause**: One or more tables in schema.json missing the required `row_count` field

**Solution**: 
Add `row_count` to each table definition:
```json
"your_table": {
  "description": "Table description",
  "row_count": 1000000,  // Add this line
  "columns": { ... }
}
```

The generator will list which tables are missing row_count.

### "Referential integrity violations found"

**Cause**: Foreign keys reference non-existent records

**Solution**: 
- Ensure parent tables are defined in schema
- Check foreign key syntax in schema (`table.column`)
- Verify parent table row counts are sufficient

### "Transaction rate limit exceeded"

**Cause**: Too many transactions for a merchant in a short time window

**Solution**:
- Adjust temporal constraints
- Increase time window in schema
- Reduce transaction volume for specific merchants

### "Generation too slow"

**Cause**: Generating millions of rows can take time

**Solution**:
- Reduce row counts for testing
- Consider generating in stages
- Use faster storage (SSD vs HDD)
- Disable unnecessary constraints during generation

### "COPY command failed"

**Cause**: PostgreSQL COPY requires specific formatting

**Solution**:
- Script automatically falls back to INSERT
- Check for special characters in data
- Verify PostgreSQL user permissions

## Requirements

**Python Packages:**
- `psycopg2` - PostgreSQL adapter
- Standard library only (json, csv, random, datetime, uuid, argparse, pathlib)

Install: `pip install psycopg2-binary`

**Database:**
- PostgreSQL 12+ (earlier versions may work)
- UUID extension enabled (`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`)

## Tips for Success

1. **Start small**: Generate 1,000 rows first to validate schema
2. **Read references**: Schema format and constraint patterns are detailed in reference docs
3. **Validate early**: Check referential integrity on small datasets before scaling
4. **Use constraints**: Inject business logic via constraints file, don't modify scripts
5. **Monitor progress**: Scripts print progress every 10,000 rows
6. **Test queries**: After loading, test queries to ensure data meets requirements

## Next Steps After Generation

After generating and loading data:

1. Create additional indices for query patterns
2. Run ANALYZE to update PostgreSQL statistics
3. Test query performance
4. Create views for common access patterns
5. Consider materialized views for expensive aggregations
6. Set up monitoring for database health
