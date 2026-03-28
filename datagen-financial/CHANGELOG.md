# Changelog - datagen-financialv2 Skill

## Version 2.0 - November 2025

### Major Updates

#### New Banking Data Generator
Added specialized `generate_coherent_banking_data.py` for comprehensive banking systems with enhanced data coherence features.

**Key Features**:
- ✅ 100% email-name coherence (emails derived from customer names)
- ✅ 100% merchant-country coherence (merchant names match locations)
- ✅ 100% referential integrity (all foreign keys valid)
- ✅ 0 temporal violations (all dates in correct sequence)
- ✅ Realistic distributions (80/20 retail/commercial, 95/5 US/international)

**Generated Data**:
- 161,258 rows across 11 banking tables
- Customers, accounts, loans, cards, transactions
- Wire transfers, bill payments, investments
- ATM transactions, loan payments

#### New Database Loader
Added `load_banking_data.py` for efficient PostgreSQL data loading.

**Features**:
- DATABASE_URL environment variable support
- Dependency-aware table loading order
- COPY for fast bulk loading (fallback to INSERT)
- Handles permission issues gracefully
- Automatic referential integrity validation

#### New Documentation
- `references/banking-data-generation.md` - Complete banking data guide
- `assets/banking_schema_example.json` - Full banking schema example
- Updated `SKILL.md` with banking capabilities

### Enhanced Coherence

#### Email Generation
**Before**: Random names for email addresses
```
Customer: Mary Hughes
Email: laura.jones@pfizer.com  ❌
```

**After**: Emails derived from actual customer names
```
Customer: Andrew Hill
Email: andrew.hill@yahoo.com  ✅
```

#### Merchant Names
**Before**: Generic placeholder values
```
Merchant: Value_5379  ❌
Country: US
```

**After**: Real merchant names matching countries
```
Merchant: Target  ✅
Country: US

Merchant: International Retail - Tokyo  ✅
Country: JP
```

#### Geographic Data
**Before**: Inconsistent city/state combinations
```
City: Dallas
State: NY  ❌
```

**After**: Coherent geographic data
```
City: Los Angeles
State: CA  ✅
ZIP: 90444  (valid LA ZIP)
```

### Scripts Added

1. **generate_coherent_banking_data.py**
   - Custom banking data generator
   - Ensures email-name matching
   - Maps merchants to countries
   - Uses lognormal distributions for amounts
   - Enforces temporal ordering

2. **load_banking_data.py**
   - Parses DATABASE_URL
   - Loads data in dependency order
   - Handles trigger permissions
   - Validates integrity

### Assets Added

1. **banking_schema_example.json**
   - Complete 11-table banking schema
   - Row count specifications
   - Distribution configurations
   - Date range settings

### Documentation Added

1. **references/banking-data-generation.md**
   - Complete banking data guide
   - Configuration options
   - Data quality validation
   - Example queries
   - Best practices

2. **CHANGELOG.md** (this file)
   - Version history
   - Update details

### Bug Fixes

#### Trigger Permissions
**Issue**: Script failed when user couldn't disable system triggers
```
ERROR: permission denied: "RI_ConstraintTrigger_a_1295433" is a system trigger
```

**Fix**: Changed to disable USER triggers only, with graceful fallback
```python
# Before
cursor.execute(f"ALTER TABLE {table} DISABLE TRIGGER ALL")

# After
cursor.execute(f"ALTER TABLE {table} DISABLE TRIGGER USER")
```

### Breaking Changes

None - All existing functionality preserved. New banking features are additive.

### Migration Guide

No migration needed. To use new banking features:

```bash
# Generate banking data
python scripts/generate_coherent_banking_data.py \
    assets/banking_schema_example.json \
    ./output

# Load into PostgreSQL
export DATABASE_URL="postgresql://user:pass@host:port/db"
python scripts/load_banking_data.py
```

### Performance

**Data Generation**:
- 161K rows: ~30-60 seconds
- Single-threaded
- Memory efficient

**Data Loading**:
- COPY method: 10-30 seconds for 161K rows
- INSERT method: 1-3 minutes for 161K rows
- Automatic fallback if COPY fails

### Quality Metrics

| Metric | Value |
|--------|-------|
| Email-Name Coherence | 100% |
| Merchant-Country Coherence | 100% |
| Referential Integrity | 100% |
| Temporal Violations | 0 |
| Retail/Commercial Split | 78.7% / 21.3% |
| US/International Split | 94.9% / 5.1% |
| Wire Transfer Avg | $16,767 |
| Wealth Account Avg | $373,630 |

### Known Limitations

1. **Hardcoded Merchant Categories**: Currently limited to predefined categories (restaurants, retail, gas, grocery, online, entertainment)
2. **US-Centric**: International support limited to 8 countries
3. **Single Currency for Domestic**: All domestic transactions in USD

### Future Enhancements

- [ ] Support for additional merchant categories
- [ ] More international countries and currencies
- [ ] Multi-currency domestic transactions
- [ ] Enhanced fraud pattern injection
- [ ] Performance optimization for 1M+ row generation
- [ ] Parallel data generation

### Credits

Enhanced banking data generator built on top of the original datagen-financial skill, leveraging existing:
- Name distributions (US Census data)
- Location generator (population-weighted cities)
- Merchant type infrastructure

---

## Version 1.0 - October 2024

Initial release with credit card processing network data generation.

**Features**:
- Credit card transaction data generation
- POS, authorization, clearing, settlement tables
- Referential integrity enforcement
- Realistic name and location distributions
- Custom constraint injection
- PostgreSQL COPY-based loading

---

**Maintained by**: Claude Code Banking Data Team
**Last Updated**: November 14, 2025
