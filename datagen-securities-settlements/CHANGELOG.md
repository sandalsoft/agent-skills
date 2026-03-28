# Changelog

All notable changes to the Securities Settlements Data Generator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-15

### Added

#### Core Functionality
- **Securities Settlement Data Generator** with focus on settlement fails
- Support for multi-market settlements (US T+1, Japan T+2, Europe T+2)
- Comprehensive 8-table schema covering full settlement lifecycle
- Realistic fail generation with 15% default rate (configurable 5-40%)

#### Schema Tables
- `broker_dealers` - Market participants with DTC numbers and market coverage
- `investors` - Institutional and retail investors with custodian relationships
- `securities` - Equities with CUSIP/ISIN identifiers across markets
- `trades` - Trade executions with market-specific settlement cycles
- `settlement_instructions` - SSI, DVP/RVP/FOP instructions with affirmation
- `settlements` - Settlement attempts with status tracking
- `settlement_fails` - **Primary focus**: Detailed fail tracking with aging and resolution
- `fail_charges` - Penalty fees including daily charges, buy-ins, fines

#### Industry-Standard Features
- **CUSIP Generator**: Valid 9-character identifiers with proper check digits
- **ISIN Generator**: Valid 12-character identifiers using Luhn algorithm
- **Business Day Calculator**: Market-specific holiday calendars (US, JP, EU)
- **Settlement Cycle Logic**: Proper T+1 (US) and T+2 (JP/EU) calculations
- **DTC Participant Numbers**: 4-digit identifiers for US broker-dealers

#### Settlement Fail Features
- **5 Fail Categories**:
  - Insufficient securities (40%)
  - Cash shortfall (25%)
  - Operational issues (20%)
  - Custody problems (10%)
  - Other reasons (5%)
- **Fail Aging Buckets**:
  - Recent (0-3 days): 60% resolution rate
  - Aged (4-10 days): 30% resolution rate
  - Extended (11-20 days): 15% resolution rate
  - Chronic (21+ days): 5% resolution rate, buy-in triggered
- **Realistic Fail Reasons**: 25+ specific fail reasons across categories
- **Resolution Methods**: 8 different resolution approaches
- **Regulatory Threshold Tracking**: Flags fails exceeding $250M

#### Fail Charges
- **Daily Fail Fees**: 1-5 bps per day based on security type
- **Buy-In Costs**: Market price impact modeling (1-5%)
- **Administrative Fees**: $50-$2,000 per fail
- **Regulatory Fines**: $1,000-$10,000+ for threshold breaches
- **Interest Charges**: Based on overnight lending rates

#### Multi-Market Support
- **US Markets**:
  - Exchanges: NYSE, NASDAQ, NYSE American, BATS
  - Currency: USD
  - Identifiers: CUSIP (9-char) + ISIN
  - Settlement: DTC/NSCC, T+1 cycle
  - 60% of generated securities

- **Japan Markets**:
  - Exchanges: Tokyo Stock Exchange, Osaka Exchange
  - Currency: JPY
  - Identifiers: ISIN (JP prefix)
  - Settlement: JSCC, T+2 cycle
  - 20% of generated securities

- **Europe Markets**:
  - Exchanges: LSE, Euronext, Deutsche Börse, SIX Swiss
  - Currency: EUR, GBP, CHF (market-dependent)
  - Identifiers: ISIN (GB/FR/DE/CH prefix)
  - Settlement: Euroclear/Clearstream, T+2 cycle
  - 20% of generated securities

#### Investor Types
- **Institutional (15%)**:
  - Hedge funds, mutual funds, pension funds
  - Investment mandates and subtypes
  - Large trade sizes (10K-500K shares)
  - Lower commission rates (5-20 bps)

- **Retail (85%)**:
  - Individual investors
  - Small trade sizes (10-1K shares)
  - Higher commission rates (50-150 bps)

#### Broker-Dealer Types
- Buy-side brokers (30%)
- Sell-side brokers (35%)
- Market makers (20%)
- Prime brokers (15%)

#### Scripts
- `generate_securities_data.py` - Main data generator (1000+ lines)
  - Command-line interface with `--fail-rate` and `--seed` options
  - Progress tracking and statistics
  - Fail analysis breakdown by category and status
- `create_postgres_schema.py` - PostgreSQL DDL generator
- `insert_data.py` - CSV bulk loader with validation

#### Documentation
- **SKILL.md**: Claude Code skill configuration and usage guide
- **README.md**: Comprehensive overview with examples
- **CHANGELOG.md**: Version history (this file)
- **references/settlement-fail-patterns.md**: Industry patterns, fail categories, charges, regulatory frameworks
- **references/schema-format.md**: Schema JSON specification

