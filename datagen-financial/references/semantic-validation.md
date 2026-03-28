# Semantic Data Validation Guide

## Overview

This document describes the semantic validation rules and data generation constraints applied to ensure generated financial data makes sense for the banking domain.

## Customer Data Validation

### Customer Types

The system differentiates between two customer types:

1. **Retail Customers** (50% of total)
   - Individual consumers
   - Personal email addresses from public providers (gmail.com, yahoo.com, outlook.com, icloud.com, hotmail.com, aol.com)
   - Residential addresses
   - Lower credit limits ($500 - $50,000)

2. **Corporate/Business Customers** (50% of total)
   - Business entities and organizations
   - Corporate email domains from real companies (chase.com, microsoft.com, boeing.com, etc.)
   - Business addresses with suite/floor numbers
   - Higher credit limits ($10,000 - $500,000)

### Date of Birth Constraints

**Valid Age Range**: 18-85 years old from current date

**Rationale**:
- Banking regulations require customers to be at least 18 years old (legal age)
- Most active banking customers are under 85 years old
- Distribution is weighted towards economically active age groups

**Age Distribution**:
- 18-25 years: 15% (young adults, students, early career)
- 25-35 years: 25% (prime working age, growing families)
- 35-45 years: 25% (peak earning years, established careers)
- 45-55 years: 20% (mature professionals, peak wealth accumulation)
- 55-65 years: 10% (pre-retirement, high net worth)
- 65-85 years: 5% (retired, fixed income)

**Implementation**:
```python
# Date range: today minus 18 years to today minus 85 years
# Distribution weighted towards 25-55 age range
```

### Email Addresses

**Retail Customers**:
- Use public email providers
- Format: `{first_name}.{last_name}@{domain}`
- Domains: gmail.com, yahoo.com, outlook.com, icloud.com, hotmail.com, aol.com

**Corporate Customers**:
- Use real company domains from curated list
- Format: `{first_name}.{last_name}@{company_domain}`
- Domains: Real corporations (jpmchase.com, microsoft.com, apple.com, boeing.com, etc.)
- 75+ major US corporations across all sectors (Financial Services, Technology, Healthcare, Retail, Energy, etc.)

### Phone Numbers

**Format**: `{area_code}-{exchange}-{number}`

**Constraints**:
- Uses realistic US area codes (212, 415, 312, 713, etc.)
- Exchange codes: 200-999 (avoiding reserved ranges)
- Line numbers: 1000-9999

**Area Codes**: Includes major metropolitan areas:
- 212, 917: New York City
- 415, 510: San Francisco Bay Area
- 312, 773: Chicago
- 213, 310: Los Angeles
- 617: Boston
- 713: Houston
- And 25+ more realistic US area codes

### Address Generation

**Retail Customer Addresses**:
- **Line 1**: Residential street addresses
  - Format: `{number} {street_name} {street_type}`
  - Numbers: 1-9999
  - Street names: Main, Oak, Maple, Pine, Cedar, Elm, Park, Lake, Hill
  - Street types: St, Ave, Blvd, Dr, Ln, Ct, Way
  - Example: "4523 Oak Ave"

- **Line 2**: Optional apartment numbers (30% probability)
  - Format: `Apt {number}`
  - Numbers: 1-999
  - Example: "Apt 42"

**Corporate Customer Addresses**:
- **Line 1**: Business addresses
  - Format: `{number} {business_name} {location_type}`
  - Numbers: 1-999
  - Business names: Corporate, Business, Commerce, Executive, Professional, Enterprise, Industry, Tech, Innovation
  - Location types: Plaza, Center, Park, Way, Drive, Parkway, Boulevard
  - Example: "250 Corporate Plaza"

- **Line 2**: Optional suite/floor numbers (60% probability)
  - Format: `{type} {number}`
  - Types: Suite, Floor, Ste
  - Numbers: 100-2500
  - Example: "Suite 1800"

## Card Data Validation

### Credit Limits

**Retail Cards**:
- Range: $500 - $50,000
- Reflects typical consumer credit limits
- Distribution: uniform random within range

**Corporate Cards**:
- Range: $10,000 - $500,000
- Reflects business purchasing needs
- Distribution: uniform random within range

### Card Expiration Dates

**Valid Range**: 1-6 years from current year

**Rationale**:
- Cards are typically issued with 3-5 year expiration periods
- Allows for recently issued cards (1 year) and longer-term cards (6 years)
- Always future dates (current_year + 1 to current_year + 6)

**Implementation**:
```python
current_year = datetime.now().year
expiration_year = random.randint(current_year + 1, current_year + 6)
expiration_month = random.randint(1, 12)
```

### Card Numbers

**Format**: 16-digit number (4 groups of 4 digits)

**Constraints**:
- First 4 digits: 4000-5999 (Visa/Mastercard range)
- Remaining 12 digits: Random
- Note: Does not implement Luhn algorithm (synthetic data)

**Example**: "4523 8765 2341 7890"

### CVV Codes

**Format**: 3-digit number

**Range**: 000-999

## Transaction Data Validation

### Transaction Amounts

**General Transactions**:
- Range: $5.00 - $500.00
- Reflects typical consumer spending patterns
- Can be customized per merchant category

### Fees

**General Fees**:
- Range: $0.50 - $25.00
- Includes interchange fees, network fees, processing fees
- Realistic for typical credit card transactions

### Transaction Timing

