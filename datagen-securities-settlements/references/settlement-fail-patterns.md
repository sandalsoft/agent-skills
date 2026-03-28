# Settlement Fail Patterns and Industry Standards

## Overview

This document describes the realistic settlement fail patterns, industry standards, and domain knowledge embedded in the securities settlement data generator.

## Settlement Cycles by Market

### United States (T+1)

**Effective Date**: May 28, 2024

- **Settlement Cycle**: Trade Date + 1 business day
- **Securities**: Equities, ETFs, corporate bonds
- **Identifier**: CUSIP (9 characters)
- **Clearinghouse**: DTCC (DTC/NSCC)
- **Currency**: USD
- **Exchanges**: NYSE, NASDAQ, NYSE American, BATS

**Example**:
- Trade Date: Monday
- Settlement Date: Tuesday (next business day)

### Japan (T+2)

- **Settlement Cycle**: Trade Date + 2 business days
- **Securities**: Japanese equities
- **Identifier**: ISIN with JP prefix (12 characters)
- **Clearinghouse**: Japan Securities Clearing Corporation (JSCC)
- **Currency**: JPY
- **Exchanges**: Tokyo Stock Exchange (TSE), Osaka Exchange

**Example**:
- Trade Date: Monday
- Settlement Date: Wednesday (two business days later)

### Europe (T+2)

- **Settlement Cycle**: Trade Date + 2 business days
- **Securities**: European equities
- **Identifier**: ISIN with country prefix (GB, FR, DE, etc.)
- **Clearinghouse**: Euroclear, Clearstream
- **Currency**: EUR, GBP, CHF (market-dependent)
- **Exchanges**: LSE, Euronext, Deutsche Börse, SIX Swiss Exchange

**Example**:
- Trade Date: Monday
- Settlement Date: Wednesday (two business days later)

## Settlement Fail Categories

### 1. Insufficient Securities (40% of fails)

**Description**: Seller cannot deliver securities on settlement date

**Specific Reasons**:
- Seller does not have securities in custody account
- Securities are pledged or encumbered (e.g., used as collateral)
- Corporate action pending on securities (dividend, split, merger)
- Securities in transfer between custodian accounts
- Account restrictions preventing delivery (regulatory hold, legal freeze)

**Typical Resolution**:
- Seller locates and delivers securities (60% within 3 days)
- Borrow securities from securities lending desk
- Buy-in procedure after regulatory threshold (T+21 in US)

**Example Scenario**:
A sell-side trader executes a sale of 50,000 shares but the institutional client doesn't have the shares in their custody account. The shares are held in a different sub-account that requires manual transfer approval.

### 2. Cash Shortfall (25% of fails)

**Description**: Buyer cannot pay for securities on settlement date

**Specific Reasons**:
- Buyer has insufficient funds in settlement account
- Credit limit exceeded
- Payment system unavailable (technical issue, holiday mismatch)
- Bank account frozen or restricted
- Currency conversion failed (for cross-border trades)

**Typical Resolution**:
- Buyer funds settlement account (50% within 1-2 days)
- Credit line extension approved
- Alternative payment method arranged

**Example Scenario**:
A hedge fund buys $25M of stock but their settlement account only has $20M. They need to transfer additional funds from their prime broker, which takes 1-2 days.

### 3. Operational Issues (20% of fails)

**Description**: Process or system failures preventing settlement

**Specific Reasons**:
- System outage during settlement window
- Incorrect settlement instructions (wrong account number, custodian)
- Missing or invalid SSI (Standing Settlement Instructions) data
- Manual intervention required but not completed
- Matching failed between buyer and seller instructions
- Settlement cut-off time missed

**Typical Resolution**:
- Correct instructions and resubmit (70% resolved next day)
- Manual processing by operations team
- System restoration

**Example Scenario**:
Buyer's custodian bank SSI was recently changed but the update wasn't communicated to the selling broker. Instructions don't match and settlement fails.

### 4. Custody Issues (10% of fails)

**Description**: Problems with custodian banks or account structure

