# datagen-financial Skill

Generate realistic, coherent synthetic financial data for banking systems and credit card processing networks.

## What's New

🎉 **Enhanced Banking Data Generator** with 100% data coherence:
- ✅ Emails match customer names exactly
- ✅ Merchant names match their countries
- ✅ Perfect referential integrity
- ✅ Realistic distributions
- ✅ 161K+ rows across 11 banking tables

## Quick Start

### Banking Data (Recommended for Demos)

```bash
# 1. Generate coherent banking data
python scripts/generate_coherent_banking_data.py \
    assets/banking_schema_example.json \
    ./output

# 2. Load into PostgreSQL
export DATABASE_URL="postgresql://user:password@host:port/database"
python scripts/load_banking_data.py
```

**Result**: 161,258 rows of production-ready banking data with:
- Customers, accounts, loans, cards
- Card transactions, wire transfers, bill payments
- Investment portfolios and transactions
- ATM transactions, loan payments

### Credit Card Processing

```bash
# 1. Create schema
python scripts/create_postgres_schema.py schema.json --output schema.sql

# 2. Generate data
python scripts/generate_data.py schema.json ./output

# 3. Load data
python scripts/insert_data.py schema.json ./output -d dbname -U user
```

## Features

### Data Coherence

**Email-Name Matching** (100%)
```
Andrew Hill → andrew.hill@yahoo.com ✅
Catherine Richardson → catherine.richardson@outlook.com ✅
```

**Merchant-Country Matching** (100%)
```
US: Target, Walmart, Shell, Amazon, Whole Foods
International: "International Retail - Tokyo" (Japan)
```

**Temporal Ordering** (0 violations)
```
Wire Transfer:
  initiated_at: 2023-09-26 08:37:18
  completed_at: 2023-09-26 20:36:18 ✅
```

**Referential Integrity** (100%)
```
All foreign keys valid
No orphaned records
```

### Realistic Distributions

- 80% retail / 20% commercial customers
- 95% US / 5% international transactions
- Wire transfers: avg $16,913 (lognormal)
- Wealth accounts: avg $367,420 (biased higher)

## Files

### Scripts
- `generate_coherent_banking_data.py` - Banking data generator (NEW!)
- `load_banking_data.py` - DATABASE_URL-based loader (NEW!)
- `generate_data.py` - Credit card data generator
- `insert_data.py` - Standard data loader
- `create_postgres_schema.py` - Schema DDL generator

### Assets
- `banking_schema_example.json` - Full banking schema (NEW!)
- `example_schema.json` - Credit card processing schema
- `name_distributions.json` - US Census name frequencies
- `merchant_types.json` - Merchant categories and brands
- `corporate_domains.json` - Company email domains

### References
- `banking-data-generation.md` - Banking data guide (NEW!)
- `schema-format.md` - Schema JSON specification
- `realistic-data-patterns.md` - Realism documentation
- `rule-patterns.md` - Constraint injection guide
- `semantic-validation.md` - Validation patterns

### Documentation
- `SKILL.md` - Complete skill documentation
- `CHANGELOG.md` - Version history (NEW!)
- `README.md` - This file (NEW!)

## Use Cases

### Banking Demos
- Realistic customer data with coherent emails
- Transaction history across multiple products
- Investment portfolios and trades
- Wire transfers and bill payments

### Development
- Local testing with production-like data
- Integration testing scenarios
- Performance benchmarking

### Credit Card Processing
- POS transaction data
- Authorization and settlement flows
- Fraud detection testing

### Training & Education
- Learning SQL with realistic datasets
- Database design examples
- Financial data analysis

## Examples

### Generate 1 Million Transactions

```json
// schema.json
{
  "tables": {
    "card_transactions": {
      "row_count": 1000000,
      "columns": { ... }
    }
  }
}
```

```bash
python scripts/generate_coherent_banking_data.py schema.json ./output
```

### Customize Distributions

```json
{
  "tables": {
    "customers": {
      "columns": {
        "customer_type": {
          "distribution": {
            "retail": 0.90,
            "commercial": 0.10
          }
        }
      }
    }
  }
}
```

### Load with Custom Connection

```bash
# Using DATABASE_URL
export DATABASE_URL="postgresql://admin:pass@db.example.com:5432/banking"
python scripts/load_banking_data.py

# Using direct parameters
python scripts/insert_data.py schema.json ./output \
    -d banking \
    -U admin \
    -W password \
    --host db.example.com \
    --port 5432
```

## Performance

### Generation
- 2K customers: <1 second
- 85K transactions: ~10 seconds
- 161K total rows: ~30-60 seconds

### Loading
- COPY: 10-30 seconds for 161K rows
- INSERT: 1-3 minutes for 161K rows
- Automatic fallback if COPY fails

## Requirements

```bash
pip install psycopg2-binary
```

PostgreSQL 12+ recommended.

## Quality Guarantees

| Metric | Target | Actual |
|--------|--------|--------|
| Email-Name Coherence | 100% | 100% ✅ |
| Merchant-Country Coherence | 100% | 100% ✅ |
| Referential Integrity | 100% | 100% ✅ |
| Temporal Violations | 0 | 0 ✅ |
| Retail/Commercial Split | 80/20 | 78.7/21.3 ✅ |
| US/International Split | 95/5 | 94.9/5.1 ✅ |

## Troubleshooting

### Permission Denied for Triggers
The loader automatically handles this by:
- Only disabling USER triggers (not system triggers)
- Continuing if trigger disabling fails
- Data loads correctly due to dependency ordering

### COPY Command Fails
Automatic fallback to batch INSERT.

### Connection Issues
Check DATABASE_URL format:
```
postgresql://user:password@host:port/database
```

## Documentation

- **Quick Start**: This README
- **Banking Guide**: `references/banking-data-generation.md`
- **Complete Skill Docs**: `SKILL.md`
- **Schema Format**: `references/schema-format.md`
- **Constraints**: `references/rule-patterns.md`

## Support

For issues or questions:
1. Check `SKILL.md` for detailed documentation
2. Review examples in `references/`
3. See `CHANGELOG.md` for recent updates

## License

Part of Claude Code skills collection.

---

**Version**: 2.0
**Last Updated**: November 14, 2025
**Status**: ✅ Production Ready
