#!/usr/bin/env python3
"""
Securities Settlement Data Generator

Generates realistic synthetic data for securities settlements with focus on
settlement fails across multiple markets (US T+1, Japan T+2, Europe T+2).
"""

import json
import csv
import random
import uuid
import argparse
import sys
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict


class CUSIPGenerator:
    """Generates valid CUSIP identifiers with proper check digits."""

    @staticmethod
    def generate_cusip() -> str:
        """Generate a 9-character CUSIP with valid check digit."""
        # Generate 8 random alphanumeric characters (issuer=6, issue=2)
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        base = ''.join(random.choice(chars) for _ in range(8))

        # Calculate check digit using Luhn algorithm variant
        check_digit = CUSIPGenerator._calculate_check_digit(base)
        return base + str(check_digit)

    @staticmethod
    def _calculate_check_digit(cusip_base: str) -> int:
        """Calculate CUSIP check digit."""
        char_values = {}
        for i, char in enumerate('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            char_values[char] = i

        total = 0
        for i, char in enumerate(cusip_base):
            value = char_values[char]
            if i % 2 == 1:  # Odd positions (0-indexed)
                value *= 2
            total += value // 10 + value % 10

        return (10 - (total % 10)) % 10


class ISINGenerator:
    """Generates valid ISIN identifiers with proper check digits."""

    @staticmethod
    def generate_isin(country_code: str, cusip: Optional[str] = None) -> str:
        """Generate a 12-character ISIN with valid check digit."""
        if country_code == 'US' and cusip:
            # US ISINs are derived from CUSIP: US + 9-digit CUSIP + check digit
            base = country_code + cusip
        else:
            # Generate random 9-character national security identifier
            chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            national_id = ''.join(random.choice(chars) for _ in range(9))
            base = country_code + national_id

        check_digit = ISINGenerator._calculate_check_digit(base)
        return base + str(check_digit)

    @staticmethod
    def _calculate_check_digit(isin_base: str) -> int:
        """Calculate ISIN check digit using Luhn algorithm."""
        # Convert letters to numbers (A=10, B=11, ..., Z=35)
        digits = ''
        for char in isin_base:
            if char.isalpha():
                digits += str(ord(char) - ord('A') + 10)
            else:
                digits += char

        # Luhn algorithm
        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 0:  # Every other digit from right
                n *= 2
                if n > 9:
                    n -= 9
            total += n

        return (10 - (total % 10)) % 10


class BusinessDayCalculator:
    """Calculate business days for different markets."""

    # Simplified holiday lists (in practice, would use comprehensive calendars)
    US_HOLIDAYS_2024 = [
        date(2024, 1, 1), date(2024, 1, 15), date(2024, 2, 19),
        date(2024, 5, 27), date(2024, 6, 19), date(2024, 7, 4),
        date(2024, 9, 2), date(2024, 11, 28), date(2024, 12, 25)
    ]

    JP_HOLIDAYS_2024 = [
        date(2024, 1, 1), date(2024, 1, 8), date(2024, 2, 11),
        date(2024, 2, 23), date(2024, 3, 20), date(2024, 4, 29),
        date(2024, 5, 3), date(2024, 5, 4), date(2024, 5, 5),
        date(2024, 7, 15), date(2024, 8, 11), date(2024, 9, 16),
        date(2024, 9, 23), date(2024, 10, 14), date(2024, 11, 3),
        date(2024, 11, 23), date(2024, 12, 31)
    ]

    EU_HOLIDAYS_2024 = [
        date(2024, 1, 1), date(2024, 3, 29), date(2024, 4, 1),
        date(2024, 5, 1), date(2024, 12, 25), date(2024, 12, 26)
    ]

    @staticmethod
    def add_business_days(start_date: date, days: int, market: str) -> date:
        """Add business days to a date considering market holidays."""
        holidays = {
            'US': BusinessDayCalculator.US_HOLIDAYS_2024,
            'JP': BusinessDayCalculator.JP_HOLIDAYS_2024,
            'EU': BusinessDayCalculator.EU_HOLIDAYS_2024
        }.get(market, [])

        current = start_date
        while days > 0:
            current += timedelta(days=1)
            # Skip weekends and holidays
            if current.weekday() < 5 and current not in holidays:
                days -= 1

        return current

    @staticmethod
    def is_business_day(check_date: date, market: str) -> bool:
        """Check if date is a business day."""
        holidays = {
            'US': BusinessDayCalculator.US_HOLIDAYS_2024,
            'JP': BusinessDayCalculator.JP_HOLIDAYS_2024,
            'EU': BusinessDayCalculator.EU_HOLIDAYS_2024
        }.get(market, [])

        return check_date.weekday() < 5 and check_date not in holidays

    @staticmethod
    def business_days_between(start_date: date, end_date: date, market: str) -> int:
        """Calculate number of business days between two dates."""
        if start_date > end_date:
            return 0

        count = 0
        current = start_date
        while current <= end_date:
            if BusinessDayCalculator.is_business_day(current, market):
                count += 1
            current += timedelta(days=1)

        return count


class SecuritiesDataGenerator:
    """Main data generator for securities settlements."""

    def __init__(self, schema_path: str, output_dir: str, fail_rate: float = 0.15):
        self.schema_path = Path(schema_path)
        self.output_dir = Path(output_dir)
        self.fail_rate = fail_rate

        # Load schema
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)

        # Parse generation period
        period = self.schema.get('data_generation_period', {})
        self.start_date = datetime.strptime(period.get('start_date', '2024-01-01'), '%Y-%m-%d').date()
        self.end_date = datetime.strptime(period.get('end_date', '2024-12-31'), '%Y-%m-%d').date()

        # Storage for generated data
        self.broker_dealers = []
        self.investors = []
        self.securities = []
        self.trades = []
        self.settlement_instructions = []
        self.settlements = []
        self.settlement_fails = []
        self.fail_charges = []

        # Lookups for referential integrity
        self.broker_dealer_lookup = {}
        self.investor_lookup = {}
        self.security_lookup = {}

        # Market data
        self.markets = ['US', 'JP', 'EU']
        self.market_weights = {'US': 0.60, 'JP': 0.20, 'EU': 0.20}

        # Reference data
        self._load_reference_data()

    def _load_reference_data(self):
        """Load reference data for generation."""
        # Broker dealer names
        self.broker_names_us = [
            "Goldman Sachs", "Morgan Stanley", "JP Morgan Securities", "Bank of America Merrill Lynch",
            "Citi Global Markets", "Wells Fargo Securities", "UBS Securities", "Barclays Capital",
            "Credit Suisse Securities", "Deutsche Bank Securities", "Jefferies", "Raymond James",
            "Piper Sandler", "William Blair", "Stifel Nicolaus"
        ]

        self.broker_names_jp = [
            "Nomura Securities", "Daiwa Securities", "SMBC Nikko Securities", "Mizuho Securities",
            "SBI Securities", "Rakuten Securities", "Matsui Securities"
        ]

        self.broker_names_eu = [
            "Barclays Europe", "Deutsche Bank AG", "BNP Paribas", "Société Générale",
            "Credit Suisse Europe", "UBS Europe", "HSBC Bank", "ING Bank"
        ]

        # Institutional investor names
        self.institutional_names = [
            "Vanguard Asset Management", "BlackRock Fund Advisors", "State Street Global",
            "Fidelity Management", "T. Rowe Price", "Wellington Management",
            "Capital Group", "Dimensional Fund Advisors", "Northern Trust",
            "Invesco", "Franklin Templeton", "Alliance Bernstein",
            "Prudential Financial", "TIAA-CREF", "Principal Financial"
        ]

        # Custodian banks
        self.custodians_us = [
            "BNY Mellon", "State Street Bank", "JP Morgan Chase Bank",
            "Citi Global Custody", "Northern Trust"
        ]

        self.custodians_intl = [
            "Euroclear Bank", "Clearstream Banking", "SIX SIS",
            "Sumitomo Mitsui Trust Bank", "Mizuho Trust & Banking"
        ]

        # Company names by sector
        self.companies = {
            'Technology': ['GlobalTech Corp', 'DataSystems Inc', 'CloudWare Ltd', 'SoftLogic Group',
                          'NetServices Inc', 'CyberSolutions AG', 'TechInnovate KK'],
            'Financials': ['National Bank Corp', 'Global Finance Group', 'Trust Holdings Inc',
                          'Capital Markets Ltd', 'Investment Services AG', 'Financial Corp KK'],
            'Healthcare': ['MediCare Inc', 'BioPharma Group', 'Health Systems Ltd',
                          'Medical Devices Corp', 'Pharmaceutical AG', 'HealthTech KK'],
            'Consumer': ['Retail Group Inc', 'Consumer Goods Corp', 'Shopping Network Ltd',
                        'Home Products AG', 'Consumer Services KK'],
            'Industrials': ['Manufacturing Corp', 'Industrial Group Inc', 'Engineering Ltd',
                           'Construction AG', 'Heavy Industries KK'],
            'Energy': ['Energy Corp', 'Oil & Gas Inc', 'Power Generation Ltd', 'Energy AG', 'Utilities KK'],
            'Materials': ['Materials Corp', 'Chemical Group Inc', 'Mining Ltd', 'Resources AG'],
            'Utilities': ['Utility Services Inc', 'Power Corp', 'Water & Gas Ltd'],
            'Telecommunications': ['Telecom Group Inc', 'Communications Corp', 'Network Services Ltd']
        }

        # Exchanges
        self.exchanges = {
            'US': ['NYSE', 'NASDAQ', 'NYSE American', 'BATS'],
            'JP': ['Tokyo Stock Exchange', 'Osaka Exchange'],
            'EU': ['London Stock Exchange', 'Euronext Paris', 'Deutsche Börse', 'SIX Swiss Exchange']
        }

        # Fail reasons by category
        self.fail_reasons = {
            'insufficient_securities': [
                'Seller does not have securities in custody',
                'Securities pledged or encumbered',
                'Corporate action pending on securities',
                'Securities in transfer between accounts',
                'Account restrictions preventing delivery'
            ],
            'cash_shortfall': [
                'Buyer insufficient funds in settlement account',
                'Credit limit exceeded',
                'Payment system unavailable',
                'Bank account frozen or restricted',
                'Currency conversion failed'
            ],
            'operational': [
                'System outage during settlement window',
                'Incorrect settlement instructions',
                'Missing or invalid SSI data',
                'Manual intervention required',
                'Matching failed between counterparties',
                'Cut-off time missed'
            ],
            'custody': [
                'Securities in wrong custodian account',
                'Custody transfer pending',
                'Account closure in progress',
                'Beneficiary account invalid',
                'Custodian system issue'
            ],
            'other': [
                'Regulatory hold on securities',
                'Legal dispute pending',
                'Force majeure event',
                'Counterparty dispute',
                'Market suspension'
            ]
        }

        # Resolution methods
        self.resolution_methods = [
            'Securities delivered by seller',
            'Cash settled by buyer',
            'Buy-in executed in market',
            'Manual intervention and correction',
            'Instruction corrected and resubmitted',
            'Custody transfer completed',
            'Trade cancelled by mutual agreement',
            'Forced close-out by clearinghouse'
        ]

    def generate_all_data(self):
        """Generate all tables in correct dependency order."""
        print("🔧 Starting securities settlement data generation...")
        print(f"📅 Period: {self.start_date} to {self.end_date}")
        print(f"⚠️  Target fail rate: {self.fail_rate * 100:.1f}%\n")

        # Generate in dependency order
        self._generate_broker_dealers()
        self._generate_investors()
        self._generate_securities()
        self._generate_trades()
        self._generate_settlement_instructions()
        self._generate_settlements()
        self._generate_settlement_fails()
        self._generate_fail_charges()

        # Write CSV files
        self._write_csv_files()

        print("\n✅ Data generation complete!")
        self._print_statistics()

    def _generate_broker_dealers(self):
        """Generate broker-dealer firms."""
        print("Generating broker-dealers...")
        row_count = self.schema['tables']['broker_dealers']['row_count']

        # Create mix of US, JP, EU brokers
        us_count = int(row_count * 0.60)
        jp_count = int(row_count * 0.20)
        eu_count = row_count - us_count - jp_count

        broker_id = 0

        # US brokers
        for i in range(us_count):
            broker = self._create_broker_dealer('US', broker_id)
            self.broker_dealers.append(broker)
            self.broker_dealer_lookup[broker['broker_dealer_id']] = broker
            broker_id += 1

        # Japan brokers
        for i in range(jp_count):
            broker = self._create_broker_dealer('JP', broker_id)
            self.broker_dealers.append(broker)
            self.broker_dealer_lookup[broker['broker_dealer_id']] = broker
            broker_id += 1

        # EU brokers
        for i in range(eu_count):
            broker = self._create_broker_dealer('EU', broker_id)
            self.broker_dealers.append(broker)
            self.broker_dealer_lookup[broker['broker_dealer_id']] = broker
            broker_id += 1

        print(f"  ✓ Generated {len(self.broker_dealers)} broker-dealers")

    def _create_broker_dealer(self, primary_market: str, index: int) -> Dict:
        """Create a single broker-dealer."""
        broker_types = ['buy_side', 'sell_side', 'market_maker', 'prime_broker']
        broker_type_weights = [0.30, 0.35, 0.20, 0.15]

        # Select firm name based on market
        if primary_market == 'US':
            firm_name = self.broker_names_us[index % len(self.broker_names_us)]
        elif primary_market == 'JP':
            firm_name = self.broker_names_jp[index % len(self.broker_names_jp)]
        else:
            firm_name = self.broker_names_eu[index % len(self.broker_names_eu)]

        # Determine market coverage
        if random.random() < 0.70:
            # Single market
            market_coverage = primary_market
        elif random.random() < 0.60:
            # Two markets
            other_markets = [m for m in ['US', 'JP', 'EU'] if m != primary_market]
            market_coverage = ','.join([primary_market, random.choice(other_markets)])
        else:
            # All markets
            market_coverage = 'US,JP,EU'

        # DTC number (only for US participants)
        dtc_number = f"{random.randint(1000, 9999)}" if primary_market == 'US' or 'US' in market_coverage else None

        return {
            'broker_dealer_id': str(uuid.uuid4()),
            'firm_name': firm_name,
            'dtc_participant_number': dtc_number,
            'broker_type': random.choices(broker_types, broker_type_weights)[0],
            'primary_market': primary_market,
            'market_coverage': market_coverage,
            'credit_rating': random.choices(
                ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+'],
                [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05]
            )[0],
            'settlement_efficiency': round(random.uniform(0.8000, 0.9900), 4),
            'created_at': self._random_timestamp_in_period()
        }

    def _generate_investors(self):
        """Generate institutional and retail investors."""
        print("Generating investors...")
        row_count = self.schema['tables']['investors']['row_count']

        # 15% institutional, 85% retail
        inst_count = int(row_count * 0.15)
        retail_count = row_count - inst_count

        # Generate institutional
        for i in range(inst_count):
            investor = self._create_investor('institutional', i)
            self.investors.append(investor)
            self.investor_lookup[investor['investor_id']] = investor

        # Generate retail
        for i in range(retail_count):
            investor = self._create_investor('retail', i)
            self.investors.append(investor)
            self.investor_lookup[investor['investor_id']] = investor

        print(f"  ✓ Generated {len(self.investors)} investors ({inst_count} institutional, {retail_count} retail)")

    def _create_investor(self, investor_type: str, index: int) -> Dict:
        """Create a single investor."""
        countries = ['US', 'JP', 'GB', 'FR', 'DE']
        country_weights = [0.65, 0.15, 0.08, 0.07, 0.05]
        country = random.choices(countries, country_weights)[0]

        if investor_type == 'institutional':
            investor_name = f"{self.institutional_names[index % len(self.institutional_names)]} - {random.choice(['Fund A', 'Fund B', 'Fund C', 'Portfolio I', 'Portfolio II'])}"
            subtypes = ['hedge_fund', 'mutual_fund', 'pension_fund', 'insurance', 'asset_manager']
            subtype = random.choice(subtypes)
        else:
            # Retail investor - generic name
            first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Mary']
            last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
            investor_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            subtype = 'individual'

        # Select primary broker (prefer brokers from same region)
        region_brokers = [b for b in self.broker_dealers
                         if b['primary_market'] == country or country in ['GB', 'FR', 'DE'] and b['primary_market'] == 'EU']
        if not region_brokers:
            region_brokers = self.broker_dealers

        primary_broker = random.choice(region_brokers)

        # Custodian
        if country == 'US':
            custodian = random.choice(self.custodians_us)
        else:
            custodian = random.choice(self.custodians_intl)

        return {
            'investor_id': str(uuid.uuid4()),
            'investor_type': investor_type,
            'investor_name': investor_name,
            'investor_subtype': subtype,
            'country': country,
            'primary_broker_id': primary_broker['broker_dealer_id'],
            'account_number': f"{'INV' if investor_type == 'institutional' else 'RTL'}{random.randint(100000000, 999999999)}",
            'custodian_bank': custodian if investor_type == 'institutional' else (custodian if random.random() < 0.3 else None),
            'created_at': self._random_timestamp_in_period()
        }

    def _generate_securities(self):
        """Generate equity securities."""
        print("Generating securities...")
        row_count = self.schema['tables']['securities']['row_count']

        # Split by market
        us_count = int(row_count * 0.60)
        jp_count = int(row_count * 0.20)
        eu_count = row_count - us_count - jp_count

        security_id = 0

        # US securities
        for i in range(us_count):
            security = self._create_security('US', security_id)
            self.securities.append(security)
            self.security_lookup[security['security_id']] = security
            security_id += 1

        # JP securities
        for i in range(jp_count):
            security = self._create_security('JP', security_id)
            self.securities.append(security)
            self.security_lookup[security['security_id']] = security
            security_id += 1

        # EU securities
        for i in range(eu_count):
            security = self._create_security('EU', security_id)
            self.securities.append(security)
            self.security_lookup[security['security_id']] = security
            security_id += 1

        print(f"  ✓ Generated {len(self.securities)} securities")

    def _create_security(self, market: str, index: int) -> Dict:
        """Create a single security."""
        sectors = list(self.companies.keys())
        sector_weights = [0.25, 0.18, 0.15, 0.14, 0.12, 0.06, 0.04, 0.03, 0.03]
        sector = random.choices(sectors, sector_weights)[0]

        company_name = random.choice(self.companies[sector])

        # Generate ticker
        if market == 'US':
            ticker = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.choice([3, 4])))
            cusip = CUSIPGenerator.generate_cusip()
            isin = ISINGenerator.generate_isin('US', cusip)
            currency = 'USD'
            exchange = random.choice(self.exchanges['US'])
        elif market == 'JP':
            ticker = f"{random.randint(1000, 9999)}"
            cusip = None
            isin = ISINGenerator.generate_isin('JP')
            currency = 'JPY'
            exchange = random.choice(self.exchanges['JP'])
        else:  # EU
            ticker = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.choice([2, 3, 4])))
            country_codes = ['GB', 'FR', 'DE', 'CH']
            country = random.choice(country_codes)
            cusip = None
            isin = ISINGenerator.generate_isin(country)
            currency = 'EUR' if country in ['FR', 'DE'] else ('GBP' if country == 'GB' else 'CHF')
            exchange = random.choice(self.exchanges['EU'])

        # Market cap and liquidity
        market_cap_tiers = ['large_cap', 'mid_cap', 'small_cap']
        market_cap_weights = [0.30, 0.40, 0.30]
        market_cap_tier = random.choices(market_cap_tiers, market_cap_weights)[0]

        liquidity_tiers = ['high', 'medium', 'low']
        liquidity_weights = [0.35, 0.45, 0.20]
        liquidity_tier = random.choices(liquidity_tiers, liquidity_weights)[0]

        # Average daily volume based on liquidity and market cap
        base_volumes = {
            ('large_cap', 'high'): (5_000_000, 50_000_000),
            ('large_cap', 'medium'): (1_000_000, 5_000_000),
            ('large_cap', 'low'): (100_000, 1_000_000),
            ('mid_cap', 'high'): (500_000, 5_000_000),
            ('mid_cap', 'medium'): (100_000, 500_000),
            ('mid_cap', 'low'): (10_000, 100_000),
            ('small_cap', 'high'): (100_000, 1_000_000),
            ('small_cap', 'medium'): (10_000, 100_000),
            ('small_cap', 'low'): (1_000, 10_000)
        }

        vol_min, vol_max = base_volumes.get((market_cap_tier, liquidity_tier), (10_000, 100_000))
        avg_daily_volume = random.randint(vol_min, vol_max)

        # Stock price based on market
        if market == 'US':
            price = round(random.uniform(10.0, 500.0), 4)
        elif market == 'JP':
            price = round(random.uniform(500.0, 10000.0), 2)
        else:  # EU
            price = round(random.uniform(5.0, 200.0), 4)

        return {
            'security_id': str(uuid.uuid4()),
            'ticker': ticker,
            'cusip': cusip,
            'isin': isin,
            'security_name': company_name,
            'market': market,
            'exchange': exchange,
            'currency': currency,
            'sector': sector,
            'market_cap_tier': market_cap_tier,
            'liquidity_tier': liquidity_tier,
            'average_daily_volume': avg_daily_volume,
            'current_price': price,
            'created_at': self._random_timestamp_in_period()
        }

    def _generate_trades(self):
        """Generate trade executions."""
        print("Generating trades...")
        row_count = self.schema['tables']['trades']['row_count']

        for i in range(row_count):
            trade = self._create_trade()
            self.trades.append(trade)

            if (i + 1) % 50000 == 0:
                print(f"  → Generated {i + 1:,} trades...")

        print(f"  ✓ Generated {len(self.trades):,} trades")

    def _create_trade(self) -> Dict:
        """Create a single trade."""
        # Select random security
        security = random.choice(self.securities)
        market = security['market']

        # Select investor (prefer investors from same region)
        region_investors = [inv for inv in self.investors
                           if inv['country'] == market or (market == 'EU' and inv['country'] in ['GB', 'FR', 'DE'])]
        if not region_investors:
            region_investors = self.investors

        investor = random.choice(region_investors)

        # Get investor's primary broker
        executing_broker = self.broker_dealer_lookup[investor['primary_broker_id']]

        # Select counterparty broker (different from executing broker)
        counterparty_brokers = [b for b in self.broker_dealers
                               if b['broker_dealer_id'] != executing_broker['broker_dealer_id']
                               and (market in b['market_coverage'].split(','))]
        if not counterparty_brokers:
            counterparty_brokers = [b for b in self.broker_dealers
                                   if b['broker_dealer_id'] != executing_broker['broker_dealer_id']]

        counterparty_broker = random.choice(counterparty_brokers)

        # Trade side
        trade_side = random.choice(['buy', 'sell'])

        # Quantity based on investor type
        if investor['investor_type'] == 'institutional':
            quantity = random.randint(10000, 500000)
        else:
            quantity = random.randint(10, 1000)

        # Price (add some variance to current price)
        price_variance = random.uniform(0.95, 1.05)
        price = round(float(security['current_price']) * price_variance, 4)

        # Amounts
        gross_amount = round(quantity * price, 2)

        # Commission based on investor type
        if investor['investor_type'] == 'institutional':
            commission_rate = random.uniform(0.0005, 0.002)  # 5-20 bps
        else:
            commission_rate = random.uniform(0.005, 0.015)  # 50-150 bps

        commission = round(gross_amount * commission_rate, 2)

        if trade_side == 'buy':
            net_amount = round(gross_amount + commission, 2)
        else:
            net_amount = round(gross_amount - commission, 2)

        # Trade date
        trade_date = self._random_date_in_period()

        # Ensure it's a business day
        while not BusinessDayCalculator.is_business_day(trade_date, market):
            trade_date = self._random_date_in_period()

        # Trade time (during market hours)
        if market == 'US':
            hour = random.randint(9, 15)  # 9:30 AM - 4:00 PM EST
        elif market == 'JP':
            hour = random.randint(9, 14)  # 9:00 AM - 3:00 PM JST
        else:  # EU
            hour = random.randint(8, 16)  # 8:00 AM - 4:30 PM CET

        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        trade_time = datetime.combine(trade_date, datetime.min.time()).replace(
            hour=hour, minute=minute, second=second
        )

        # Settlement date (T+1 for US, T+2 for JP/EU)
        settlement_cycle = 1 if market == 'US' else 2
        settlement_date = BusinessDayCalculator.add_business_days(trade_date, settlement_cycle, market)

        # Trade status
        trade_status = random.choices(
            ['executed', 'confirmed', 'allocated', 'cancelled'],
            [0.02, 0.95, 0.02, 0.01]
        )[0]

        return {
            'trade_id': str(uuid.uuid4()),
            'trade_reference': f"TRD{random.randint(10000000, 99999999)}",
            'security_id': security['security_id'],
            'investor_id': investor['investor_id'],
            'executing_broker_id': executing_broker['broker_dealer_id'],
            'counterparty_broker_id': counterparty_broker['broker_dealer_id'],
            'trade_side': trade_side,
            'quantity': quantity,
            'price': price,
            'gross_amount': gross_amount,
            'commission': commission,
            'net_amount': net_amount,
            'trade_date': trade_date.isoformat(),
            'trade_time': trade_time.isoformat(),
            'settlement_date': settlement_date.isoformat(),
            'trade_status': trade_status,
            'execution_venue': security['exchange'],
            'created_at': trade_time.isoformat()
        }

    def _generate_settlement_instructions(self):
        """Generate settlement instructions for trades."""
        print("Generating settlement instructions...")

        for trade in self.trades:
            if trade['trade_status'] == 'cancelled':
                continue

            ssi = self._create_settlement_instruction(trade)
            self.settlement_instructions.append(ssi)

        print(f"  ✓ Generated {len(self.settlement_instructions):,} settlement instructions")

    def _create_settlement_instruction(self, trade: Dict) -> Dict:
        """Create settlement instruction for a trade."""
        security = self.security_lookup[trade['security_id']]
        investor = self.investor_lookup[trade['investor_id']]

        # Instruction type
        if trade['trade_side'] == 'buy':
            instruction_type = 'RVP'  # Receive vs Payment
        else:
            instruction_type = 'DVP'  # Delivery vs Payment

        if random.random() < 0.02:
            instruction_type = 'FOP'  # Free of Payment (rare)

        # Settlement method
        if security['market'] == 'US':
            settlement_method = 'DTC'
        elif security['market'] == 'JP':
            settlement_method = 'JSCC'
        else:  # EU
            settlement_method = random.choice(['Euroclear', 'Clearstream'])

        # Custodian
        custodian = investor.get('custodian_bank') or random.choice(
            self.custodians_us if security['market'] == 'US' else self.custodians_intl
        )

        # Status
        instruction_status = random.choices(
            ['pending', 'affirmed', 'matched', 'rejected'],
            [0.05, 0.10, 0.83, 0.02]
        )[0]

        # Timestamps
        trade_time = datetime.fromisoformat(trade['trade_time'])

        if instruction_status in ['affirmed', 'matched']:
            affirm_delay = timedelta(minutes=random.randint(30, 2880))  # 30 min to 48 hours
            affirmation_timestamp = trade_time + affirm_delay
        else:
            affirmation_timestamp = None

        if instruction_status == 'matched' and affirmation_timestamp:
            match_delay = timedelta(minutes=random.randint(5, 120))
            matching_timestamp = affirmation_timestamp + match_delay
        else:
            matching_timestamp = None

        return {
            'ssi_id': str(uuid.uuid4()),
            'trade_id': trade['trade_id'],
            'instruction_type': instruction_type,
            'settlement_method': settlement_method,
            'custodian': custodian,
            'custodian_account': f"CUST{random.randint(100000, 999999)}",
            'agent_bank': random.choice(self.custodians_us + self.custodians_intl),
            'payment_currency': security['currency'],
            'instruction_status': instruction_status,
            'affirmation_timestamp': affirmation_timestamp.isoformat() if affirmation_timestamp else None,
            'matching_timestamp': matching_timestamp.isoformat() if matching_timestamp else None,
            'created_at': (trade_time + timedelta(minutes=random.randint(1, 30))).isoformat()
        }

    def _generate_settlements(self):
        """Generate settlement attempts."""
        print("Generating settlements...")

        # Create settlement for each SSI
        for ssi in self.settlement_instructions:
            trade = next(t for t in self.trades if t['trade_id'] == ssi['trade_id'])
            settlement = self._create_settlement(trade, ssi)
            self.settlements.append(settlement)

        print(f"  ✓ Generated {len(self.settlements):,} settlements")

        # Count fails
        fail_count = sum(1 for s in self.settlements if s['settlement_status'] == 'failed')
        fail_rate = fail_count / len(self.settlements) if self.settlements else 0
        print(f"  ⚠️  Settlement fails: {fail_count:,} ({fail_rate*100:.1f}%)")

    def _create_settlement(self, trade: Dict, ssi: Dict) -> Dict:
        """Create a settlement record."""
        security = self.security_lookup[trade['security_id']]

        scheduled_date = date.fromisoformat(trade['settlement_date'])

        # Determine if settlement fails based on multiple factors
        fail_probability = self.fail_rate

        # Adjust fail probability based on:
        # 1. Liquidity tier (low liquidity = higher fails)
        if security['liquidity_tier'] == 'low':
            fail_probability *= 1.5
        elif security['liquidity_tier'] == 'high':
            fail_probability *= 0.7

        # 2. SSI status (not matched = higher fails)
        if ssi['instruction_status'] != 'matched':
            fail_probability *= 2.0

        # 3. Broker efficiency
        executing_broker = self.broker_dealer_lookup[trade['executing_broker_id']]
        if executing_broker['settlement_efficiency'] < 0.85:
            fail_probability *= 1.3

        # Cap probability
        fail_probability = min(fail_probability, 0.45)

        # Determine status
        if random.random() < fail_probability:
            settlement_status = 'failed'
            actual_settlement_date = None
            settled_quantity = None
        elif random.random() < 0.02:
            settlement_status = 'partial'
            actual_settlement_date = scheduled_date
            settled_quantity = int(trade['quantity'] * random.uniform(0.5, 0.9))
        elif random.random() < 0.01:
            settlement_status = 'pending'
            actual_settlement_date = None
            settled_quantity = None
        else:
            settlement_status = 'settled'
            actual_settlement_date = scheduled_date
            settled_quantity = trade['quantity']

        # Settlement location
        settlement_location = ssi['settlement_method']

        return {
            'settlement_id': str(uuid.uuid4()),
            'trade_id': trade['trade_id'],
            'ssi_id': ssi['ssi_id'],
            'settlement_reference': f"STL{random.randint(10000000, 99999999)}",
            'scheduled_settlement_date': scheduled_date.isoformat(),
            'actual_settlement_date': actual_settlement_date.isoformat() if actual_settlement_date else None,
            'settlement_status': settlement_status,
            'settlement_amount': trade['net_amount'],
            'settled_quantity': settled_quantity,
            'settlement_location': settlement_location,
            'value_date': actual_settlement_date.isoformat() if actual_settlement_date else None,
            'created_at': datetime.combine(scheduled_date, datetime.min.time()).replace(
                hour=random.randint(8, 18), minute=random.randint(0, 59)
            ).isoformat()
        }

    def _generate_settlement_fails(self):
        """Generate detailed fail tracking records."""
        print("Generating settlement fails...")

        failed_settlements = [s for s in self.settlements if s['settlement_status'] == 'failed']

        for settlement in failed_settlements:
            fail = self._create_settlement_fail(settlement)
            self.settlement_fails.append(fail)

        print(f"  ✓ Generated {len(self.settlement_fails):,} fail records")

    def _create_settlement_fail(self, settlement: Dict) -> Dict:
        """Create a settlement fail record."""
        trade = next(t for t in self.trades if t['trade_id'] == settlement['trade_id'])
        security = self.security_lookup[trade['security_id']]

        # Fail category
        fail_categories = ['insufficient_securities', 'cash_shortfall', 'operational', 'custody', 'other']
        fail_category_weights = [0.40, 0.25, 0.20, 0.10, 0.05]
        fail_category = random.choices(fail_categories, fail_category_weights)[0]

        # Specific fail reason
        fail_reason = random.choice(self.fail_reasons[fail_category])

        # Failing party
        if fail_category == 'insufficient_securities':
            failing_party = 'seller' if trade['trade_side'] == 'buy' else 'buyer'
        elif fail_category == 'cash_shortfall':
            failing_party = 'buyer' if trade['trade_side'] == 'buy' else 'seller'
        else:
            failing_party = random.choices(['buyer', 'seller', 'intermediary'], [0.30, 0.55, 0.15])[0]

        # Fail start date
        fail_start_date = date.fromisoformat(settlement['scheduled_settlement_date'])

        # Fail age (days outstanding)
        # Distribution: most fails resolved quickly, some aged
        age_buckets = [(0, 3), (4, 10), (11, 20), (21, 60)]
        age_weights = [0.60, 0.25, 0.10, 0.05]
        min_age, max_age = random.choices(age_buckets, age_weights)[0]
        fail_age_days = random.randint(min_age, max_age)

        # Fail status based on age
        if fail_age_days <= 3:
            # Recent fails: mostly active, some resolved
            fail_status = random.choices(
                ['active', 'resolved'],
                [0.40, 0.60]
            )[0]
        elif fail_age_days <= 10:
            # Aged fails
            fail_status = random.choices(
                ['active', 'resolved', 'buy_in_initiated'],
                [0.45, 0.45, 0.10]
            )[0]
        elif fail_age_days <= 20:
            # Extended fails
            fail_status = random.choices(
                ['active', 'resolved', 'buy_in_initiated', 'closed_out'],
                [0.30, 0.40, 0.20, 0.10]
            )[0]
        else:
            # Chronic fails
            fail_status = random.choices(
                ['active', 'resolved', 'buy_in_initiated', 'closed_out', 'disputed'],
                [0.20, 0.30, 0.25, 0.20, 0.05]
            )[0]

        # Resolution method and date
        if fail_status == 'resolved':
            resolution_method = random.choice(self.resolution_methods)
            resolution_date = fail_start_date + timedelta(days=fail_age_days)
        elif fail_status in ['closed_out', 'buy_in_initiated']:
            resolution_method = 'Buy-in executed in market' if fail_status == 'buy_in_initiated' else 'Forced close-out by clearinghouse'
            resolution_date = fail_start_date + timedelta(days=fail_age_days)
        else:
            resolution_method = None
            resolution_date = None

        # Buy-in date (for chronic fails)
        if fail_age_days >= 21 and fail_status in ['buy_in_initiated', 'closed_out']:
            buy_in_date = fail_start_date + timedelta(days=21)
        else:
            buy_in_date = None

        # Fail quantity and value
        fail_quantity = trade['quantity']
        fail_value = float(trade['net_amount'])

        # Regulatory threshold breach (e.g., $250M for US)
        threshold = 250_000_000
        regulatory_breach = fail_value >= threshold

        return {
            'fail_id': str(uuid.uuid4()),
            'settlement_id': settlement['settlement_id'],
            'trade_id': trade['trade_id'],
            'fail_reference': f"FAIL{random.randint(10000000, 99999999)}",
            'fail_category': fail_category,
            'fail_reason': fail_reason,
            'failing_party': failing_party,
            'fail_quantity': fail_quantity,
            'fail_value': fail_value,
            'fail_start_date': fail_start_date.isoformat(),
            'fail_age_days': fail_age_days,
            'fail_status': fail_status,
            'resolution_method': resolution_method,
            'resolution_date': resolution_date.isoformat() if resolution_date else None,
            'buy_in_date': buy_in_date.isoformat() if buy_in_date else None,
            'regulatory_threshold_breach': regulatory_breach,
            'notification_sent': True,
            'created_at': datetime.combine(fail_start_date, datetime.min.time()).replace(
                hour=random.randint(8, 18), minute=random.randint(0, 59)
            ).isoformat()
        }

    def _generate_fail_charges(self):
        """Generate penalty charges for fails."""
        print("Generating fail charges...")

        for fail in self.settlement_fails:
            # Generate multiple charges for each fail based on age
            num_charges = self._calculate_charge_count(fail)

            for i in range(num_charges):
                charge = self._create_fail_charge(fail, i)
                self.fail_charges.append(charge)

        print(f"  ✓ Generated {len(self.fail_charges):,} fail charges")

    def _calculate_charge_count(self, fail: Dict) -> int:
        """Calculate how many charges to generate for a fail."""
        age = fail['fail_age_days']

        # Daily fail fees for each day
        daily_fees = min(age, 10)  # Cap at 10 daily fees

        # Additional charges
        additional = 0

        # Buy-in cost if buy-in was initiated
        if fail['buy_in_date']:
            additional += 1

        # Administrative fee for aged fails
        if age >= 10:
            additional += 1

        # Regulatory fine for threshold breaches
        if fail['regulatory_threshold_breach']:
            additional += 1

        # Interest charges for extended fails
        if age >= 5:
            additional += random.randint(1, 3)

        return daily_fees + additional

    def _create_fail_charge(self, fail: Dict, charge_index: int) -> Dict:
        """Create a single fail charge."""
        trade = next(t for t in self.trades if t['trade_id'] == fail['trade_id'])
        security = self.security_lookup[trade['security_id']]

        fail_start = date.fromisoformat(fail['fail_start_date'])
        fail_value = fail['fail_value']

        # Determine charge type
        if charge_index < fail['fail_age_days'] and charge_index < 10:
            # Daily fail fee
            charge_type = 'daily_fail_fee'
            charge_date = fail_start + timedelta(days=charge_index + 1)

            # Daily fail fee calculation (typically basis points per day)
            daily_rate = random.uniform(0.0001, 0.0005)  # 1-5 bps per day
            charge_amount = round(fail_value * daily_rate, 2)

            calculation_method = f"Daily fail fee: {fail_value:,.2f} × {daily_rate*10000:.2f} bps"

        elif fail.get('buy_in_date') and random.random() < 0.5:
            # Buy-in cost
            charge_type = 'buy_in_cost'
            charge_date = date.fromisoformat(fail['buy_in_date'])

            # Buy-in cost: difference between buy-in price and original price
            price_impact = random.uniform(0.01, 0.05)  # 1-5% adverse price movement
            charge_amount = round(fail_value * price_impact, 2)

            calculation_method = f"Buy-in cost: Market price impact {price_impact*100:.2f}%"

        elif fail['fail_age_days'] >= 10 and random.random() < 0.3:
            # Administrative fee
            charge_type = 'administrative_fee'
            charge_date = fail_start + timedelta(days=10)

            # Fixed administrative fee
            charge_amount = round(random.uniform(50, 500), 2)

            calculation_method = "Administrative processing fee for aged fail"

        elif fail['regulatory_threshold_breach'] and random.random() < 0.2:
            # Regulatory fine
            charge_type = 'regulatory_fine'
            charge_date = fail_start + timedelta(days=random.randint(5, 15))

            # Regulatory fine (typically larger)
            charge_amount = round(random.uniform(1000, 10000), 2)

            calculation_method = "Regulatory fine for threshold breach"

        else:
            # Interest charge
            charge_type = 'interest_charge'
            charge_date = fail_start + timedelta(days=random.randint(1, max(1, fail['fail_age_days'])))

            # Interest charge
            interest_rate = random.uniform(0.0002, 0.001)  # 2-10 bps
            charge_amount = round(fail_value * interest_rate, 2)

            calculation_method = f"Interest charge: {fail_value:,.2f} × {interest_rate*10000:.2f} bps"

        # Charged party (same as failing party usually)
        charged_party = fail['failing_party']

        # Payment status
        if fail['fail_status'] == 'resolved':
            payment_status = random.choices(['paid', 'disputed', 'waived'], [0.85, 0.10, 0.05])[0]
        else:
            payment_status = random.choices(['pending', 'paid', 'disputed'], [0.40, 0.50, 0.10])[0]

        return {
            'charge_id': str(uuid.uuid4()),
            'fail_id': fail['fail_id'],
            'charge_date': charge_date.isoformat(),
            'charge_type': charge_type,
            'charge_amount': charge_amount,
            'charge_currency': security['currency'],
            'charged_party': charged_party,
            'payment_status': payment_status,
            'calculation_method': calculation_method,
            'created_at': datetime.combine(charge_date, datetime.min.time()).replace(
                hour=random.randint(8, 18), minute=random.randint(0, 59)
            ).isoformat()
        }

    def _random_date_in_period(self) -> date:
        """Generate a random date within the generation period."""
        days_between = (self.end_date - self.start_date).days
        random_days = random.randint(0, days_between)
        return self.start_date + timedelta(days=random_days)

    def _random_timestamp_in_period(self) -> str:
        """Generate a random timestamp within the generation period."""
        random_date = self._random_date_in_period()
        random_time = datetime.combine(random_date, datetime.min.time()).replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        return random_time.isoformat()

    def _write_csv_files(self):
        """Write all generated data to CSV files."""
        print("\n📝 Writing CSV files...")

        self.output_dir.mkdir(parents=True, exist_ok=True)

        tables = {
            'broker_dealers': self.broker_dealers,
            'investors': self.investors,
            'securities': self.securities,
            'trades': self.trades,
            'settlement_instructions': self.settlement_instructions,
            'settlements': self.settlements,
            'settlement_fails': self.settlement_fails,
            'fail_charges': self.fail_charges
        }

        for table_name, data in tables.items():
            if not data:
                continue

            csv_path = self.output_dir / f"{table_name}.csv"

            with open(csv_path, 'w', newline='') as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)

            print(f"  ✓ {table_name}.csv ({len(data):,} rows)")

    def _print_statistics(self):
        """Print generation statistics."""
        print("\n📊 Generation Statistics:")
        print(f"  Broker-dealers: {len(self.broker_dealers):,}")
        print(f"  Investors: {len(self.investors):,}")
        print(f"  Securities: {len(self.securities):,}")
        print(f"  Trades: {len(self.trades):,}")
        print(f"  Settlement instructions: {len(self.settlement_instructions):,}")
        print(f"  Settlements: {len(self.settlements):,}")
        print(f"  Settlement fails: {len(self.settlement_fails):,}")
        print(f"  Fail charges: {len(self.fail_charges):,}")

        # Fail analysis
        if self.settlement_fails:
            print("\n⚠️  Settlement Fail Analysis:")

            # By category
            category_counts = defaultdict(int)
            for fail in self.settlement_fails:
                category_counts[fail['fail_category']] += 1

            print("  By category:")
            for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                pct = (count / len(self.settlement_fails)) * 100
                print(f"    {category}: {count:,} ({pct:.1f}%)")

            # By status
            status_counts = defaultdict(int)
            for fail in self.settlement_fails:
                status_counts[fail['fail_status']] += 1

            print("  By status:")
            for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
                pct = (count / len(self.settlement_fails)) * 100
                print(f"    {status}: {count:,} ({pct:.1f}%)")

            # Aged fails
            aged_fails = [f for f in self.settlement_fails if f['fail_age_days'] >= 10]
            chronic_fails = [f for f in self.settlement_fails if f['fail_age_days'] >= 21]

            print(f"  Aged fails (10+ days): {len(aged_fails):,}")
            print(f"  Chronic fails (21+ days): {len(chronic_fails):,}")

            # Total fail value
            total_fail_value = sum(f['fail_value'] for f in self.settlement_fails)
            print(f"  Total fail value: ${total_fail_value:,.2f}")


def main():
    parser = argparse.ArgumentParser(description='Generate securities settlement data with focus on fails')
    parser.add_argument('schema', help='Path to schema JSON file')
    parser.add_argument('output_dir', help='Output directory for CSV files')
    parser.add_argument('--fail-rate', type=float, default=0.15,
                       help='Target settlement fail rate (default: 0.15 = 15%%)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')

    args = parser.parse_args()

    if args.seed:
        random.seed(args.seed)

    # Validate fail rate
    if not 0.01 <= args.fail_rate <= 0.50:
        print(f"ERROR: Fail rate must be between 0.01 (1%%) and 0.50 (50%%)")
        sys.exit(1)

    generator = SecuritiesDataGenerator(args.schema, args.output_dir, args.fail_rate)
    generator.generate_all_data()


if __name__ == '__main__':
    main()