**Specific Reasons**:
- Securities in wrong custodian account or sub-account
- Custody transfer pending between custodians
- Account closure in progress
- Beneficiary account invalid or closed
- Custodian system issue (rare but happens)

**Typical Resolution**:
- Transfer securities to correct account (2-5 days)
- Update account information
- Open new account if needed

**Example Scenario**:
Client has transferred their account from Custodian A to Custodian B, but some securities are still in transit. Settlement fails until transfer completes.

### 5. Other (5% of fails)

**Description**: Uncommon or unique circumstances

**Specific Reasons**:
- Regulatory hold on securities (SEC investigation, insider trading restriction)
- Legal dispute pending (class action, litigation)
- Force majeure event (natural disaster, war, pandemic market closure)
- Counterparty dispute (price dispute, trade cancellation request)
- Market suspension or circuit breaker

**Typical Resolution**:
- Varies widely depending on circumstance
- May require legal or regulatory resolution
- Can take weeks or months

## Fail Aging and Resolution Rates

### Recent Fails (0-3 days)

**Characteristics**:
- Most common fail bucket
- Often simple issues (cash, instructions)
- High resolution rate

**Resolution Rate**: 60% resolve within this period

**Example**: Same-day fails often resolve T+1 when buyer funds account or seller locates securities

### Aged Fails (4-10 days)

**Characteristics**:
- More complex issues
- Requires intervention
- Operations teams engaged

**Resolution Rate**: 30% resolve in this period (cumulative 90% by day 10)

**Example**: Custody transfers, account corrections, securities lending arrangements

### Extended Fails (11-20 days)

**Characteristics**:
- Problematic fails
- Management escalation
- Buy-in warnings issued

**Resolution Rate**: 15% resolve in this period

**Example**: Complex custody issues, regulatory holds pending clearance

### Chronic Fails (21+ days)

**Characteristics**:
- Regulatory threshold breach
- Mandatory buy-in procedures
- Significant scrutiny

**Resolution Rate**: 5% resolve in this period, 95% require forced close-out

**Regulatory Actions**:
- US: Reg SHO close-out requirement
- EU: CSDR mandatory buy-in regime
- Penalties and fines assessed

## Fail Charges and Penalties

### Daily Fail Fees

**Calculation**: Fail value × basis points per day

**Typical Rates**:
- Investment grade securities: 1-2 bps/day
- High yield securities: 3-5 bps/day
- Hard-to-borrow securities: 5-10 bps/day

**Example**:
- Fail value: $10,000,000
- Daily rate: 3 bps (0.0003)
- Daily fail fee: $3,000

**Charged to**: Failing party (buyer if cash fail, seller if securities fail)

### Buy-In Costs

**Trigger**: Chronic fails (typically after 21 days in US)

**Calculation**: Price difference between original trade and buy-in trade

**Typical Impact**: 1-5% adverse price movement (higher for illiquid securities)

**Example**:
- Original trade: 100,000 shares @ $50.00 = $5,000,000
- Buy-in executed: 100,000 shares @ $52.00 = $5,200,000
- Buy-in cost: $200,000 (4% impact)

**Charged to**: Failing seller

### Administrative Fees

**Purpose**: Cover operational costs of fail management

**Typical Amounts**:
- Routine fails: $50-$100 per fail
- Aged fails: $200-$500 per fail
- Complex fails: $500-$2,000 per fail

**Charged to**: Failing party

### Regulatory Fines

**US (SEC Regulation SHO)**:
- Threshold: $250 million fail for any single security
- Fine: Variable, can be $10,000-$100,000+ depending on circumstances

**EU (CSDR)**:
- Graduated penalties starting at 1 EUR per day
- Escalating based on fail duration and value
- Can reach thousands of euros per day for large chronic fails

**Japan (JSCC)**:
- Fail penalties calculated per transaction
- Escalating with duration

### Interest Charges

**Calculation**: Cost of funding the failed position

**Rate**: Typically based on:
- Overnight lending rate (e.g., SOFR + spread)
- 2-10 bps depending on creditworthiness

**Example**:
- Fail value: $10,000,000
- Interest rate: 5 bps (0.0005)
- Daily interest: $5,000

