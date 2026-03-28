---
name: datagen-securities-settlements
description: Generate realistic securities settlement data with focus on settlement fails, exceptions, and resolution workflows. Creates synthetic data for equities settlements across multiple markets (US T+1, Japan T+2, Europe T+2) with broker-dealers, institutional/retail investors, trade execution, settlement instructions, and comprehensive fail tracking with industry-standard identifiers (CUSIP, ISIN, DTC).
---

# Securities Settlements Data Generator

Generate realistic synthetic data for **equities settlement workflows** with a primary focus on **settlement fails, exceptions, and resolution processes**.

## When to Use This Skill

Use this skill when you need to:

### Securities Settlement Testing
- Generate realistic settlement data for T+1 (US), T+2 (Japan/Europe) settlement cycles
- Test settlement fail detection and resolution systems
- Create data for regulatory reporting (fails tracking, buy-in procedures)
- Simulate multi-market settlement scenarios

### Settlement Fails Analysis
- **Primary focus**: Generate realistic settlement fail scenarios
- Track fail reasons (insufficient securities, cash shortfalls, operational issues)
- Model fail charges and penalties
- Simulate fail resolution workflows (aged fails, buy-ins, close-outs)

### Market Participant Workflows
- Broker-dealer trade execution and settlement
- Institutional investor settlement processing
- Retail investor trade settlements
- Multi-party settlement chains

### Industry Standards
- CUSIP and ISIN security identifiers
- DTC participant numbers
- DVP/RVP settlement methods
- NSCC settlement workflows
- Industry-standard fail classifications

## Core Workflow

The skill follows a three-step process:

1. **Schema Generation**: Create PostgreSQL DDL for securities settlements
2. **Data Generation**: Generate CSV files with realistic settlement data
3. **Data Loading**: Bulk insert CSVs into PostgreSQL with validation

## Quick Start

### Step 1: Generate PostgreSQL Schema

Create the database schema from the provided schema definition:

```bash
python scripts/create_postgres_schema.py \
    assets/securities_settlement_schema.json \
    --output settlement_schema.sql
```

This generates a PostgreSQL 18 schema with:
- **broker_dealers** - Market participants (buy-side/sell-side)
- **investors** - Institutional and retail investors
- **securities** - Equities with market identifiers (CUSIP, ISIN)
- **trades** - Trade executions with market-specific details
- **settlement_instructions** - SSIs, DVP/RVP instructions
- **settlements** - Settlement attempts with status tracking
- **settlement_fails** - **Detailed fail tracking** (reasons, aging, resolution)
- **fail_charges** - Penalty fees and charges for fails

Then create the schema: `psql -U username -d database -f settlement_schema.sql`

### Step 2: Generate Settlement Data

Generate CSV files with realistic settlement data focused on fails:

```bash
python scripts/generate_securities_data.py \
    assets/securities_settlement_schema.json \
    ./settlement_data
```

Optional flags:
- `--fail-rate 0.15` - Target fail rate (default: 15% realistic industry rate)
- `--markets US,JP,EU` - Specific markets to generate
- `--date-range 2024-01-01,2024-12-31` - Custom date range

The generator will:
1. Create broker-dealers and investors across markets
2. Generate securities with proper identifiers (CUSIP for US, ISIN for international)
3. Create trades with realistic volumes and prices
4. Generate settlement instructions (SSIs, DVP/RVP)
5. **Simulate settlements with realistic fail scenarios**
6. Track fail aging, charges, and resolution

### Step 3: Load Data into PostgreSQL

Bulk insert the generated settlement data:

```bash
python scripts/insert_data.py \
    assets/securities_settlement_schema.json \
    ./settlement_data \
    -d settlement_db -U username -W password
```

Optional flags:
- `--host localhost` - Database host
- `--port 5432` - Database port
- `--batch-size 10000` - Rows per batch
- `--stats` - Show settlement statistics after loading

## Settlement Fails - Primary Focus

This generator's **primary differentiator** is its focus on realistic settlement fails.

### Fail Scenarios Generated

**Insufficient Securities (40%)**
- Seller doesn't have securities in custody
- Securities are pledged/encumbered
- Corporate action pending

