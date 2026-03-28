# Securities Settlements Data Generator

Generate realistic synthetic data for equities settlement workflows with primary focus on **settlement fails, exceptions, and resolution processes**.

## Overview

This skill creates comprehensive, referentially-integral data for securities settlements across multiple markets:

- **US Markets**: T+1 settlement cycle (post-May 2024 standard)
- **Japan Markets**: T+2 settlement cycle
- **European Markets**: T+2 settlement cycle

**Primary Focus**: Settlement fails with realistic reasons, aging patterns, resolution workflows, and penalty calculations.

## Features

✅ **Realistic Settlement Fails** (15% default rate)
- 5 fail categories: insufficient securities, cash shortfall, operational, custody, other
- Aged fail tracking (recent, aged, extended, chronic)
- Resolution methods and timelines
- Buy-in procedures for chronic fails

✅ **Industry-Standard Identifiers**
- CUSIP (US securities) with valid check digits
- ISIN (all markets) with proper Luhn algorithm validation
- DTC participant numbers for US broker-dealers

✅ **Multi-Market Support**
- US: NYSE, NASDAQ, BATS (T+1 settlement)
- Japan: Tokyo Stock Exchange (T+2 settlement)
- Europe: LSE, Euronext, Deutsche Börse (T+2 settlement)

✅ **Complete Settlement Lifecycle**
- Broker-dealers and investors
- Securities (equities across markets)
- Trade executions with realistic volumes
- Settlement instructions (DVP/RVP/FOP)
- Settlement attempts with status tracking
- **Detailed fail records** with reasons and resolution
- Fail charges and penalties

✅ **Referential Integrity**
- All foreign keys reference existing records
- Temporal consistency (trade → settlement → fail → resolution)
- Business day calculations with market-specific holidays

## Quick Start

### 1. Generate PostgreSQL Schema

```bash
python scripts/create_postgres_schema.py \
    assets/securities_settlement_schema.json \
    --output settlement_schema.sql
```

Creates an 8-table PostgreSQL 18 schema with all constraints, indices, and comments.

### 2. Generate Settlement Data

```bash
python scripts/generate_securities_data.py \
    assets/securities_settlement_schema.json \
    ./settlement_data
```

Generates:
- 250 broker-dealers
- 15,000 investors (institutional & retail)
- 5,000 securities with CUSIP/ISIN
- 500,000 trades
- 500,000 settlement instructions
- 500,000 settlement attempts
- **75,000 settlement fails** (15% rate)
- 150,000 fail charges and penalties

### 3. Load into PostgreSQL

```bash
python scripts/insert_data.py \
    assets/securities_settlement_schema.json \
    ./settlement_data \
    -d settlement_db -U username -W password
```

Bulk loads all CSV files into PostgreSQL with validation.

## Schema Overview

### Core Tables

**broker_dealers** (250 rows)
- Executing firms with DTC numbers
- Buy-side, sell-side, market makers
- Multi-market coverage

**investors** (15,000 rows)
- Institutional: hedge funds, mutual funds, pensions
- Retail: individual investors
- Linked to primary brokers

**securities** (5,000 rows)
- Equities across US, Japan, Europe
- CUSIP (US), ISIN (all markets)
- Market cap and liquidity tiers

**trades** (500,000 rows)
- Buy/sell executions
- Quantities, prices, commissions
- Market-specific settlement dates

**settlement_instructions** (500,000 rows)
- DVP/RVP/FOP instructions
- Custodian details
- Affirmation and matching status

**settlements** (500,000 rows)
- Settlement attempts
- Status: settled (82%), **failed (15%)**, partial (2%), pending (1%)
- Actual vs scheduled settlement dates

**settlement_fails** (75,000 rows) ⭐ **PRIMARY FOCUS**
- Detailed fail tracking
- 5 fail categories with specific reasons
- Fail aging (0-3 days, 4-10, 11-20, 21+ days)
- Resolution methods and status
- Buy-in procedures for chronic fails

**fail_charges** (150,000 rows)
- Daily fail fees
- Buy-in costs
- Administrative fees
- Regulatory fines
- Interest charges

## Configuration Options

### Adjust Fail Rate

```bash
# Low fail environment (5%)
python scripts/generate_securities_data.py schema.json ./data --fail-rate 0.05

# Normal market (15% - default)
python scripts/generate_securities_data.py schema.json ./data --fail-rate 0.15

# Crisis scenario (40%)
python scripts/generate_securities_data.py schema.json ./data --fail-rate 0.40
```

### Random Seed for Reproducibility

```bash
python scripts/generate_securities_data.py schema.json ./data --seed 42
```

## Use Cases

### Settlement Operations
- Test fail detection and resolution systems
- Automate fail aging analysis
- Model buy-in procedures
- Calculate penalty costs

### Regulatory Compliance
- Reg SHO testing (US close-out requirements)
- CSDR compliance (EU mandatory buy-in)
- Threshold list monitoring
- Reporting automation

### Risk Analytics
- Counterparty fail exposure analysis
- Aged fail concentration monitoring
- Settlement efficiency metrics
- Fail cost attribution

### Performance Testing
- Load test settlement matching systems
- Stress test fail tracking databases
- Benchmark reporting and analytics
- End-of-day processing simulation

## Example Queries

### Fail Analysis by Category