## Failing Party Determination

### Securities Fails

**Failing Party**: Seller

**Reasons**:
- Seller doesn't have securities to deliver
- Seller's operational issue
- Seller's custodian issue

**Responsibility**: Seller charged with fail fees and buy-in costs

### Cash Fails

**Failing Party**: Buyer

**Reasons**:
- Buyer doesn't have cash to pay
- Buyer's bank/credit issue
- Buyer's operational issue

**Responsibility**: Buyer charged with fail fees and interest

### Intermediary Fails

**Failing Party**: Broker, custodian, or clearinghouse

**Reasons**:
- System failures
- Operational errors
- Matching failures

**Responsibility**: Intermediary charged and typically indemnifies client

## Industry Identifiers

### CUSIP (Committee on Uniform Securities Identification Procedures)

**Format**: 9 characters
- Characters 1-6: Issuer identifier
- Characters 7-8: Issue identifier
- Character 9: Check digit (Luhn algorithm variant)

**Example**: 037833100 (Apple Inc.)

**Scope**: US and Canadian securities

**Check Digit Calculation**:
1. Convert letters to numbers (A=10, B=11, ..., Z=35)
2. Double every other digit starting from position 2
3. Sum all digits
4. Check digit = (10 - (sum mod 10)) mod 10

### ISIN (International Securities Identification Number)

**Format**: 12 characters
- Characters 1-2: Country code (ISO 3166-1 alpha-2)
- Characters 3-11: National securities identifier
- Character 12: Check digit (Luhn algorithm)

**Examples**:
- US0378331005 (Apple Inc. - derived from CUSIP)
- JP3633400001 (Toyota Motor Corp)
- GB0005405286 (HSBC Holdings)

**Scope**: Global standard for securities identification

**Check Digit Calculation** (Luhn algorithm):
1. Convert letters to numbers (A=10, B=11, ..., Z=35)
2. Double every other digit from the right
3. If doubled value > 9, sum the digits (18 → 1+8 = 9)
4. Sum all values
5. Check digit = (10 - (sum mod 10)) mod 10

### DTC Participant Numbers

**Format**: 4 digits

**Example**: 0901 (Goldman Sachs)

**Purpose**: Identifies participants in the Depository Trust Company system

**Scope**: US broker-dealers and custodians settling through DTC

## Settlement Methods

### DVP (Delivery vs Payment)

**Description**: Securities delivered only when payment is received simultaneously

**Use Case**: Standard for most securities trades

**Process**:
1. Seller delivers securities to central depository
2. Buyer's cash transferred simultaneously
3. Securities and cash exchange atomically

**Risk Mitigation**: Eliminates principal risk

### RVP (Receive vs Payment)

**Description**: Payment made only when securities are received simultaneously

**Use Case**: Buyer's perspective of DVP

**Same Process**: DVP and RVP are two sides of the same settlement

### FOP (Free of Payment)

**Description**: Securities transferred without payment

**Use Case**:
- Internal account transfers
- Corporate actions (stock splits, dividends)
- Collateral movements
- Gift transfers

**Risk**: Higher risk as payment is separate or non-existent

## Realistic Fail Rates

### Industry Benchmarks

**Overall Market**:
- Normal conditions: 10-15% of trades fail at least once
- Stressed conditions: 20-30% fail rate
- Crisis conditions: 40%+ fail rate

**By Security Type**:
- Large cap equities (high liquidity): 5-10% fail rate
- Small cap equities (low liquidity): 15-25% fail rate
- Corporate bonds: 20-30% fail rate
- Hard-to-borrow securities: 30-50% fail rate

**By Participant Type**:
- Prime brokers (efficient operations): 8-12% fail rate
- Smaller broker-dealers: 15-25% fail rate
- Retail brokers: 10-15% fail rate

### Generator Default

**Target Fail Rate**: 15% (realistic industry baseline)

**Adjustable**: Can be configured from 5% (optimistic) to 40% (crisis)

## Settlement Infrastructure

### United States

**Central Depository**: Depository Trust Company (DTC)
**Clearinghouse**: National Securities Clearing Corporation (NSCC)
**Settlement System**: Continuous Net Settlement (CNS)