#### Assets
- `securities_settlement_schema.json` - Complete schema with 8 tables
  - Row counts: 250 to 500,000 rows per table
  - Temporal constraints for settlement flows
  - Generation period: 2024-01-01 to 2024-12-31

#### Data Quality Features
- **Referential Integrity**: All foreign keys reference existing records
- **Temporal Consistency**: Trade date < Settlement date < Fail date < Resolution date
- **Business Day Logic**: No settlements on weekends or market holidays
- **Realistic Distributions**: Industry-accurate percentages throughout
- **Identifier Validation**: Valid CUSIP/ISIN check digits
- **Fail Rate Calibration**: Adjustable based on liquidity, broker efficiency, SSI status

#### Statistical Output
- Generation summary with row counts per table
- Fail analysis by category and status
- Aged fail counts (10+ days, 21+ days)
- Total fail value calculation
- Detailed progress indicators during generation

### Technical Details

#### Dependencies
- Python 3.7+
- psycopg2-binary (for PostgreSQL loading)
- Standard library: json, csv, random, uuid, datetime, argparse, pathlib

#### Performance
- Generates 500,000 trades in ~2-5 minutes (hardware-dependent)
- CSV output for fast PostgreSQL COPY bulk loading
- Efficient in-memory generation with lookup dictionaries

#### Data Volume (Default Schema)
- Total rows: ~1,740,250
- Total CSV size: ~500-800 MB (uncompressed)
- PostgreSQL database size: ~1-2 GB (with indices)

### Design Decisions

#### Settlement Fail Focus
- 15% default fail rate matches industry baseline (10-20% typical)
- Fail distribution weighted toward recent fails (realistic)
- Chronic fails trigger buy-in procedures (regulatory compliance)
- Multiple charges per fail based on aging (realistic cost accumulation)

#### Multi-Market Approach
- Mixed settlement cycles (T+1/T+2) reflect current global standards
- Market-specific holiday calendars for business day calculations
- Proper identifier standards (CUSIP for US, ISIN for all)

#### Data Realism
- Institutional investors have lower fail rates (better operations)
- Low liquidity securities have higher fail rates
- Unmatched settlement instructions increase fail probability
- Broker efficiency rating affects fail likelihood

### Known Limitations

1. **Simplified Holiday Calendars**: Uses subset of actual market holidays
   - Future versions may include complete holiday calendars

2. **Fixed Fail Categories**: 5 main categories
   - Real-world fails may have more nuanced classifications

3. **Single Currency Settlements**: No FX settlement fails
   - Focus is on equities, not multi-currency scenarios

4. **No Netting**: Each trade settles individually
   - Real-world CNS (Continuous Net Settlement) not modeled

5. **Static Security Prices**: Current price doesn't change over time
   - Trade prices vary around current price but security price is fixed

### Future Enhancements (Roadmap)

#### Potential Version 1.1 Features
- Continuous Net Settlement (CNS) modeling
- Corporate actions (dividends, splits affecting fails)
- Securities lending and borrowing
- Partial fill scenarios
- Multi-currency settlement fails

#### Potential Version 1.2 Features
- Intraday settlement cycles
- Real-time settlement status updates
- Failed trade allocations
- Settlement predictions (ML-ready data)

#### Potential Version 2.0 Features
- Fixed income securities (bonds)
- Options and derivatives settlement
- Cross-border complexity (withholding tax, dual listing)
- Settlement optimization algorithms

### Credits

**Created**: December 15, 2025

**Based On**: `datagen-financialv2` skill architecture
- Leveraged core generation patterns
- Adapted banking data generator approach
- Maintained schema format compatibility

**Industry Knowledge Sources**:
- SEC Regulation SHO (US close-out requirements)
- EU CSDR (Central Securities Depositories Regulation)
- DTCC settlement rules and procedures
- JSCC (Japan Securities Clearing Corporation) standards
- Euroclear/Clearstream settlement documentation

**Domain Expertise**:
- Equities settlement lifecycles
- Post-trade processing workflows
- Settlement fail management practices
- Regulatory compliance frameworks

---

## Version Numbering

- **Major version** (X.0.0): Incompatible schema changes, breaking API changes
- **Minor version** (1.X.0): New features, backward compatible
- **Patch version** (1.0.X): Bug fixes, documentation updates

## Unreleased

### Planned
- [ ] Support for PostgreSQL versions 12-17 compatibility testing
- [ ] Additional fail resolution scenarios
- [ ] CSV compression option for large datasets
- [ ] Performance benchmarks and optimization

### Under Consideration
- [ ] REST API for data generation
- [ ] Web UI for configuration
- [ ] Pre-built Docker container
- [ ] Cloud deployment templates (AWS, GCP, Azure)

---

**Note**: This is the initial release. Please report any issues or suggestions for improvement.
