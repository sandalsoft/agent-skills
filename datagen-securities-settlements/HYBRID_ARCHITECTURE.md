# Hybrid PostgreSQL + MongoDB Architecture

## Overview

The Securities Settlements Data Generator uses a **hybrid database architecture**:

- **PostgreSQL**: Core settlement data (trades, securities, brokers, investors)
- **MongoDB** (`fails_db`): Settlement fails tracking with exceptions

This separation allows:
- Relational integrity for core settlement workflows
- Flexible document structure for fails and exceptions
- Optimized queries for each data type

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                  Data Generation Pipeline                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │  generate_all_data.py         │
              │  (Master Orchestrator)        │
              └───────────────────────────────┘
                      │               │
        ┌─────────────┘               └─────────────┐
        ▼                                           ▼
┌──────────────────┐                    ┌──────────────────────┐
│   PostgreSQL     │                    │     MongoDB          │
│   Data Gen       │                    │   Export Script      │
│                  │                    │                      │
│ • Broker-dealers │                    │ • Transform fails    │
│ • Investors      │                    │ • Create exceptions  │
│ • Securities     │                    │ • Aggregate stats    │
│ • Trades         │                    │                      │
│ • SSI            │                    └──────────────────────┘
│ • Settlements    │                              │
└──────────────────┘                              │
        │                                         │
        ▼                                         ▼
  ./data/postgres/                       ./data/mongodb/
  ├── broker_dealers.csv                 └── fails_db/
  ├── investors.csv                          ├── Fails.json
  ├── securities.csv                         └── Statistics.json
  ├── trades.csv
  ├── settlement_instructions.csv
  └── settlements.csv
```

## Database Schemas

### PostgreSQL Schema (Core Settlement Data)

**6 Tables** - Relational data with strong referential integrity:

1. **broker_dealers** - Market participants with DTC numbers
2. **investors** - Institutional and retail investors
3. **securities** - Equities with CUSIP/ISIN identifiers
4. **trades** - Trade executions
5. **settlement_instructions** - DVP/RVP/FOP instructions
6. **settlements** - Settlement attempts and outcomes

**Removed Tables** (moved to MongoDB):
- ~~settlement_fails~~ → MongoDB `Fails` collection
- ~~fail_charges~~ → Embedded in `Fails` documents

### MongoDB Schema (Fails Database)

**Database**: `fails_db`

**2 Collections** - Document-based fail tracking:

#### 1. Fails Collection

Stores detailed fail records with nested exceptions:

```json
{
  "id": "68f24d98e703adb2ac88306d",
  "last_update_time": "2025-10-18T11:28:58.812Z",
  "expiration_time": "9999-01-31T00:00:00Z",
  "aggregate_id": "BBC1L7T7H",
  "state": {
    "trade_id": "BBC1L7T7H",
    "trade_reference": "TRD85007641",
    "trade_date": "2025-10-16",
    "trade_product": "Receivesecurities",
    "trade_status": "OPEN",
    "settlement_system": "NY",
    "settlement_region": "NORTH_AMERICA",
    "market": "DTC",
    "fail_id": "840dc593-1acf-4466-b640-05cc61c9297d",
    "fail_type": "PENDING",
    "fail_status": "OPEN",
    "fail_category": "insufficient_securities",
    "fail_reason": "Securities pledged or encumbered",
    "failing_party": "seller",
    "fail_quantity": 150751,
    "fail_value": 46414186.76,
    "fail_age_days": 1,
    "total_charges": 16970.34,
    "exceptions": [
      {
        "actionable": true,
        "exception_status": "UNRESOLVED",
        "exception_reason": "Securities pledged or encumbered",
        "legacy_exception_type": "FAI"
      }
    ]
  }
}
```

**Key Fields**:
- `id`: Unique MongoDB document ID
- `aggregate_id`: Groups related fails
- `state.trade_id`: References PostgreSQL `trades` table
- `state.fail_status`: OPEN, RESOLVED, BUY_IN_INITIATED, CLOSED_OUT
- `state.exceptions[]`: Array of exception records

**Indexes**:
- `id` (unique)
- `aggregate_id`
- `state.trade_id` (cross-database reference)
- `state.fail_id` (unique)
- `state.fail_status`
- `state.market`
- `state.fail_age_days`

#### 2. Statistics Collection

Aggregated fail statistics by CUSIP, counterparty, and market:

```json
{
  "id": "691f6d9e848dóc8080ccd621",
  "cusip": "917288BK7",
  "counter_party_account_number": "027333335",
  "type": "MS_ACTION",
  "market": "DTC",
  "settlement_category": null,
  "fail_count": 5,
  "total_fail_value": 1250000.00,
  "avg_fail_age_days": 8.4,
  "last_updated": "2025-10-18T11:30:00Z"
}
```

**Key Fields**:
- `cusip`: Security identifier
- `counter_party_account_number`: Counterparty account
- `type`: MS_ACTION, CP_ACTION, SYSTEMIC
- `fail_count`: Number of fails
- `total_fail_value`: Aggregate fail value
- `avg_fail_age_days`: Average aging

**Indexes**:
- `id` (unique)
- `cusip`
- `market`
- `type`
- `counter_party_account_number`

## Cross-Database Relationships

### PostgreSQL → MongoDB

```
PostgreSQL.trades.trade_id
        ↓ (referenced by)
