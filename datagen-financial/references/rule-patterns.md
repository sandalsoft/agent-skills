# Constraint Rules and Business Logic

This document describes how to inject custom business logic and constraints into the data generation process.

## Overview

Constraints allow you to enforce business rules, data quality patterns, and domain-specific logic that goes beyond basic referential integrity.

## Constraint File Format

Constraints are defined in a JSON or YAML file passed to the generator via the `--constraints` flag.

### JSON Format

```json
{
  "spatial": [ ... ],
  "temporal": [ ... ],
  "data_quality": [ ... ],
  "relational": [ ... ],
  "custom": [ ... ]
}
```

### YAML Format

```yaml
spatial:
  - ...
temporal:
  - ...
data_quality:
  - ...
relational:
  - ...
custom:
  - ...
```

## Constraint Types

### 1. Spatial Constraints

Control geographic distribution and location-based rules.

#### Continental US Restriction

```json
"spatial": [
  {
    "entity": "pos_locations",
    "rule": "continental_us_only",
    "description": "All POS locations must be in continental US"
  }
]
```

This is the **default behavior**. To allow locations outside continental US:

```json
"spatial": [
  {
    "entity": "pos_locations",
    "rule": "allow_global",
    "countries": ["US", "CA", "MX"]
  }
]
```

#### City/Region Restrictions

```json
"spatial": [
  {
    "field": "merchants.city",
    "rule": "restrict_to_cities",
    "cities": ["New York", "Los Angeles", "Chicago"]
  }
]
```

#### Distance Constraints

```json
"spatial": [
  {
    "rule": "cardholder_merchant_max_distance",
    "max_distance_km": 100,
    "description": "Cardholder and merchant within 100km for non-ecommerce"
  }
]
```

### 2. Temporal Constraints

Control timing, sequencing, and rate limiting.

#### Missing Timestamp Fields

```json
"temporal": [
  {
    "field": "authorization_requests.requested_at",
    "rule": "never_missing",
    "enforcement": "hard"
  }
]
```

#### Transaction Rate Limits

```json
"temporal": [
  {
    "entity": "gas_station",
    "rule": "max_transactions_per_minute",
    "value": 25,
    "description": "Gas stations process max 25 tx/min"
  },
  {
    "entity": "fast_food",
    "rule": "max_transactions_per_minute",
    "value": 50,
    "description": "Fast food can process up to 50 tx/min"
  }
]
```

#### Business Hours

```json
"temporal": [
  {
    "entity": "retail_store",
    "rule": "business_hours",
    "hours": {
      "monday": ["09:00", "21:00"],
      "tuesday": ["09:00", "21:00"],
      "wednesday": ["09:00", "21:00"],
      "thursday": ["09:00", "21:00"],
      "friday": ["09:00", "22:00"],
      "saturday": ["10:00", "22:00"],
      "sunday": ["11:00", "19:00"]
    }
  }
]
```

#### Sequence Constraints

```json
"temporal": [
  {
    "rule": "transaction_lifecycle_sequence",
    "sequence": [
      "authorization_requests.requested_at",
      "clearing_records.cleared_at",
      "settlement_records.settled_at",
      "reconciliation_records.reconciled_at"
    ],
    "description": "Timestamps must progress in this order"
  }
]
```

### 3. Data Quality Constraints

Control missing data, outliers, and data quality issues.

#### Missing Data Rates

```json
"data_quality": [
  {
    "field": "authorization_requests.transaction_code",
    "rule": "missing_rate",
    "rate": 0.0002,
    "description": "Transaction code missing 0.02% of the time"
  },
  {
    "field": "cardholders.phone",
    "rule": "missing_rate",
    "rate": 0.05,
    "description": "Phone numbers missing 5% of the time"
  }
]
```

#### Outlier Generation

```json
"data_quality": [
  {
    "field": "authorization_requests.transaction_amount",
    "rule": "generate_outliers",
    "outlier_rate": 0.001,
    "outlier_range": [5000, 25000],
    "description": "0.1% of transactions are unusually high amounts"
  }
]
```

#### Data Corruption Simulation

```json
"data_quality": [
  {
    "field": "authorization_requests.card_number",
    "rule": "corrupt_data",
    "corruption_rate": 0.0001,
    "corruption_type": "digit_swap",
    "description": "Simulate occasional data entry errors"
  }
]
```

### 4. Relational Constraints

Enforce relationships and invariants between fields.

#### Hard Constraints (Always Enforced)