**Cash Shortfalls (25%)**
- Buyer insufficient funds
- Credit limit exceeded
- Payment system unavailable

**Operational Issues (20%)**
- System outages
- Incorrect settlement instructions
- Missing/invalid SSI data

**Custody Issues (10%)**
- Securities in wrong account
- Custody transfer pending
- Account restrictions

**Other (5%)**
- Regulatory holds
- Legal disputes
- Force majeure

### Fail Aging and Resolution

Generates realistic fail aging patterns:
- **Day 0-3**: Recent fails, high resolution rate (60%)
- **Day 4-10**: Aged fails, medium resolution rate (30%)
- **Day 11-20**: Extended fails, lower resolution rate (15%)
- **Day 21+**: Chronic fails, buy-in procedures initiated

### Fail Charges and Penalties

Realistic penalty calculations:
- **Daily fail charges**: Based on fail value and duration
- **Buy-in costs**: When counterparty purchases securities in market
- **Administrative fees**: For extended fail processing
- **Regulatory fines**: For chronic or systemic fails

## Settlement Cycles by Market

### US Markets (T+1)
- **Exchanges**: NYSE, NASDAQ, BATS
- **Settlement**: Trade date + 1 business day
- **Identifiers**: CUSIP (9 characters)
- **Clearinghouse**: NSCC/DTC
- **Fail threshold**: $250M+ trigger mandatory buy-in

### Japan Market (T+2)
- **Exchange**: Tokyo Stock Exchange (TSE)
- **Settlement**: Trade date + 2 business days
- **Identifiers**: ISIN (JP prefix)
- **Clearinghouse**: JSCC
- **Business days**: Exclude Japanese holidays

### European Markets (T+2)
- **Exchanges**: LSE, Euronext, Deutsche Börse
- **Settlement**: Trade date + 2 business days
- **Identifiers**: ISIN (country prefix - GB, FR, DE, etc.)
- **Clearinghouse**: Euroclear, Clearstream
- **Cross-border**: Additional complexity for multi-market settlements

## Schema Overview

### Core Tables

**broker_dealers** (100-500 rows)
- DTC participant numbers
- Broker type (buy-side, sell-side, market maker)
- Market coverage and relationships

**investors** (5,000-50,000 rows)
- Institutional (hedge funds, mutual funds, pensions)
- Retail (individual investors)
- Investment mandates and trading patterns

**securities** (1,000-10,000 rows)
- Equities across US, Japan, Europe markets
- CUSIP (US), ISIN (international) identifiers
- Market cap, sector, liquidity tiers

**trades** (100,000-1,000,000 rows)
- Buy/sell executions
- Trade prices, quantities, commissions
- Executing broker and settlement broker

**settlement_instructions** (100,000-1,000,000 rows)
- Standing Settlement Instructions (SSI)
- DVP (Delivery vs Payment) / RVP (Receive vs Payment)
- Custodian details and account numbers

**settlements** (100,000-1,000,000 rows)
- Settlement attempts with status (settled, failed, partial)
- Settlement dates and amounts
- Links to trades and settlement instructions

**settlement_fails** (15,000-150,000 rows)
- **Detailed fail tracking**
- Fail reasons and categories
- Aging analysis (days outstanding)
- Resolution status and methods

**fail_charges** (10,000-100,000 rows)
- Daily fail fees
- Buy-in costs
- Administrative and regulatory penalties

## Realistic Data Features

### Industry-Standard Identifiers

**CUSIP (US Securities)**
- 9-character identifier (6 issuer + 2 issue + 1 check digit)
- Example: 037833100 (Apple Inc.)
- Generated with valid check digits

**ISIN (International Securities)**
- 12-character identifier (2 country + 9 security + 1 check digit)
- Japan: JP3633400001 (Toyota Motor Corp)
- UK: GB0005405286 (HSBC Holdings)
- Generated with valid Luhn algorithm check digits

**DTC Participant Numbers**
- 4-digit numbers for US broker-dealers
- Realistic numbering for major brokers

### Settlement Timing Realism