**Process**:
1. Trade executed on exchange
2. Trade reported to NSCC
3. NSCC novates (becomes counterparty to both sides)
4. Net settlement obligations calculated
5. DTC settles against netted positions
6. DVP settlement via Fed wire

### Japan

**Central Depository**: Japan Securities Depository Center (JASDEC)
**Clearinghouse**: Japan Securities Clearing Corporation (JSCC)

**Process**:
1. Trade executed on TSE
2. Trade reported to JSCC
3. JSCC clears and settles
4. DVP settlement through Bank of Japan

### Europe

**Central Depositories**:
- Euroclear (Belgium, France, Netherlands, UK)
- Clearstream (Germany, Luxembourg)
- National CSDs (country-specific)

**Settlement Platform**: TARGET2-Securities (T2S)

**Process**:
1. Trade executed on exchange
2. Trade reported to CCP (if cleared) or bilateral
3. Settlement instructions sent to CSD
4. DVP settlement via T2S platform

## Corporate Actions Impact

### Dividends

**Impact on Settlement**:
- Trades executed before ex-dividend date settle "cum-dividend"
- Trades executed on/after ex-dividend date settle "ex-dividend"
- Fails spanning ex-dividend date create dividend claims

**Resolution**: Failing party compensates for missed dividend

### Stock Splits

**Impact on Settlement**:
- Settlement quantity adjusted for split ratio
- Pending fails recalculated
- System updates required

**Example**: 2-for-1 split changes 1,000 share fail to 2,000 share fail

### Mergers/Acquisitions

**Impact on Settlement**:
- Target company securities may become ineligible
- Conversion to acquirer securities
- Settlement complications during transition period

**Resolution**: Often requires manual intervention and trade amendments

## Best Practices

### Fail Prevention

1. **Affirm early**: Institutional clients should affirm trades within 24 hours
2. **Verify SSI**: Ensure standing settlement instructions are current
3. **Pre-settlement matching**: Match instructions 1-2 days before settlement
4. **Securities availability**: Confirm holdings before executing sell trades
5. **Cash availability**: Ensure funding in place before trade execution

### Fail Management

1. **Monitor aging**: Track fails daily and escalate aged fails
2. **Communicate**: Notify counterparties immediately when fail occurs
3. **Document**: Maintain clear records of fail reasons and resolution efforts
4. **Escalate**: Involve management for extended fails (10+ days)
5. **Buy-in procedures**: Initiate buy-ins before regulatory deadlines

### Regulatory Compliance

1. **Threshold lists**: Monitor securities on threshold lists
2. **Close-out requirements**: Comply with Reg SHO, CSDR requirements
3. **Reporting**: Accurate and timely fail reporting to regulators
4. **Locate requirements**: For short sales, ensure borrow/locate in place
5. **Penalties**: Track and pay fail charges promptly

## Data Quality Checks

When using generated settlement data, validate:

1. **Settlement dates**: Correct T+1 (US) or T+2 (JP/EU) calculation
2. **Business days**: No settlement on weekends or market holidays
3. **Identifiers**: Valid CUSIP/ISIN check digits
4. **Fail rates**: Within reasonable range (5-40%)
5. **Temporal consistency**: Trade date < Settlement date < Fail date
6. **Referential integrity**: All FKs resolve correctly
7. **Fail aging**: Resolution rates align with aging buckets
8. **Charge calculations**: Penalty amounts are realistic

## Additional Resources

### Regulatory References

- **SEC Regulation SHO**: Close-out requirements for equity fails
- **EU CSDR**: Central Securities Depositories Regulation
- **DTCC Rules**: DTC and NSCC participant rules

### Industry Standards

- **ISO 15022**: Securities message standards
- **ISO 20022**: Financial messaging standard (newer)
- **SWIFT**: Cross-border settlement messaging

### Market Infrastructure

- **DTCC**: www.dtcc.com (US settlement infrastructure)
- **Euroclear**: www.euroclear.com (European settlement)
- **JSCC**: www.jpx.co.jp/jscc/en/ (Japan clearing)