```json
"relational": [
  {
    "rule": "issuer.settlement_amount > acquirer.settlement_amount",
    "enforcement": "always",
    "description": "Issuer settlement must exceed acquirer (interchange)"
  },
  {
    "rule": "cards.expiration_date > current_date",
    "enforcement": "always",
    "description": "No expired cards in active transactions"
  }
]
```

#### Soft Constraints (Probabilistic)

```json
"relational": [
  {
    "rule": "authorization_requests.auth_response == 'approved'",
    "enforcement": "probabilistic",
    "probability": 0.87,
    "description": "87% of transactions are approved"
  }
]
```

#### Multi-Field Relationships

```json
"relational": [
  {
    "rule": "settlement_amount_calculation",
    "formula": "settlement_records.issuer_settlement_amount = authorization_requests.transaction_amount + clearing_records.interchange_fee + settlement_records.network_fee",
    "enforcement": "always",
    "description": "Settlement amount calculation"
  }
]
```

#### Conditional Constraints

```json
"relational": [
  {
    "rule": "decline_reason_required",
    "condition": "authorization_requests.auth_response == 'declined'",
    "then": "authorization_requests.decline_reason IS NOT NULL",
    "enforcement": "always"
  }
]
```

### 5. Custom Constraints

For complex logic that can't be expressed declaratively.

#### Python Function Reference

```json
"custom": [
  {
    "name": "validate_settlement_amounts",
    "script": "assets/custom_rules/settlement_validation.py",
    "function": "validate_settlement_amounts",
    "applies_to": ["settlement_records"],
    "description": "Custom settlement validation logic"
  }
]
```

#### Inline Python (Simple Cases)

```json
"custom": [
  {
    "name": "luhn_check",
    "code": "def validate(card_number): return luhn_checksum(card_number) % 10 == 0",
    "applies_to": ["cards.card_number"],
    "enforcement": "validation"
  }
]
```

## Constraint Enforcement Levels

### Hard Constraints (`enforcement: "always"`)

- MUST be satisfied for every record
- Generation fails if constraint cannot be met
- Used for critical business rules

Example: Settlement amounts, referential integrity

### Soft Constraints (`enforcement: "probabilistic"`)

- Satisfied according to specified probability
- Used for realistic distributions
- Generation continues even if individual records don't satisfy

Example: Approval rates, transaction patterns

### Validation Constraints (`enforcement: "validation"`)

- Applied after generation
- Records that fail validation are flagged (but not removed)
- Used for data quality checks

Example: Checksum validation, format validation

## Common Constraint Patterns

### Financial Domain

#### Credit Card Processing

```json
{
  "relational": [
    {
      "rule": "issuer_settlement_greater",
      "formula": "issuer.settlement_amount > acquirer.settlement_amount + 0.01",
      "enforcement": "always"
    },
    {
      "rule": "interchange_fee_percentage",
      "formula": "interchange_fee >= transaction_amount * 0.015 AND interchange_fee <= transaction_amount * 0.03",
      "enforcement": "always"
    },
    {
      "rule": "network_fee_range",
      "formula": "network_fee >= 0.10 AND network_fee <= 0.25",
      "enforcement": "always"
    }
  ],
  "data_quality": [
    {
      "field": "authorization_requests.auth_code",
      "rule": "missing_when_declined",
      "condition": "auth_response == 'declined'",
      "missing_rate": 1.0
    }
  ]
}
```

#### Fraud Detection Testing

```json
{
  "custom": [
    {
      "name": "inject_fraud_patterns",
      "rule": "velocity_fraud",
      "fraud_rate": 0.001,
      "pattern": {
        "same_card_multiple_locations": true,
        "time_window_minutes": 30,
        "min_distance_km": 500
      },
      "description": "Inject 0.1% fraud patterns for ML training"
    }
  ]
}
```

### E-Commerce Domain

```json
{
  "spatial": [
    {
      "field": "transactions.merchant_location",
      "rule": "ecommerce_no_location",
      "condition": "pos_entry_mode == 'ecommerce'",
      "set_to_null": true
    }
  ],
  "relational": [
    {
      "rule": "ecommerce_higher_decline_rate",
      "condition": "pos_entry_mode == 'ecommerce'",
      "then": "auth_response == 'approved'",
      "probability": 0.75,
      "description": "E-commerce has lower approval rate (75%)"
    }
  ]
}
```

### Regulatory Compliance

