# Realistic Data Patterns

This document describes how the data generator maintains realism across multiple dimensions.

## Name Generation

### Distribution-Based Sampling

Names are sampled from frequency-weighted distributions based on US Census data:

- **Common names appear more frequently**: "Michael Johnson" is statistically more likely than "Xenophon Beaumont"
- **Uniqueness is enforced**: Each person entity gets a unique name combination
- **Fallback mechanism**: If all combinations are exhausted, middle initials are added

### Gender Distribution

- Male names: ~49% of population
- Female names: ~51% of population

## Spatial Realism

### Location Constraints

All locations are constrained to **continental United States** only:
- Latitude: 24.4° N to 49.4° N
- Longitude: 125° W to 66.9° W

### Population-Weighted Distribution

Merchant and cardholder locations are distributed based on actual population density:

- Major metropolitan areas (NYC, LA, Chicago) get proportionally more activity
- Rural areas get proportionally less activity
- Distribution matches real-world population weights

### Geographic Coherence

- ZIP codes match their state
- City/state combinations are realistic
- Lat/long coordinates align with city centers (±0.5° variation)

## Temporal Realism

### Transaction Timing

Transactions respect merchant-specific business hours and peak patterns:

#### By Merchant Category

**Gas Stations (MCC 5541)**
- Peak hours: 7-8 AM, 5-6 PM (commute times)
- Transactions per day: 30-600
- Average processing time: 2-3 minutes per transaction

**Restaurants (MCC 5812)**
- Peak hours: 12-1 PM (lunch), 6-8 PM (dinner)
- Transactions per day: 20-350
- Higher variance in transaction amounts during dinner

**Grocery Stores (MCC 5411)**
- Peak hours: 7-9 AM, 5-7 PM
- Transactions per day: 15-800 (varies by store size)
- Consistent throughout the week with weekend spikes

**Bars (MCC 5813)**
- Peak hours: 5-11 PM
- Transactions per day: 15-200
- Near-zero activity before 5 PM

### Transaction Flow Timing

Financial transaction processing follows realistic timelines:

**Authorization → Clearing**
- Typical: 1-24 hours
- Most transactions clear within 4-6 hours
- Some (international, high-value) take up to 24 hours

**Clearing → Settlement**
- Typical: 2-48 hours
- Batch processing occurs 1-2 times per day
- Weekend transactions may take longer

**Settlement → Reconciliation**
- Typical: 12 hours to 3 days
- Daily batch reconciliation
- Month-end reconciliation may take longer

### Rate Limiting

The generator enforces realistic transaction rate limits per merchant:

- **Fast food**: Up to 50 transactions/hour
- **Gas stations**: Up to 25 transactions/hour  
- **Sit-down restaurants**: Up to 15 transactions/hour
- **Retail stores**: Varies by size, typically 10-40/hour

## Financial Realism

### Transaction Amounts

Transaction amounts follow merchant-specific distributions:

**Amount Generation**
- Mean transaction amount varies by MCC
- Standard deviation creates realistic variance
- No artificial rounding (real amounts like $67.43, not just $67.00)

**Example Distributions**

| Merchant Type | Avg | Std Dev | Typical Range |
|--------------|-----|---------|---------------|
| Fast Food | $12.30 | $8.75 | $5-35 |
| Gas Station | $45.00 | $22.10 | $15-95 |
| Electronics | $245.60 | $312.40 | $20-1200 |
| Hotel | $189.40 | $145.30 | $75-600 |

### Fee Structures

Fees follow realistic credit card processing economics:

**Interchange Fees**
- Typically 1.5%-3.0% of transaction amount
- Higher for credit cards vs. debit cards
- Premium cards (rewards cards) have higher interchange

**Network Fees**
- Fixed per-transaction fee: $0.10-$0.25
- Varies by network (Visa, Mastercard, Amex, Discover)

**Settlement Amounts**
- Issuer settlement > Acquirer settlement (by interchange + network fee)
- This inequality is **always enforced** as a hard constraint

## Card Network Distribution

Card distribution matches real-world market share:

- Visa: ~50%
- Mastercard: ~30%
- Amex: ~12%
- Discover: ~8%

## Data Quality Patterns

### Missing Data

Certain fields may be intentionally missing to reflect real-world data quality:

**Default Missing Rates** (unless overridden by constraints):
- Transaction codes: 0.02% missing
- Secondary address lines: 30% NULL (realistically not everyone has apt numbers)
- Decline reasons: Only present when auth_response = 'declined'
- Phone numbers: 5% missing

### Authorization Outcomes

**Approval Rates** (typical):
- Overall: 85-90% approved
- First-time cards: 75-80% approved (more scrutiny)
- High-value transactions: 70-75% approved (more fraud checks)

**Decline Reasons**:
- Insufficient funds: 40%
- Suspected fraud: 30%
- Expired card: 15%
- Incorrect CVV/PIN: 10%
- Other: 5%

## Cardholder Behavior Patterns

### Card Usage

**Frequency Distribution**:
- Heavy users (>20 tx/month): 10% of cardholders, 40% of transactions
- Regular users (5-20 tx/month): 40% of cardholders, 45% of transactions  
- Light users (<5 tx/month): 50% of cardholders, 15% of transactions

### Credit Limits

Credit limits follow log-normal distribution:
- Median: $8,000
- Mean: $12,500
- Range: $500 - $50,000
- Correlated with cardholder credit history (implicitly modeled)

## Maintaining Coherence

### Entity Consistency

**Across Tables**:
- A `transaction_id` represents the SAME transaction across all tables
- Authorization, clearing, settlement, and reconciliation records share the same `transaction_id`
- Timestamps progress forward across the lifecycle (auth_time < clearing_time < settlement_time)

**Within Tables**:
- Cardholder addresses are consistent (same person = same address)
- Merchant locations are consistent (same merchant_id = same physical location)
- Card attributes are immutable (card_number doesn't change)

### Referential Integrity

All foreign keys are guaranteed to reference existing records:

- Every `card_id` in transactions exists in the `cards` table
- Every `merchant_id` in transactions exists in the `merchants` table  
- Every `cardholder_id` in cards exists in the `cardholders` table

The generator creates parent entities first, then child entities that reference them.

## Fraud Pattern Generation

While not the default, the system can generate fraud patterns when configured:

**Velocity Fraud**:
- Same card used at multiple distant locations within short timeframe
- Configured via constraints: `allow_geographic_fraud: true`

**Synthetic Identity Fraud**:
- Fabricated identities with unusual attribute combinations
- Requires special constraint configuration

**Testing Fraud Detection**:
- Mark certain transactions as "known fraud" for ML training
- Add metadata flag without disrupting referential integrity