MongoDB.Fails.state.trade_id
```

**Usage**: Join PostgreSQL trade data with MongoDB fail details

**Example Query**:
```javascript
// MongoDB: Get fail
const fail = db.Fails.findOne({'state.fail_status': 'OPEN'});
const tradeId = fail.state.trade_id;

// PostgreSQL: Get trade details
SELECT * FROM trades WHERE trade_id = '${tradeId}';
```

### PostgreSQL → MongoDB (via CUSIP)

```
PostgreSQL.securities.cusip
        ↓ (referenced by)
MongoDB.Statistics.cusip
```

**Usage**: Analyze fails by security

**Example Query**:
```javascript
// MongoDB: Get statistics for a security
db.Statistics.find({cusip: '917288BK7'});
```

## Data Generation Workflow

### Step 1: Generate All Data

```bash
python src/generate_all_data.py \
    --postgres-schema assets/settlements_postgres_schema.json \
    --output-dir ./data \
    --fail-rate 0.15 \
    --seed 42
```

**This does**:
1. Generates PostgreSQL CSV files
2. Exports fails to MongoDB JSON format
3. Creates statistics aggregations
4. Outputs to `./data/` directory

### Step 2: Load PostgreSQL Data

```bash
# Create schema
python src/create_postgres_schema.py \
    assets/settlements_postgres_schema.json \
    --output ./data/schema.sql

# Create database and tables
psql -d settlements_db -f ./data/schema.sql

# Load data
python src/insert_data.py \
    assets/settlements_postgres_schema.json \
    ./data/postgres \
    -d settlements_db -U user -W password
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

# Create indexes
mongo fails_db --eval '
    db.Fails.createIndex({"id": 1}, {unique: true});
    db.Fails.createIndex({"state.trade_id": 1});
    db.Fails.createIndex({"state.fail_status": 1});
    db.Statistics.createIndex({"cusip": 1});
'
```

## Query Examples

### Cross-Database Queries

#### Example 1: Get Failed Trade Details

```javascript
// MongoDB: Find fails
const fails = db.Fails.find({'state.fail_status': 'OPEN'}).toArray();

// Extract trade IDs
const tradeIds = fails.map(f => f.state.trade_id);

// PostgreSQL: Get trade details
SELECT
    t.trade_id,
    t.trade_reference,
    s.ticker,
    s.cusip,
    t.quantity,
    t.gross_amount,
    t.trade_date,
    t.settlement_date
FROM trades t
JOIN securities s ON t.security_id = s.security_id
WHERE t.trade_id = ANY(ARRAY['...', '...']::uuid[]);
```

#### Example 2: Fail Analysis by Security

```sql
-- PostgreSQL: Get securities with high fail rates
WITH failed_settlements AS (
    SELECT trade_id
    FROM settlements
    WHERE settlement_status = 'failed'
)
SELECT
    s.ticker,
    s.cusip,
    s.security_name,
    COUNT(*) as fail_count
