# Banking Data Generation Guide

This guide covers generating coherent, realistic banking data using the enhanced datagen-financialv2 skill.

## Overview

The skill now includes a specialized banking data generator (`generate_coherent_banking_data.py`) that ensures:

- ✅ **Email-Name Coherence**: 100% of customer emails match their first/last names
- ✅ **Merchant-Country Coherence**: Merchant names match their geographic locations
- ✅ **Geographic Consistency**: All city/state/zip combinations are valid
- ✅ **Temporal Ordering**: All transaction dates follow proper sequences
- ✅ **Referential Integrity**: 100% valid foreign key relationships
- ✅ **Realistic Distributions**: Based on real-world banking patterns

## Quick Start

### 1. Generate Banking Data

```bash
python scripts/generate_coherent_banking_data.py \
    assets/banking_schema_example.json \
    ./output_data
```

This generates:
- 2,108+ customers
- 3,000+ accounts
- 2,500+ loans
- 85,000+ card transactions
- Plus wire transfers, bill payments, investments, ATM transactions, and loan payments
- **Total: 161,258+ rows** of coherent data

### 2. Load into PostgreSQL

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
python scripts/load_banking_data.py
```

## Banking Schema Structure

The banking schema includes 11 related tables:

### Master Data
- **customers**: Retail and commercial customers
- **accounts**: Checking, savings, CDs, money market accounts
- **loans**: Personal, auto, mortgage, business, education loans
- **cards**: Debit and credit cards
- **wealth_management_accounts**: Investment portfolios

### Transaction Data
- **card_transactions**: POS and online purchases
- **wire_transfers**: Domestic and international transfers
- **bill_payments**: Utility and service payments
- **investment_transactions**: Stock/bond/ETF trades
- **atm_transactions**: ATM withdrawals and deposits
- **loan_payments**: Monthly loan repayments

## Data Coherence Features

### Email-Name Matching

The generator ensures customer emails are derived from their actual names:

```
Andrew Hill → andrew.hill@yahoo.com
Catherine Richardson → catherine.richardson@outlook.com
Robert Anderson → robert.anderson@target.com (commercial)
```

**Implementation**:
- Retail customers get public email domains (gmail, yahoo, outlook)
- Commercial customers get corporate email domains (from corporate_domains.json)
- Email username is always `firstname.lastname`

### Merchant-Country Coherence

Merchants have realistic names matching their countries:

**US Transactions (95%)**:
- Restaurants: Olive Garden, Cheesecake Factory, Applebee's
- Retail: Target, Walmart, Best Buy, Macy's
- Gas Stations: Shell, Chevron, Exxon, BP
- Grocery: Whole Foods, Trader Joe's, Kroger
- Online: Amazon, eBay, Netflix, Spotify

**International Transactions (5%)**:
- Format: `International [Category] - [City]`
- Examples:
  - "International Retail - Tokyo" (Japan)
  - "International Grocery - Paris" (France)
  - "International Restaurants - Vancouver" (Canada)

### Geographic Consistency

All location data is coherent:
- City/State pairs are valid
- ZIP codes match the state
- Population-weighted city distribution (more NYC, less small towns)

Example:
```
City: Los Angeles
State: CA
ZIP: 90444 (valid LA ZIP range)
```

### Temporal Ordering

All transaction sequences maintain proper timing:

**Wire Transfers**:
```
initiated_at: 2023-09-26 08:37:18
completed_at: 2023-09-26 20:36:18  (same day for domestic)
```

**Investment Transactions**:
```
transaction_date: 2024-06-15 10:30:00
settlement_date: 2024-06-17 10:30:00  (T+2 settlement)
```

**Account Lifecycle**:
```
customer.created_at: 2022-10-05 00:21:43
account.opened_at: 2023-01-15 14:30:00  (after customer created)
```

## Realistic Distributions

### Customer Types

```json
{
  "retail": 80%,
  "commercial": 18%,
  "corporate": 2%
}
```

Actual: 78.7% retail, 21.3% commercial+corporate

### Transaction Geography

```json
{
  "US": 95%,
  "International": 5%
}
```

Actual: 94.9% US, 5.1% international

### Wire Transfer Amounts

- Distribution: Lognormal
- Mean: $16,913
- Range: $100 - $500,000
- Actual Mean: $16,767

### Wealth Management Accounts

- Distribution: Lognormal (biased higher)
- Mean: $367,420
- Range: $10,000 - $5,000,000
- Actual Mean: $373,630

### Education Loans

- Distribution: Lognormal (biased higher)
- Principal Mean: $81,613
- Outstanding balances reflect realistic paydown over time

## Configuration

### Schema JSON Format

```json
{
  "schema_version": "1.0",
  "description": "Banking schema description",
  "tables": {
    "customers": {
      "description": "Bank customers",
      "row_count": 2108,
      "columns": {
        "customer_type": {
          "type": "varchar(20)",
          "values": ["retail", "commercial", "corporate"],
          "distribution": {
            "retail": 0.80,
            "commercial": 0.18,
            "corporate": 0.02
          }
        }
      }
    }
  },
  "data_generation_period": {
    "start_date": "2020-01-01",
    "end_date": "2025-11-14"
  }
}
```

### Key Configuration Options

**Row Counts**: Specify how many rows to generate for each table
```json
"row_count": 2108
```

**Distributions**: Control value distributions for enum fields
```json
"distribution": {
  "retail": 0.80,
  "commercial": 0.20
}
```

**Date Range**: Set the time period for generated data
```json
"data_generation_period": {
  "start_date": "2020-01-01",
  "end_date": "2025-11-14"
}
```

## Advanced Usage

### Custom Merchant Names

Edit `assets/merchant_types.json` to add custom merchants:

```json
{
  "merchant_categories": [
    {
      "mcc": "5812",
      "description": "Restaurants",
      "major_brands": ["Your Custom Restaurant"]
    }
  ]
}
```

### Custom Name Distributions

Edit `assets/name_distributions.json` to use different name frequencies.

### Custom Corporate Domains

Edit `assets/corporate_domains.json` to add company email domains:

```json
{
  "domains": [
    {
      "domain": "yourcompany.com",
      "company": "Your Company Inc"
    }
  ]
}
```

## Loading Data

### Basic Load

```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
python scripts/load_banking_data.py
```

### Features

1. **Dependency-Aware Loading**: Tables loaded in correct order to satisfy foreign keys
2. **Performance Optimization**:
   - Tries COPY for fast bulk loading
   - Falls back to batch INSERT if COPY fails
   - Disables user triggers during load (if permitted)
3. **Validation**: Automatic referential integrity checks after load
4. **Error Handling**: Graceful handling of permission issues

### Troubleshooting

**Permission Denied for Triggers**:
The script handles this automatically by:
- Only disabling USER triggers (not system triggers)
- Continuing if trigger disabling fails
- Data still loads correctly due to dependency ordering

**COPY Command Fails**:
The script automatically falls back to batch INSERT.

**Connection Issues**:
Use the test script first:
```bash
python scripts/test_connection.py
```

## Data Quality Validation

After loading, verify data quality:

```sql
-- Email-name coherence
SELECT
    first_name,
    last_name,
    email,
    CASE
        WHEN LOWER(SPLIT_PART(email, '@', 1)) = LOWER(first_name || '.' || last_name)
        THEN 'Match'
        ELSE 'Mismatch'
    END as status