**Business Day Calculations**
- Excludes weekends and market holidays
- Market-specific holiday calendars (US, Japan, Europe)
- Proper T+1 and T+2 settlement date calculations

**Intraday Timing**
- Trade execution times (market hours per exchange)
- Settlement cut-off times
- Fail notification timing

### Financial Realism

**Trade Sizing**
- Institutional: 10,000-500,000 shares per trade
- Retail: 10-1,000 shares per trade
- Price impact modeling for large trades

**Fail Value Distribution**
- Small fails: $10K-$100K (70%)
- Medium fails: $100K-$1M (25%)
- Large fails: $1M+ (5%)

### Referential Integrity

- All foreign keys reference existing records
- Settlement cycles properly linked to trades
- Fail charges linked to specific fails
- Temporal consistency (trade → settlement → fail)

## Advanced Usage

### Custom Fail Rate Scenarios

Generate specific fail rate scenarios:

```bash
# Low fail environment (5%)
python scripts/generate_securities_data.py schema.json ./data --fail-rate 0.05

# Crisis scenario (40% fails)
python scripts/generate_securities_data.py schema.json ./data --fail-rate 0.40

# Normal market (15% - default)
python scripts/generate_securities_data.py schema.json ./data --fail-rate 0.15
```

### Market-Specific Generation

Focus on specific markets:

```bash
# US only (T+1)
python scripts/generate_securities_data.py schema.json ./data --markets US

# Japan only (T+2)
python scripts/generate_securities_data.py schema.json ./data --markets JP

# Europe only (T+2)
python scripts/generate_securities_data.py schema.json ./data --markets EU
```

### Aged Fails Analysis

Generate data with specific fail aging patterns:

```bash
# Include more aged fails for stress testing
python scripts/generate_securities_data.py schema.json ./data --aged-fails-pct 0.30
```

## Use Cases

### Regulatory Compliance Testing

Test systems for:
- Reg SHO (close-out requirements)
- CSDR (Central Securities Depositories Regulation) penalties
- Fail reporting requirements
- Buy-in regime compliance

### Operations Automation

Develop and test:
- Automated fail detection
- Fail resolution workflows
- Buy-in process automation
- Fail charge calculations

### Risk Analytics

Analyze:
- Fail exposure by counterparty
- Aged fail concentrations
- Fail cost analysis
- Settlement efficiency metrics

### Performance Testing

Load test:
- Real-time settlement matching systems
- Fail tracking databases
- Reporting and analytics platforms
- End-of-day settlement processing

## Requirements

**Python Packages:**
- `psycopg2` - PostgreSQL adapter
- Standard library (json, csv, random, datetime, uuid, argparse, pathlib)

Install: `pip install psycopg2-binary`

**Database:**
- PostgreSQL 18 (recommended) or PostgreSQL 12+
- UUID extension enabled

## Industry Accuracy

This generator uses real-world settlement industry knowledge:

✅ **Realistic fail rates**: 10-20% industry average
✅ **Proper settlement cycles**: T+1 (US), T+2 (JP/EU)
✅ **Valid identifiers**: CUSIP/ISIN with check digits
✅ **Industry terminology**: DVP, RVP, SSI, DTC, NSCC
✅ **Realistic fail reasons**: Based on actual market patterns
✅ **Proper aging**: Fail progression and resolution rates
✅ **Accurate penalties**: Based on regulatory frameworks

## Tips for Success

1. **Start small**: Generate 10,000 trades first to validate schema
2. **Focus on fails**: Use `--fail-rate` to control fail scenarios
3. **Market-specific**: Test one market at a time initially
4. **Validate cycles**: Check T+1 vs T+2 settlement date calculations
5. **Review identifiers**: Ensure CUSIP/ISIN formats are correct
6. **Test resolution**: Verify fail aging and resolution patterns

## Next Steps

After generating settlement data:

1. Create views for fail analytics (aging buckets, fail reasons)
2. Build dashboards for settlement efficiency monitoring
3. Test fail resolution workflows with the generated exceptions
4. Validate buy-in process automation
5. Run regulatory reporting simulations
6. Analyze counterparty fail exposure