FROM failed_settlements fs
JOIN trades t ON fs.trade_id = t.trade_id
JOIN securities s ON t.security_id = s.security_id
GROUP BY s.ticker, s.cusip, s.security_name
ORDER BY fail_count DESC
LIMIT 10;
```

```javascript
// MongoDB: Get detailed fail info for those securities
db.Statistics.aggregate([
    {$match: {cusip: {$in: ['917288BK7', ...]}}},
    {$group: {
        _id: '$cusip',
        total_fails: {$sum: '$fail_count'},
        total_value: {$sum: '$total_fail_value'},
        avg_age: {$avg: '$avg_fail_age_days'}
    }},
    {$sort: {total_fails: -1}}
]);
```

#### Example 3: Exception Tracking

```javascript
// MongoDB: Find unresolved exceptions
db.Fails.find({
    'state.exceptions.exception_status': 'UNRESOLVED',
    'state.fail_age_days': {$gte: 10}
}, {
    'state.trade_id': 1,
    'state.fail_reason': 1,
    'state.exceptions': 1,
    'state.fail_age_days': 1
});
```

## Why Hybrid Architecture?

### Advantages

**PostgreSQL (Core Settlement Data)**
✅ Strong referential integrity for trades and settlements
✅ ACID transactions for critical financial data
✅ Complex joins across related tables
✅ Standard SQL reporting and analytics

**MongoDB (Fails and Exceptions)**
✅ Flexible schema for evolving fail reasons
✅ Nested documents for exceptions (no separate join table)
✅ Fast lookups by fail status and aging
✅ Easy to add new exception types without schema changes

### Trade-offs

**Consistency**: Cross-database joins require application logic
**Transactions**: Cannot use distributed transactions across databases
**Complexity**: Two databases to manage and maintain

**Solution**: Use `trade_id` as the linking key between systems

## Deployment Considerations

### Docker Compose Example

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:18
    environment:
      POSTGRES_DB: settlements_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - ./data/schema.sql:/docker-entrypoint-initdb.d/schema.sql
      - pg_data:/var/lib/postgresql/data

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  pg_data:
  mongo_data:
```

### Load Data

```bash
# After containers are running
docker-compose up -d

# Load PostgreSQL
docker exec -it <postgres_container> psql -U user -d settlements_db -f /docker-entrypoint-initdb.d/schema.sql

# Load MongoDB
docker cp ./data/mongodb/fails_db/Fails.json <mongo_container>:/tmp/
docker exec -it <mongo_container> mongoimport --db fails_db --collection Fails --file /tmp/Fails.json --jsonArray
```

## Performance Optimization

### PostgreSQL

```sql
-- Create additional indexes
CREATE INDEX idx_settlements_status ON settlements(settlement_status);
CREATE INDEX idx_trades_date ON trades(trade_date);
CREATE INDEX idx_securities_market ON securities(market);

-- Analyze tables
ANALYZE trades;
ANALYZE settlements;
```

### MongoDB

```javascript
// Create compound indexes
db.Fails.createIndex({'state.market': 1, 'state.fail_status': 1});
db.Fails.createIndex({'state.fail_start_date': 1, 'state.fail_age_days': -1});
db.Statistics.createIndex({'market': 1, 'type': 1});

// Analyze query performance
db.Fails.find({'state.fail_status': 'OPEN'}).explain('executionStats');
```

## Monitoring

### Key Metrics

**PostgreSQL**:
- Settlement success rate: `SELECT COUNT(*) WHERE settlement_status = 'settled' / COUNT(*)`
- Average settlement time
- Trade volume by market

**MongoDB**:
- Active fails count: `db.Fails.count({'state.fail_status': 'OPEN'})`
- Average fail age: `db.Statistics.aggregate([{$group: {_id: null, avg: {$avg: '$avg_fail_age_days'}}}])`
- Fails by category

### Alerts

- Fail rate exceeds 20%
- Average fail age > 10 days
- Chronic fails (21+ days) increasing

## Future Enhancements

1. **Real-time sync**: Stream PostgreSQL changes to MongoDB
2. **GraphQL API**: Unified query layer across both databases
3. **Event sourcing**: Use MongoDB for event log, PostgreSQL for projections
4. **Analytics**: Time-series collections for trend analysis