FROM customers
LIMIT 10;

-- Referential integrity
SELECT
    (SELECT COUNT(*) FROM accounts WHERE customer_id NOT IN (SELECT customer_id FROM customers)) as orphaned_accounts,
    (SELECT COUNT(*) FROM cards WHERE customer_id NOT IN (SELECT customer_id FROM customers)) as orphaned_cards;

-- Temporal ordering violations (should be 0)
SELECT COUNT(*)
FROM wire_transfers
WHERE completed_at IS NOT NULL
  AND completed_at < initiated_at;

-- Geographic distribution
SELECT
    merchant_country,
    COUNT(*),
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) as percentage
FROM card_transactions
GROUP BY merchant_country
ORDER BY COUNT(*) DESC;
```

## Performance

### Generation Performance

- **2,108 customers**: <1 second
- **85,000 card transactions**: ~10 seconds
- **Total 161K rows**: ~30-60 seconds

### Loading Performance

- **COPY method**: 10-30 seconds for 161K rows
- **INSERT method**: 1-3 minutes for 161K rows

## Example Queries

### Top Customers by Transaction Volume

```sql
SELECT
    c.first_name,
    c.last_name,
    c.customer_type,
    COUNT(ct.transaction_id) as tx_count,
    SUM(ct.transaction_amount) as total_spent
FROM customers c
JOIN cards ca ON c.customer_id = ca.customer_id
JOIN card_transactions ct ON ca.card_id = ct.card_id
WHERE ct.auth_response = 'approved'
GROUP BY c.customer_id, c.first_name, c.last_name, c.customer_type
ORDER BY total_spent DESC
LIMIT 10;
```

### Average Loan Balances by Type

```sql
SELECT
    loan_type,
    COUNT(*) as loan_count,
    AVG(outstanding_balance) as avg_balance,
    AVG(principal_amount) as avg_principal,
    AVG(interest_rate) as avg_rate
FROM loans
WHERE loan_status = 'active'
GROUP BY loan_type
ORDER BY avg_balance DESC;
```

### Monthly Transaction Trends

```sql
SELECT
    DATE_TRUNC('month', transaction_date) as month,
    COUNT(*) as tx_count,
    COUNT(CASE WHEN auth_response = 'approved' THEN 1 END) as approved,
    COUNT(CASE WHEN auth_response = 'declined' THEN 1 END) as declined,
    SUM(CASE WHEN auth_response = 'approved' THEN transaction_amount ELSE 0 END) as total_amount
FROM card_transactions
GROUP BY month
ORDER BY month DESC
LIMIT 12;
```

## Best Practices

1. **Start Small**: Generate 1,000 rows first to validate schema and configuration
2. **Validate Early**: Check data quality on small datasets before scaling up
3. **Use Test Connection**: Always run `test_connection.py` before loading
4. **Monitor Progress**: The generator prints progress every 1,000-10,000 rows
5. **Customize Distributions**: Edit the schema JSON to match your specific needs
6. **Check Coherence**: Validate email-name matching, merchant-country matching after generation

## Integration with Existing Scripts

The banking data generator is compatible with the existing skill infrastructure:

- Uses same name distributions (`name_distributions.json`)
- Uses same location generator (`merchant_types.json`)
- Compatible with `create_postgres_schema.py` for schema generation
- Works with existing constraint engine (if needed)

## Summary

The enhanced banking data generator provides:

✅ 161K+ rows of production-ready data
✅ 100% email-name coherence
✅ 100% merchant-country coherence
✅ 100% referential integrity
✅ 0 temporal violations
✅ Realistic distributions matching real banking patterns
✅ Fast generation (~1 minute)
✅ Fast loading (10-30 seconds with COPY)
✅ Well-documented and easy to customize

Perfect for demos, development, testing, and training with realistic banking data.
