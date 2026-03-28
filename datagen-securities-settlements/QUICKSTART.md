# Quick Start Guide

## Prerequisites

- Python 3.7+
- PostgreSQL 12+ (recommended: PostgreSQL 18)
- MongoDB 4.4+ (recommended: MongoDB 7)
- `pip install psycopg2-binary pymongo` (optional for MongoDB loader)

## Generate Data (3 Steps)

### Step 1: Generate All Data

```bash
cd ~/.claude/skills/datagen-securities-settlements

# Generate with default settings (500K trades, 15% fail rate)
python src/generate_all_data.py \
    --postgres-schema assets/settlements_postgres_schema.json \
    --output-dir ./data

# Or generate smaller sample for testing (1K trades)
python src/generate_all_data.py \
    --postgres-schema /tmp/small_settlement_schema.json \
    --output-dir ./data \
    --fail-rate 0.15 \
    --seed 42
```

**Output**:
```
./data/
├── postgres/
│   ├── broker_dealers.csv
│   ├── investors.csv
│   ├── securities.csv
│   ├── trades.csv
│   ├── settlement_instructions.csv
│   └── settlements.csv
└── mongodb/
    └── fails_db/
        ├── Fails.json
        └── Statistics.json
```

### Step 2: Load PostgreSQL Data

```bash
# Create schema
python src/create_postgres_schema.py \
    assets/settlements_postgres_schema.json \
    --output ./data/schema.sql

# Create database
createdb settlements_db

# Create tables
psql -d settlements_db -f ./data/schema.sql

# Load data
python src/insert_data.py \
    assets/settlements_postgres_schema.json \
    ./data/postgres \
    -d settlements_db -U $USER
```

**Verify**:
```sql
psql -d settlements_db -c "
SELECT
    table_name,
    (xpath('/row/cnt/text()', xml_count))[1]::text::int as row_count
FROM (
    SELECT
        table_name,
        query_to_xml(format('select count(*) as cnt from %I', table_name), false, true, '') as xml_count
    FROM information_schema.tables
    WHERE table_schema = 'public'
) t
ORDER BY row_count DESC;
"
```

### Step 3: Load MongoDB Data

```bash
# Import Fails collection
mongoimport \
    --db fails_db \
    --collection Fails \
    --file ./data/mongodb/fails_db/Fails.json \
    --jsonArray

# Import Statistics collection
mongoimport \
    --db fails_db \
    --collection Statistics \
    --file ./data/mongodb/fails_db/Statistics.json \
    --jsonArray
```

**Verify**:
```bash
mongosh fails_db --eval "
print('Fails collection:', db.Fails.countDocuments({}));
print('Statistics collection:', db.Statistics.countDocuments({}));
print('');
print('Sample Fail:');
printjson(db.Fails.findOne());
"
```

## Query Examples

### PostgreSQL Queries

```sql
-- Get all failed settlements
SELECT
    s.settlement_reference,
    t.trade_reference,
    t.trade_date,
    s.settlement_status,
    t.gross_amount
FROM settlements s
JOIN trades t ON s.trade_id = t.trade_id
WHERE s.settlement_status = 'failed'
LIMIT 10;

-- Settlement success rate by market
SELECT
    sec.market,
    COUNT(*) as total_settlements,
    SUM(CASE WHEN s.settlement_status = 'settled' THEN 1 ELSE 0 END) as successful,
    ROUND(100.0 * SUM(CASE WHEN s.settlement_status = 'settled' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate_pct
FROM settlements s
JOIN trades t ON s.trade_id = t.trade_id
JOIN securities sec ON t.security_id = sec.security_id
GROUP BY sec.market
ORDER BY success_rate_pct DESC;

-- Top securities by trade volume
SELECT
    s.ticker,
    s.cusip,
    s.security_name,
    COUNT(*) as trade_count,
    SUM(t.gross_amount) as total_value
FROM trades t
JOIN securities s ON t.security_id = s.security_id
GROUP BY s.ticker, s.cusip, s.security_name
ORDER BY total_value DESC
LIMIT 10;
```

### MongoDB Queries