```json
{
  "data_quality": [
    {
      "field": "cardholders.ssn",
      "rule": "never_generate",
      "description": "Never generate SSNs for compliance"
    }
  ],
  "temporal": [
    {
      "field": "cardholders.created_at",
      "rule": "age_restriction",
      "min_age_years": 18,
      "description": "Cardholders must be 18+ at account creation"
    }
  ]
}
```

## Custom Python Scripts

For complex logic, create Python scripts in `assets/custom_rules/`:

### Example: Settlement Validation

```python
# assets/custom_rules/settlement_validation.py

import random

def validate_settlement_amounts(row, context):
    """
    Validate and adjust settlement amounts.
    
    Args:
        row: Dict containing current row data
        context: Dict with access to other table data
    
    Returns:
        Dict with adjusted row data
    """
    transaction_amount = row['transaction_amount']
    
    # Calculate interchange fee (1.5% - 3.0%)
    interchange_rate = random.uniform(0.015, 0.030)
    interchange_fee = round(transaction_amount * interchange_rate, 2)
    
    # Network fee ($0.10 - $0.25)
    network_fee = round(random.uniform(0.10, 0.25), 2)
    
    # Acquirer gets transaction amount minus interchange
    acquirer_settlement = round(transaction_amount - interchange_fee, 2)
    
    # Issuer gets transaction amount plus network fee
    issuer_settlement = round(transaction_amount + network_fee, 2)
    
    # Ensure issuer > acquirer (with buffer)
    if issuer_settlement <= acquirer_settlement:
        issuer_settlement = acquirer_settlement + random.uniform(0.50, 2.00)
    
    row.update({
        'interchange_fee': interchange_fee,
        'network_fee': network_fee,
        'acquirer_settlement_amount': acquirer_settlement,
        'issuer_settlement_amount': issuer_settlement
    })
    
    return row
```

### Example: Fraud Pattern Injection

```python
# assets/custom_rules/fraud_patterns.py

import random
from datetime import timedelta

def inject_velocity_fraud(transactions, fraud_rate=0.001):
    """
    Inject velocity fraud patterns (same card, multiple locations).
    
    Args:
        transactions: List of transaction dicts
        fraud_rate: Fraction of transactions to mark as fraudulent
    
    Returns:
        Updated transactions list
    """
    fraud_count = int(len(transactions) * fraud_rate)
    
    for _ in range(fraud_count):
        # Pick a random card
        base_tx = random.choice(transactions)
        card_id = base_tx['card_id']
        base_time = base_tx['transaction_time']
        
        # Create fraudulent transactions
        for i in range(3):  # 3 rapid transactions
            fraud_tx = base_tx.copy()
            fraud_tx['transaction_id'] = generate_uuid()
            fraud_tx['transaction_time'] = base_time + timedelta(minutes=i*10)
            fraud_tx['merchant_id'] = random.choice(distant_merchants)
            fraud_tx['fraud_flag'] = True
            transactions.append(fraud_tx)
    
    return transactions
```

## Using Constraints

### Command Line

```bash
python scripts/generate_data.py schema.json ./output \
    --constraints constraints.json
```

### In SKILL.md Workflow

```bash
# 1. Generate schema SQL
python scripts/create_postgres_schema.py schema.json

# 2. Generate data with constraints
python scripts/generate_data.py schema.json ./data \
    --constraints business_rules.json

# 3. Load data
python scripts/insert_data.py schema.json ./data \
    -d mydb -U myuser
```

## Validation and Debugging

### Validate Constraints Before Generation

```python
from generate_data import ConstraintEngine

engine = ConstraintEngine('constraints.json')
is_valid = engine.validate_constraints()

if not is_valid:
    print("Invalid constraints:", engine.get_errors())
```

### Enable Constraint Logging

```bash
python scripts/generate_data.py schema.json ./output \
    --constraints constraints.json \
    --log-constraints
```

This will log every constraint check to help debug issues.

## Best Practices

### Organization

- **Separate concerns**: Keep spatial, temporal, and relational constraints in separate sections
- **Document everything**: Use `description` fields liberally
- **Version constraints**: Include version info in constraint files

### Performance

- **Hard constraints are expensive**: Each hard constraint requires validation
- **Use probabilistic where possible**: Soft constraints are much faster
- **Batch validations**: Custom scripts should process in batches

### Testing

- **Start small**: Test constraints on 1,000 rows before generating millions
- **Validate incrementally**: Test each constraint type separately
- **Check edge cases**: Ensure constraints don't conflict

### Maintainability

- **Use constraint files**: Don't hardcode rules in scripts
- **Parameterize values**: Make rates/thresholds configurable
- **Document assumptions**: Explain why each constraint exists