```sql
SELECT
    fail_category,
    COUNT(*) as fail_count,
    ROUND(AVG(fail_age_days), 1) as avg_age_days,
    SUM(fail_value) as total_fail_value
FROM settlement_fails
WHERE fail_status = 'active'
GROUP BY fail_category
ORDER BY fail_count DESC;
```

### Chronic Fails Requiring Buy-In

```sql
SELECT
    sf.fail_reference,
    s.ticker,
    t.trade_date,
    sf.fail_start_date,
    sf.fail_age_days,
    sf.fail_value,
    sf.fail_reason
FROM settlement_fails sf
JOIN trades t ON sf.trade_id = t.trade_id
JOIN securities s ON t.security_id = s.security_id
WHERE sf.fail_age_days >= 21
  AND sf.fail_status IN ('active', 'buy_in_initiated')
ORDER BY sf.fail_age_days DESC;
```

### Broker Settlement Efficiency

```sql
SELECT
    bd.firm_name,
    COUNT(DISTINCT t.trade_id) as total_trades,
    COUNT(DISTINCT sf.fail_id) as failed_trades,
    ROUND(COUNT(DISTINCT sf.fail_id)::numeric / COUNT(DISTINCT t.trade_id) * 100, 2) as fail_rate_pct,
    SUM(fc.charge_amount) as total_penalties
FROM broker_dealers bd
JOIN trades t ON bd.broker_dealer_id = t.executing_broker_id
LEFT JOIN settlements stl ON t.trade_id = stl.trade_id
LEFT JOIN settlement_fails sf ON stl.settlement_id = sf.settlement_id
LEFT JOIN fail_charges fc ON sf.fail_id = fc.fail_id
GROUP BY bd.broker_dealer_id, bd.firm_name
HAVING COUNT(DISTINCT t.trade_id) > 100
ORDER BY fail_rate_pct DESC
LIMIT 20;
```

### Daily Fail Charges by Type

```sql
SELECT
    charge_date,
    charge_type,
    COUNT(*) as charge_count,
    SUM(charge_amount) as total_charges
FROM fail_charges
WHERE charge_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY charge_date, charge_type
ORDER BY charge_date DESC, total_charges DESC;
```

## Settlement Fail Details

### Fail Categories (Distribution)

1. **Insufficient Securities** (40%)
   - Seller doesn't have securities in custody
   - Securities pledged or encumbered
   - Corporate action pending

2. **Cash Shortfall** (25%)
   - Buyer insufficient funds
   - Credit limit exceeded
   - Payment system unavailable

3. **Operational** (20%)
   - System outages
   - Incorrect settlement instructions
   - Matching failures

4. **Custody** (10%)
   - Securities in wrong account
   - Custody transfer pending
   - Account restrictions

5. **Other** (5%)
   - Regulatory holds
   - Legal disputes
   - Force majeure events

### Fail Aging Patterns

- **Recent (0-3 days)**: 60% resolution rate
- **Aged (4-10 days)**: 30% resolution rate
- **Extended (11-20 days)**: 15% resolution rate
- **Chronic (21+ days)**: 5% resolution rate, buy-in triggered

### Fail Charges

- **Daily Fail Fees**: 1-5 bps per day based on security type
- **Buy-In Costs**: Market price impact (1-5% typical)
- **Administrative Fees**: $50-$2,000 per fail
- **Regulatory Fines**: $1,000-$10,000+ for threshold breaches
- **Interest Charges**: Based on overnight rates

## File Structure

```
datagen-securities-settlements/
├── SKILL.md                    # Skill configuration
├── README.md                   # This file
├── CHANGELOG.md                # Version history
├── scripts/
│   ├── generate_securities_data.py    # Main data generator
│   ├── create_postgres_schema.py      # Schema DDL generator
│   └── insert_data.py                 # CSV bulk loader
├── assets/
│   └── securities_settlement_schema.json   # Schema definition
└── references/
    ├── settlement-fail-patterns.md    # Industry patterns
    └── schema-format.md               # Schema specification
```

## Requirements

**Python**: 3.7+

**Packages**:
```bash
pip install psycopg2-binary
```

**Database**: PostgreSQL 12+ (PostgreSQL 18 recommended)

## Industry Accuracy

This generator uses real-world settlement industry knowledge:

✅ Realistic fail rates (10-20% industry baseline)
✅ Proper settlement cycles (T+1 US, T+2 JP/EU)
✅ Valid CUSIP/ISIN check digits
✅ Industry-standard terminology (DVP, RVP, SSI, DTC, NSCC)
✅ Realistic fail reasons based on actual market patterns
✅ Proper aging buckets and resolution rates
✅ Accurate penalty calculations per regulatory frameworks

## Tips

1. **Start Small**: Generate 10K trades first to validate schema
2. **Adjust Fail Rate**: Use `--fail-rate` to test different scenarios
3. **Focus on Fails**: The settlement_fails table is the primary output
4. **Validate Cycles**: Verify T+1 vs T+2 settlement date calculations
5. **Check Identifiers**: Ensure CUSIP/ISIN formats are correct
6. **Analyze Aging**: Review fail aging distribution for realism

## Support

For questions, issues, or feature requests, please refer to:
- **Settlement Fail Patterns**: `references/settlement-fail-patterns.md`
- **Schema Format**: `references/schema-format.md`
- **Skill Documentation**: `SKILL.md`

## License

This skill is part of the Claude Code Skills library.

## Version

**1.0.0** - Initial release with comprehensive settlement fail support