```javascript
// Connect to MongoDB
mongosh fails_db

// Count fails by status
db.Fails.aggregate([
    {$group: {
        _id: '$state.fail_status',
        count: {$sum: 1}
    }},
    {$sort: {count: -1}}
])

// Find chronic fails (21+ days)
db.Fails.find({
    'state.fail_age_days': {$gte: 21},
    'state.fail_status': 'OPEN'
}, {
    'state.trade_id': 1,
    'state.fail_reason': 1,
    'state.fail_age_days': 1,
    'state.fail_value': 1
}).sort({'state.fail_age_days': -1})

// Get top securities by fail count
db.Statistics.aggregate([
    {$group: {
        _id: '$cusip',
        total_fails: {$sum: '$fail_count'},
        total_value: {$sum: '$total_fail_value'},
        avg_age: {$avg: '$avg_fail_age_days'}
    }},
    {$sort: {total_fails: -1}},
    {$limit: 10}
])

// Find unresolved exceptions
db.Fails.find({
    'state.exceptions.exception_status': 'UNRESOLVED'
}, {
    'state.trade_reference': 1,
    'state.fail_reason': 1,
    'state.exceptions': 1
}).limit(10)
```

### Cross-Database Query (Application Code)

```python
import psycopg2
from pymongo import MongoClient

# Connect to both databases
pg_conn = psycopg2.connect("dbname=settlements_db user=postgres")
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['fails_db']

# Get fails from MongoDB
fails = mongo_db.Fails.find({'state.fail_status': 'OPEN'})

# Extract trade IDs
trade_ids = [fail['state']['trade_id'] for fail in fails]

# Get trade details from PostgreSQL
pg_cursor = pg_conn.cursor()
pg_cursor.execute("""
    SELECT
        t.trade_id,
        t.trade_reference,
        s.ticker,
        s.cusip,
        t.quantity,
        t.gross_amount
    FROM trades t
    JOIN securities s ON t.security_id = s.security_id
    WHERE t.trade_id = ANY(%s)
""", (trade_ids,))

# Combine results
for row in pg_cursor.fetchall():
    trade_id, trade_ref, ticker, cusip, qty, amount = row
    print(f"{trade_ref} | {ticker} ({cusip}) | {qty} shares | ${amount:,.2f}")
```

## Configuration Options

### Adjust Row Counts

Edit schema JSON file:

```json
{
  "tables": {
    "trades": {
      "row_count": 10000  // Change from 500000 to 10000
    }
  }
}
```

### Adjust Fail Rate

```bash
# Higher fail rate (30% - stress test)
python src/generate_all_data.py ... --fail-rate 0.30

# Lower fail rate (5% - optimistic)
python src/generate_all_data.py ... --fail-rate 0.05
```

### Reproducible Data

```bash
# Use same seed for consistent data
python src/generate_all_data.py ... --seed 42
```

## Troubleshooting

### PostgreSQL: Foreign Key Violations

**Issue**: `ERROR: insert or update on table violates foreign key constraint`

**Solution**: Load tables in dependency order (handled by insert_data.py automatically)

### MongoDB: Duplicate Key Error

**Issue**: `E11000 duplicate key error`

**Solution**: Drop and recreate collections:
```bash
mongosh fails_db --eval "
db.Fails.drop();
db.Statistics.drop();
"
# Then re-import
```

### Generation Too Slow

**Issue**: Generating 500K trades takes too long

**Solution**: Start with smaller dataset for testing:
- Reduce row counts in schema JSON
- Use smaller test schema (1K-10K trades)
- Generate in stages

### Missing Files

**Issue**: `FileNotFoundError: settlement_fails.csv`

**Solution**: Ensure PostgreSQL generation completed successfully. Check for errors in Step 1.

## Next Steps

1. **Explore Data**: Run sample queries above
2. **Create Views**: Build analytical views for common queries
3. **Add Indexes**: Optimize for your query patterns
4. **Build Dashboard**: Visualize settlement metrics
5. **Scale Up**: Generate full dataset (500K trades)

## Resources

- Full Architecture: `HYBRID_ARCHITECTURE.md`
- Schema Reference: `references/schema-format.md`
- Fail Patterns: `references/settlement-fail-patterns.md`
- README: `README.md`