**Business Hours Enforcement**:
- Most merchants: 6:00 AM - 11:00 PM
- Bars/Taverns: Later hours (5:00 PM - 2:00 AM)
- 24-hour locations: Gas stations, some grocery stores

**Peak Hours**:
- Restaurants: 12-1 PM (lunch), 6-8 PM (dinner)
- Gas Stations: 7-8 AM, 5-6 PM (commute times)
- Grocery Stores: 7-9 AM, 5-7 PM
- Retailers: 11 AM - 2 PM, 5-7 PM

## Geographic Data Validation

### Location Constraints

**Continental US Only**:
- Latitude: 24.5° N to 49.0° N
- Longitude: -125.0° W to -66.5° W
- Excludes Alaska, Hawaii, territories

### City Distribution

**Population-Weighted**:
- Major cities (NYC, LA, Chicago) receive more activity
- Mid-size cities receive proportional activity
- Small cities receive less activity

**Major Cities Included**:
- New York, NY
- Los Angeles, CA
- Chicago, IL
- Houston, TX
- Phoenix, AZ
- Philadelphia, PA
- San Antonio, TX
- San Diego, CA
- Dallas, TX
- San Jose, CA
- And 20+ more cities

### ZIP Codes

**State-Specific Prefixes**:
- NY: 100-105
- CA: 900-908
- TX: 750-759
- FL: 320-329
- IL: 600-609
- PA: 150-159
- OH: 430-439
- AZ: 850-857
- MA: 010-019
- WA: 980-986

**Format**: 5-digit codes with realistic state prefixes

## Temporal Constraints

### Data Generation Period

**Default Period**: Past 18 months from execution date

**Configurable**: Can be overridden in schema with custom date ranges

**Transaction Timestamps**:
- Distributed across the generation period
- Weighted towards peak hours per merchant type
- Respects merchant business hours
- Rate-limited to prevent unrealistic bursts

### Card Issue Dates

**Range**: Within data generation period

**Constraint**: Must be before any transactions on that card

### Account Creation Dates

**Range**: Within data generation period

**Constraint**: Must be before card issue dates for that customer

## Referential Integrity

### Foreign Key Constraints

**Strict Enforcement**:
- All foreign keys reference existing parent records
- Parent tables generated before child tables
- No orphaned records

**Examples**:
- Cards reference valid Cardholders
- Transactions reference valid Cards and Merchants
- Clearing records reference valid Authorization requests

### Transaction Flow Consistency

**Temporal Ordering**:
1. Authorization Request
2. Clearing Record (1-24 hours after auth)
3. Settlement Record (2-48 hours after clearing)
4. Reconciliation Record (12 hours - 3 days after settlement)

**Amount Consistency**:
- Settlement issuer amount > Settlement acquirer amount (issuer makes money)
- Fees are realistic percentages of transaction amounts
- All amounts round to 2 decimal places (USD)

## Data Quality Constraints

### Missing Data Patterns

**Nullable Fields**:
- Phone numbers: Can be missing
- Address line 2: Often missing (30-60% depending on customer type)
- Transaction codes: Missing 0.02% of the time (realistic data quality issue)

**Required Fields**:
- Email addresses: Always present
- Names: Always present
- Primary addresses: Always present
- Transaction amounts: Always present

### Name Uniqueness

**Enforcement**:
- Each person gets a unique first name + last name combination
- If collision occurs, adds middle initial
- Uses frequency-weighted name distributions from US Census data

**Realism**:
- Common names (John Smith) appear more frequently
- Rare names appear less frequently
- Proportional to actual US population demographics

## Validation Checklist

Before generating large datasets, validate:

1. **Customer Data**
   - [ ] Date of birth in range (18-85 years old)
   - [ ] Corporate customers have company email domains (no gmail/yahoo)
   - [ ] Retail customers have public email domains
   - [ ] Corporate customers have business addresses
   - [ ] Phone numbers use realistic area codes

2. **Card Data**
   - [ ] Credit limits appropriate for customer type
   - [ ] Expiration dates are in the future (1-6 years from now)
   - [ ] All cards reference valid cardholders

3. **Transaction Data**
   - [ ] Amounts are realistic for merchant category
   - [ ] Timestamps respect business hours
   - [ ] All transactions reference valid cards and merchants

4. **Geographic Data**
   - [ ] All locations within continental US
   - [ ] ZIP codes match states
   - [ ] Cities have realistic population weighting

5. **Temporal Data**
   - [ ] All dates within generation period
   - [ ] Transaction flow ordering is correct
   - [ ] Card issue dates before transaction dates

## Future Enhancements

Potential areas for additional semantic validation:

1. **Fraud Patterns**: Inject realistic fraud scenarios
2. **Seasonal Variations**: Adjust transaction patterns by season
3. **Economic Cycles**: Reflect economic conditions in spending patterns
4. **Customer Lifecycle**: Model customer behavior over time
5. **Geographic Correlation**: Ensure transactions occur near customer location
6. **Merchant Affinity**: Model customer preferences for certain merchants
7. **Transaction Sequences**: Realistic shopping patterns (gas station + convenience store)

## Summary

All generated data now includes:
- Proper customer type differentiation (retail vs corporate)
- Semantically correct email domains
- Age-appropriate date of birth values
- Realistic credit limits
- Future-dated card expirations
- Business vs residential addresses
- Realistic US phone numbers
- Population-weighted geographic distribution
- Temporally consistent transaction flows
- Domain-appropriate value ranges

This ensures the synthetic data is realistic, coherent, and suitable for testing banking systems, fraud detection models, and analytics pipelines.
