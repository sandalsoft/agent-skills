#!/usr/bin/env python3
"""
Coherent US Banking Data Generator

Generates realistic, coherent banking data where:
- Emails match customer names
- Merchant names match their countries
- Geographic data is consistent (city/state/zip)
- Transaction dates follow correct ordering
- Distributions match realistic banking patterns
"""

import json
import csv
import random
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Dict, List, Any, Tuple
import sys

# Load the existing name and merchant distributions
sys.path.insert(0, '/Users/eric/.claude/skills/datagen-financialv2')
from scripts.generate_data import RealisticNameGenerator, LocationGenerator


class CoherentBankingDataGenerator:
    """Generate coherent US banking data."""

    def __init__(self, schema_path: str, output_dir: str):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize generators
        skill_assets = Path('/Users/eric/.claude/skills/datagen-financialv2/assets')
        self.name_gen = RealisticNameGenerator(str(skill_assets / 'name_distributions.json'))
        self.location_gen = LocationGenerator(str(skill_assets / 'merchant_types.json'))

        # Load corporate domains
        with open(skill_assets / 'corporate_domains.json', 'r') as f:
            data = json.load(f)
            self.corporate_domains = data['domains']

        # Storage for generated data (for referential integrity)
        self.customers = []
        self.accounts = []
        self.loans = []
        self.cards = []
        self.wealth_portfolios = []

        # Date range
        period = self.schema['data_generation_period']
        self.start_date = datetime.strptime(period['start_date'], '%Y-%m-%d')
        self.end_date = datetime.strptime(period['end_date'], '%Y-%m-%d')

        # Merchant categories with realistic names
        self.merchant_categories = {
            'restaurants': ['Olive Garden', 'Red Lobster', 'Cheesecake Factory', 'Outback Steakhouse', 'P.F. Chang\'s',
                           'The Capital Grille', 'Ruth\'s Chris', 'Texas Roadhouse', 'Applebee\'s', 'Chili\'s'],
            'grocery': ['Whole Foods', 'Trader Joe\'s', 'Safeway', 'Kroger', 'Publix', 'Wegmans', 'H-E-B',
                       'Stop & Shop', 'Food Lion', 'Giant Eagle'],
            'gas_stations': ['Shell', 'Exxon', 'Chevron', 'BP', '76', 'Valero', 'Mobil', 'Sunoco', 'Marathon', 'Speedway'],
            'retail': ['Target', 'Walmart', 'Costco', 'Best Buy', 'Home Depot', 'Lowe\'s', 'Macy\'s',
                      'Nordstrom', 'Gap', 'Old Navy'],
            'online': ['Amazon', 'eBay', 'Etsy', 'Wayfair', 'Zappos', 'Chewy', 'Overstock'],
            'entertainment': ['AMC Theatres', 'Regal Cinemas', 'Dave & Buster\'s', 'Spotify', 'Netflix', 'Hulu'],
        }

        # Bill payment billers by type
        self.billers = {
            'electricity': ['Pacific Gas & Electric', 'Con Edison', 'Duke Energy', 'Southern California Edison',
                           'Florida Power & Light', 'Georgia Power', 'ComEd', 'Ameren'],
            'water': ['City Water Department', 'Municipal Water District', 'County Water Authority'],
            'telecom': ['Verizon', 'AT&T', 'T-Mobile', 'Sprint'],
            'internet': ['Comcast Xfinity', 'Spectrum', 'Cox Communications', 'AT&T Internet', 'Verizon Fios'],
            'insurance': ['State Farm', 'Geico', 'Progressive', 'Allstate', 'Farmers Insurance', 'Liberty Mutual'],
            'education': ['University Bursar', 'College Tuition Office', 'School District'],
            'government': ['IRS', 'State Tax Board', 'DMV', 'County Tax Collector'],
        }

        # International countries for transactions/wires (5% of total)
        self.intl_countries = {
            'GB': {'name': 'United Kingdom', 'currency': 'GBP', 'cities': ['London', 'Manchester', 'Birmingham']},
            'CA': {'name': 'Canada', 'currency': 'CAD', 'cities': ['Toronto', 'Vancouver', 'Montreal']},
            'MX': {'name': 'Mexico', 'currency': 'MXN', 'cities': ['Mexico City', 'Cancun', 'Guadalajara']},
            'FR': {'name': 'France', 'currency': 'EUR', 'cities': ['Paris', 'Lyon', 'Marseille']},
            'DE': {'name': 'Germany', 'currency': 'EUR', 'cities': ['Berlin', 'Munich', 'Frankfurt']},
            'JP': {'name': 'Japan', 'currency': 'JPY', 'cities': ['Tokyo', 'Osaka', 'Kyoto']},
            'AU': {'name': 'Australia', 'currency': 'AUD', 'cities': ['Sydney', 'Melbourne', 'Brisbane']},
            'IN': {'name': 'India', 'currency': 'INR', 'cities': ['Mumbai', 'Delhi', 'Bangalore']},
        }

        # Security names for investments
        self.securities = {
            'stock': ['Apple Inc.', 'Microsoft Corp.', 'Amazon.com Inc.', 'Tesla Inc.', 'Google (Alphabet)',
                     'Meta Platforms', 'NVIDIA Corp.', 'Berkshire Hathaway', 'Johnson & Johnson', 'JPMorgan Chase'],
            'bond': ['US Treasury 10Y', 'US Treasury 30Y', 'Corporate Bond AAA', 'Municipal Bond',
                    'Investment Grade Corporate'],
            'mutual_fund': ['Vanguard 500 Index', 'Fidelity Contra Fund', 'PIMCO Total Return',
                           'T. Rowe Price Growth', 'American Funds Growth'],
            'etf': ['SPY - S&P 500 ETF', 'QQQ - Nasdaq 100 ETF', 'VTI - Total Market ETF',
                   'AGG - Bond ETF', 'VNQ - Real Estate ETF'],
            'real_estate': ['REIT - Residential', 'REIT - Commercial', 'REIT - Industrial', 'Real Estate Fund'],
        }

    def _random_date(self, start: datetime, end: datetime) -> datetime:
        """Generate random datetime between start and end."""
        if start >= end:
            # If start is after or equal to end, return start with small offset
            return start + timedelta(seconds=random.randint(0, 3600))

        delta = end - start
        if delta.days == 0:
            # Same day - just randomize time
            random_seconds = random.randint(0, min(delta.seconds, 86400))
            return start + timedelta(seconds=random_seconds)
        random_days = random.randint(0, delta.days)
        random_seconds = random.randint(0, 86400)
        return start + timedelta(days=random_days, seconds=random_seconds)

    def _lognormal_amount(self, mean: float, std: float, min_val: float, max_val: float) -> float:
        """Generate amount using lognormal distribution (biased towards higher amounts when std is large)."""
        # Use lognormal for realistic wealth/amount distributions
        import math
        mu = math.log(mean**2 / math.sqrt(mean**2 + std**2))
        sigma = math.sqrt(math.log(1 + (std**2 / mean**2)))
        value = random.lognormvariate(mu, sigma)
        return round(max(min_val, min(max_val, value)), 2)

    def generate_customers(self):
        """Generate customer data with coherent names and emails."""
        print("📊 Generating customers...")
        row_count = self.schema['tables']['customers']['row_count']

        # Get distribution
        dist = self.schema['tables']['customers']['columns']['customer_type']['distribution']

        for i in range(row_count):
            # Determine customer type based on distribution
            rand = random.random()
            if rand < dist['retail']:
                customer_type = 'retail'
            elif rand < dist['retail'] + dist['commercial']:
                customer_type = 'commercial'
            else:
                customer_type = 'corporate'

            is_business = customer_type in ('commercial', 'corporate')

            # Generate name
            first_name, last_name = self.name_gen.generate_unique_name()

            # Generate COHERENT email from the same name
            if is_business and self.corporate_domains:
                domain_data = random.choice(self.corporate_domains)
                email = f"{first_name.lower()}.{last_name.lower()}@{domain_data['domain']}"
            else:
                domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'icloud.com', 'hotmail.com'])
                email = f"{first_name.lower()}.{last_name.lower()}@{domain}"

            # Generate coherent location
            location = self.location_gen.generate_location()

            # Determine segment based on customer type
            if customer_type == 'corporate':
                segment = 'corporate'
            elif customer_type == 'commercial':
                segment = random.choice(['business', 'priority'])
            else:
                segment = random.choices(
                    ['standard', 'priority', 'wealth'],
                    weights=[0.72, 0.22, 0.06]  # Adjusted within retail
                )[0]

            # Generate address
            if is_business:
                building = random.randint(1, 999)
                street = random.choice(['Corporate', 'Business', 'Commerce', 'Executive', 'Professional'])
                street_type = random.choice(['Plaza', 'Center', 'Park', 'Way', 'Drive'])
                address_line1 = f"{building} {street} {street_type}"
                address_line2 = f"Suite {random.randint(100, 2500)}" if random.random() < 0.6 else None
            else:
                number = random.randint(1, 9999)
                street = random.choice(['Main', 'Oak', 'Maple', 'Pine', 'Cedar', 'Elm', 'Park'])
                street_type = random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln'])
                address_line1 = f"{number} {street} {street_type}"
                address_line2 = f"Apt {random.randint(1, 999)}" if random.random() < 0.3 else None

            customer = {
                'customer_id': str(uuid.uuid4()),
                'customer_type': customer_type,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': f"{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",
                'address_line1': address_line1,
                'address_line2': address_line2,
                'city': location['city'],
                'state': location['state'],
                'postal_code': location['zip_code'],
                'date_of_birth': (datetime.now() - timedelta(days=random.randint(18*365, 85*365))).strftime('%Y-%m-%d'),
                'national_id': f"{random.randint(10, 99)}-{random.randint(1000000, 9999999)}",
                'customer_segment': segment,
                'created_at': self._random_date(self.start_date, self.end_date).strftime('%Y-%m-%d %H:%M:%S'),
            }

            self.customers.append(customer)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} customers...")

        # Write to CSV
        self._write_csv('customers', self.customers)
        print(f"  ✅ Generated {len(self.customers)} customers")

    def generate_accounts(self):
        """Generate bank accounts."""
        print("📊 Generating accounts...")
        row_count = self.schema['tables']['accounts']['row_count']

        dist = self.schema['tables']['accounts']['columns']['account_type']['distribution']
        status_dist = self.schema['tables']['accounts']['columns']['account_status']['distribution']

        for i in range(row_count):
            customer = random.choice(self.customers)
            customer_created = datetime.strptime(customer['created_at'], '%Y-%m-%d %H:%M:%S')

            # Account opened after customer created
            opened_at = self._random_date(customer_created, self.end_date)

            # Account type
            account_type = random.choices(
                list(dist.keys()),
                weights=list(dist.values())
            )[0]

            # Account status
            status = random.choices(
                list(status_dist.keys()),
                weights=list(status_dist.values())
            )[0]

            # Closed date if closed
            closed_at = None
            if status == 'closed':
                closed_at = self._random_date(opened_at, self.end_date).strftime('%Y-%m-%d %H:%M:%S')

            # Balance - lognormal distribution
            balance = self._lognormal_amount(8500, 25000, 0, 500000)

            # Interest rate depends on account type
            if account_type == 'checking':
                interest_rate = 0.0001 if random.random() < 0.1 else None  # Most checking accounts don't earn interest
            elif account_type == 'savings':
                interest_rate = round(random.uniform(0.0025, 0.0450), 4)
            elif account_type == 'certificate_deposit':
                interest_rate = round(random.uniform(0.0400, 0.0550), 4)
            else:  # money_market
                interest_rate = round(random.uniform(0.0350, 0.0500), 4)

            account = {
                'account_id': str(uuid.uuid4()),
                'customer_id': customer['customer_id'],
                'account_number': f"{random.randint(1000000000, 9999999999)}",
                'account_type': account_type,
                'account_status': status,
                'currency': 'USD',
                'balance': balance,
                'interest_rate': interest_rate,
                'opened_at': opened_at.strftime('%Y-%m-%d %H:%M:%S'),
                'closed_at': closed_at,
            }

            self.accounts.append(account)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} accounts...")

        self._write_csv('accounts', self.accounts)
        print(f"  ✅ Generated {len(self.accounts)} accounts")

    def generate_loans(self):
        """Generate loans with realistic amounts and education loan bias."""
        print("📊 Generating loans...")
        row_count = self.schema['tables']['loans']['row_count']

        dist = self.schema['tables']['loans']['columns']['loan_type']['distribution']
        status_dist = self.schema['tables']['loans']['columns']['loan_status']['distribution']

        # Loan amount ranges by type
        loan_ranges = {
            'personal': (1000, 50000, 15000),  # (min, max, mean)
            'auto': (10000, 60000, 28000),
            'mortgage': (100000, 750000, 285000),
            'business': (25000, 500000, 150000),
            'education': (5000, 200000, 81613),  # As specified
        }

        # Loan terms (months) by type
        loan_terms = {
            'personal': [12, 24, 36, 48, 60],
            'auto': [36, 48, 60, 72],
            'mortgage': [180, 240, 360],  # 15, 20, 30 years
            'business': [36, 60, 84, 120],
            'education': [120, 180, 240],  # 10, 15, 20 years
        }

        for i in range(row_count):
            customer = random.choice(self.customers)

            # Loan type
            loan_type = random.choices(
                list(dist.keys()),
                weights=list(dist.values())
            )[0]

            # Principal amount - education loans biased higher
            min_amt, max_amt, mean_amt = loan_ranges[loan_type]
            if loan_type == 'education':
                # Use lognormal with higher std for bias towards higher amounts
                principal = self._lognormal_amount(mean_amt, mean_amt * 0.8, min_amt, max_amt)
            else:
                principal = self._lognormal_amount(mean_amt, mean_amt * 0.5, min_amt, max_amt)

            # Interest rate by loan type
            if loan_type == 'mortgage':
                interest_rate = round(random.uniform(0.0325, 0.0725), 4)
            elif loan_type == 'auto':
                interest_rate = round(random.uniform(0.0399, 0.0899), 4)
            elif loan_type == 'education':
                interest_rate = round(random.uniform(0.0450, 0.0750), 4)
            elif loan_type == 'business':
                interest_rate = round(random.uniform(0.0550, 0.1200), 4)
            else:  # personal
                interest_rate = round(random.uniform(0.0699, 0.1599), 4)

            # Loan term
            term_months = random.choice(loan_terms[loan_type])

            # Monthly payment calculation (simplified)
            monthly_rate = interest_rate / 12
            monthly_payment = round(principal * (monthly_rate * (1 + monthly_rate)**term_months) /
                                   ((1 + monthly_rate)**term_months - 1), 2)

            # Origination date
            origination = self._random_date(self.start_date, self.end_date - timedelta(days=30))
            maturity = origination + timedelta(days=term_months * 30)

            # Loan status
            status = random.choices(
                list(status_dist.keys()),
                weights=list(status_dist.values())
            )[0]

            # Outstanding balance depends on how long it's been active
            months_elapsed = (datetime.now() - origination).days / 30
            if status == 'paid_off':
                outstanding = 0.0
                last_payment = self._random_date(origination, min(datetime.now(), maturity))
            elif status == 'defaulted':
                # Defaulted loans have high outstanding balance
                outstanding = round(principal * random.uniform(0.70, 0.95), 2)
                last_payment = self._random_date(origination, datetime.now())
            else:  # active or restructured
                # Calculate realistic outstanding based on amortization
                payments_made = min(months_elapsed, term_months)
                # Simplified: assume some principal paid down
                paydown_pct = payments_made / term_months
                outstanding = round(principal * (1 - paydown_pct * 0.8), 2)  # 80% of expected paydown
                last_payment = origination + timedelta(days=int(payments_made) * 30) if payments_made > 0 else None

            loan = {
                'loan_id': str(uuid.uuid4()),
                'customer_id': customer['customer_id'],
                'loan_type': loan_type,
                'principal_amount': principal,
                'outstanding_balance': outstanding,
                'interest_rate': interest_rate,
                'loan_term_months': term_months,
                'monthly_payment': monthly_payment,
                'loan_status': status,
                'origination_date': origination.strftime('%Y-%m-%d'),
                'maturity_date': maturity.strftime('%Y-%m-%d'),
                'last_payment_date': last_payment.strftime('%Y-%m-%d') if last_payment else None,
            }

            self.loans.append(loan)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} loans...")

        self._write_csv('loans', self.loans)
        print(f"  ✅ Generated {len(self.loans)} loans")

    def generate_cards(self):
        """Generate debit and credit cards."""
        print("📊 Generating cards...")
        row_count = self.schema['tables']['cards']['row_count']

        type_dist = self.schema['tables']['cards']['columns']['card_type']['distribution']
        network_dist = self.schema['tables']['cards']['columns']['card_network']['distribution']
        status_dist = self.schema['tables']['cards']['columns']['status']['distribution']

        for i in range(row_count):
            customer = random.choice(self.customers)

            # Find an account for this customer (if available)
            customer_accounts = [a for a in self.accounts if a['customer_id'] == customer['customer_id']]
            account_id = random.choice(customer_accounts)['account_id'] if customer_accounts else None

            # Card type and network
            card_type = random.choices(list(type_dist.keys()), weights=list(type_dist.values()))[0]
            network = random.choices(list(network_dist.keys()), weights=list(network_dist.values()))[0]

            # Card number (realistic format)
            if network == 'Visa':
                prefix = '4'
            else:  # Mastercard
                prefix = random.choice(['51', '52', '53', '54', '55'])
            card_number = prefix + ''.join([str(random.randint(0, 9)) for _ in range(14)])

            # Expiration
            issued_at = self._random_date(self.start_date, self.end_date)
            exp_month = random.randint(1, 12)
            exp_year = issued_at.year + random.randint(2, 5)

            # CVV
            cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])

            # Credit limit for credit cards
            credit_limit = None
            if card_type == 'credit':
                credit_limit = round(random.choice([1000, 2500, 5000, 10000, 15000, 25000, 50000]), 2)

            # Status
            status = random.choices(list(status_dist.keys()), weights=list(status_dist.values()))[0]

            card = {
                'card_id': str(uuid.uuid4()),
                'customer_id': customer['customer_id'],
                'account_id': account_id,
                'card_number': card_number,
                'card_type': card_type,
                'card_network': network,
                'expiration_month': exp_month,
                'expiration_year': exp_year,
                'cvv': cvv,
                'credit_limit': credit_limit,
                'status': status,
                'issued_at': issued_at.strftime('%Y-%m-%d %H:%M:%S'),
            }

            self.cards.append(card)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} cards...")

        self._write_csv('cards', self.cards)
        print(f"  ✅ Generated {len(self.cards)} cards")

    def generate_card_transactions(self):
        """Generate card transactions with COHERENT merchant names matching countries."""
        print("📊 Generating card transactions...")
        row_count = self.schema['tables']['card_transactions']['row_count']

        entry_mode_dist = self.schema['tables']['card_transactions']['columns']['pos_entry_mode']['distribution']
        auth_dist = self.schema['tables']['card_transactions']['columns']['auth_response']['distribution']

        for i in range(row_count):
            card = random.choice(self.cards)

            # Determine if transaction is international (5%)
            is_international = random.random() < 0.05

            if is_international:
                country_code = random.choice(list(self.intl_countries.keys()))
                country_data = self.intl_countries[country_code]
                merchant_city = random.choice(country_data['cities'])
                currency = country_data['currency']
                # For international, use generic merchant names
                category = random.choice(list(self.merchant_categories.keys()))
                merchant_name = f"International {category.title()} - {merchant_city}"
            else:
                country_code = 'US'
                location = self.location_gen.generate_location()
                merchant_city = location['city']
                currency = 'USD'
                # COHERENT: Use real merchant names for US
                category = random.choice(list(self.merchant_categories.keys()))
                merchant_name = random.choice(self.merchant_categories[category])

            # Merchant category name
            merchant_category = category

            # Transaction amount based on category
            if category == 'gas_stations':
                amount = round(random.uniform(25, 85), 2)
            elif category == 'grocery':
                amount = round(random.uniform(15, 250), 2)
            elif category == 'restaurants':
                amount = round(random.uniform(12, 180), 2)
            elif category == 'retail':
                amount = round(random.uniform(20, 500), 2)
            elif category == 'online':
                amount = round(random.uniform(10, 350), 2)
            else:  # entertainment
                amount = round(random.uniform(8, 120), 2)

            # Billing amount (same as transaction for USD, with exchange rate for others)
            if currency != 'USD':
                # Simplified exchange rate
                exchange_rates = {'GBP': 1.27, 'CAD': 0.74, 'MXN': 0.058, 'EUR': 1.10,
                                 'JPY': 0.0067, 'AUD': 0.65, 'INR': 0.012}
                billing_amount = round(amount * exchange_rates.get(currency, 1.0), 2)
            else:
                billing_amount = amount

            # POS entry mode
            entry_mode = random.choices(list(entry_mode_dist.keys()), weights=list(entry_mode_dist.values()))[0]

            # Auth response
            auth_response = random.choices(list(auth_dist.keys()), weights=list(auth_dist.values()))[0]

            # Decline reason only if declined
            decline_reason = None
            if auth_response == 'declined':
                decline_reason = random.choice([
                    'Insufficient funds',
                    'Card expired',
                    'Suspected fraud',
                    'Invalid CVV',
                    'Exceeds credit limit',
                    'Card reported lost/stolen',
                ])

            # Transaction date
            tx_date = self._random_date(self.start_date, self.end_date)

            transaction = {
                'transaction_id': str(uuid.uuid4()),
                'card_id': card['card_id'],
                'merchant_name': merchant_name,
                'merchant_category': merchant_category,
                'merchant_city': merchant_city,
                'merchant_country': country_code,
                'transaction_amount': amount,
                'transaction_currency': currency,
                'billing_amount': billing_amount,
                'pos_entry_mode': entry_mode,
                'auth_response': auth_response,
                'decline_reason': decline_reason,
                'transaction_date': tx_date.strftime('%Y-%m-%d %H:%M:%S'),
            }

            self.card_transactions.append(transaction)

            if (i + 1) % 10000 == 0:
                print(f"  Generated {i + 1}/{row_count} transactions...")

        self._write_csv('card_transactions', self.card_transactions)
        print(f"  ✅ Generated {len(self.card_transactions)} card transactions")

    def generate_wire_transfers(self):
        """Generate wire transfers with realistic amounts and COHERENT beneficiary names."""
        print("📊 Generating wire transfers...")
        row_count = self.schema['tables']['wire_transfers']['row_count']

        type_dist = self.schema['tables']['wire_transfers']['columns']['transfer_type']['distribution']
        status_dist = self.schema['tables']['wire_transfers']['columns']['transfer_status']['distribution']

        for i in range(row_count):
            account = random.choice(self.accounts)

            # Transfer type
            transfer_type = random.choices(list(type_dist.keys()), weights=list(type_dist.values()))[0]

            # Beneficiary country
            if transfer_type == 'domestic':
                beneficiary_country = 'US'
                currency = 'USD'
                exchange_rate = None
                swift_code = None
                # Domestic beneficiary name
                first, last = self.name_gen.generate_unique_name()
                beneficiary_name = f"{first} {last}"
                beneficiary_bank = random.choice(['Bank of America', 'Wells Fargo', 'Chase Bank', 'Citibank',
                                                 'US Bank', 'PNC Bank', 'Capital One'])
            else:  # international
                beneficiary_country = random.choice(list(self.intl_countries.keys()))
                country_data = self.intl_countries[beneficiary_country]
                currency = country_data['currency']
                # International beneficiary (use generic name for now)
                first, last = self.name_gen.generate_unique_name()
                beneficiary_name = f"{first} {last}"
                beneficiary_bank = f"{country_data['name']} National Bank"
                # Exchange rate
                rates = {'GBP': 1.27, 'CAD': 0.74, 'MXN': 0.058, 'EUR': 1.10,
                        'JPY': 0.0067, 'AUD': 0.65, 'INR': 0.012}
                exchange_rate = round(1.0 / rates.get(currency, 1.0), 6)
                # SWIFT code
                swift_code = f"{beneficiary_country}{random.randint(10, 99)}XXX"

            # Transfer amount - average $16,913 with lognormal distribution
            amount = self._lognormal_amount(16913, 28000, 100, 500000)

            # Transfer fee
            if transfer_type == 'domestic':
                fee = round(random.uniform(0, 25), 2)
            else:
                fee = round(random.uniform(25, 50), 2)

            # Beneficiary account
            beneficiary_account = f"{random.randint(100000000, 999999999)}"

            # Transfer purpose
            purposes = ['Family support', 'Business payment', 'Investment', 'Property purchase',
                       'Education', 'Savings transfer', 'Loan repayment', 'Services payment']
            transfer_purpose = random.choice(purposes)

            # Status
            status = random.choices(list(status_dist.keys()), weights=list(status_dist.values()))[0]

            # Initiated and completed timestamps
            initiated = self._random_date(self.start_date, self.end_date)
            completed = None
            if status == 'completed':
                # Domestic: 30 min to 1 day, International: 1-3 days
                if transfer_type == 'domestic':
                    completed = initiated + timedelta(seconds=random.randint(1800, 86400))
                else:
                    completed = initiated + timedelta(seconds=random.randint(86400, 259200))
            elif status == 'processing':
                # In progress
                completed = None
            elif status in ('failed', 'cancelled'):
                # Failed/cancelled within a few hours
                completed = initiated + timedelta(seconds=random.randint(3600, 21600))

            wire = {
                'transfer_id': str(uuid.uuid4()),
                'from_account_id': account['account_id'],
                'transfer_type': transfer_type,
                'beneficiary_name': beneficiary_name,
                'beneficiary_account': beneficiary_account,
                'beneficiary_bank': beneficiary_bank,
                'beneficiary_country': beneficiary_country,
                'transfer_amount': amount,
                'transfer_currency': currency,
                'exchange_rate': exchange_rate,
                'transfer_fee': fee,
                'swift_code': swift_code,
                'transfer_purpose': transfer_purpose,
                'transfer_status': status,
                'initiated_at': initiated.strftime('%Y-%m-%d %H:%M:%S'),
                'completed_at': completed.strftime('%Y-%m-%d %H:%M:%S') if completed else None,
            }

            self.wire_transfers.append(wire)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} wire transfers...")

        self._write_csv('wire_transfers', self.wire_transfers)
        print(f"  ✅ Generated {len(self.wire_transfers)} wire transfers")

    def generate_bill_payments(self):
        """Generate bill payments with coherent biller names."""
        print("📊 Generating bill payments...")
        row_count = self.schema['tables']['bill_payments']['row_count']

        type_dist = self.schema['tables']['bill_payments']['columns']['bill_type']['distribution']
        method_dist = self.schema['tables']['bill_payments']['columns']['payment_method']['distribution']
        status_dist = self.schema['tables']['bill_payments']['columns']['payment_status']['distribution']

        for i in range(row_count):
            account = random.choice(self.accounts)

            # Bill type
            bill_type = random.choices(list(type_dist.keys()), weights=list(type_dist.values()))[0]

            # Biller name - COHERENT with bill type
            biller_name = random.choice(self.billers[bill_type])

            # Account number
            bill_account_number = f"{random.randint(1000000000, 9999999999)}"

            # Payment amount by type
            amount_ranges = {
                'electricity': (50, 350),
                'water': (30, 150),
                'telecom': (60, 180),
                'internet': (50, 120),
                'insurance': (100, 400),
                'education': (500, 5000),
                'government': (50, 1500),
            }
            min_amt, max_amt = amount_ranges[bill_type]
            amount = round(random.uniform(min_amt, max_amt), 2)

            # Payment method and status
            method = random.choices(list(method_dist.keys()), weights=list(method_dist.values()))[0]
            status = random.choices(list(status_dist.keys()), weights=list(status_dist.values()))[0]

            # Scheduled and payment dates
            payment_date = self._random_date(self.start_date, self.end_date)
            # Scheduled date is usually a few days before payment
            scheduled_date = (payment_date - timedelta(days=random.randint(0, 5))).strftime('%Y-%m-%d')

            bill_payment = {
                'payment_id': str(uuid.uuid4()),
                'account_id': account['account_id'],
                'biller_name': biller_name,
                'bill_type': bill_type,
                'account_number': bill_account_number,
                'payment_amount': amount,
                'payment_currency': 'USD',
                'payment_method': method,
                'payment_status': status,
                'scheduled_date': scheduled_date,
                'payment_date': payment_date.strftime('%Y-%m-%d %H:%M:%S'),
            }

            self.bill_payments.append(bill_payment)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} bill payments...")

        self._write_csv('bill_payments', self.bill_payments)
        print(f"  ✅ Generated {len(self.bill_payments)} bill payments")

    def generate_wealth_management_accounts(self):
        """Generate wealth management accounts with high average value."""
        print("📊 Generating wealth management accounts...")
        row_count = self.schema['tables']['wealth_management_accounts']['row_count']

        type_dist = self.schema['tables']['wealth_management_accounts']['columns']['portfolio_type']['distribution']

        for i in range(row_count):
            customer = random.choice(self.customers)

            # Portfolio type
            portfolio_type = random.choices(list(type_dist.keys()), weights=list(type_dist.values()))[0]

            # Portfolio name
            portfolio_name = f"{customer['first_name']} {customer['last_name']} {portfolio_type.title()} Portfolio"

            # Total value - average $367,420 with bias towards higher amounts
            total_value = self._lognormal_amount(367420, 450000, 10000, 5000000)

            # Risk profile based on portfolio type
            risk_mapping = {
                'conservative': 'low',
                'balanced': 'medium',
                'income': 'low',
                'growth': 'medium',
                'aggressive': 'high',
            }
            risk_profile = risk_mapping[portfolio_type]

            # Management fee (0.25% - 1.50%)
            fee_pct = round(random.uniform(0.0025, 0.0150), 4)

            # Advisor ID
            advisor_id = str(uuid.uuid4())

            # Opened date
            opened_at = self._random_date(self.start_date, self.end_date)

            # Last reviewed (quarterly reviews)
            months_since_open = (datetime.now() - opened_at).days / 30
            if months_since_open > 3:
                last_reviewed = opened_at + timedelta(days=int(random.randint(1, int(months_since_open/3)) * 90))
            else:
                last_reviewed = None

            portfolio = {
                'portfolio_id': str(uuid.uuid4()),
                'customer_id': customer['customer_id'],
                'portfolio_name': portfolio_name,
                'portfolio_type': portfolio_type,
                'total_value': total_value,
                'currency': 'USD',
                'risk_profile': risk_profile,
                'management_fee_pct': fee_pct,
                'advisor_id': advisor_id,
                'opened_at': opened_at.strftime('%Y-%m-%d %H:%M:%S'),
                'last_reviewed_at': last_reviewed.strftime('%Y-%m-%d %H:%M:%S') if last_reviewed else None,
            }

            self.wealth_portfolios.append(portfolio)

            if (i + 1) % 100 == 0:
                print(f"  Generated {i + 1}/{row_count} portfolios...")

        self._write_csv('wealth_management_accounts', self.wealth_portfolios)
        print(f"  ✅ Generated {len(self.wealth_portfolios)} wealth management accounts")

    def generate_investment_transactions(self):
        """Generate investment transactions with coherent security names."""
        print("📊 Generating investment transactions...")
        row_count = self.schema['tables']['investment_transactions']['row_count']

        tx_type_dist = self.schema['tables']['investment_transactions']['columns']['transaction_type']['distribution']
        security_type_dist = self.schema['tables']['investment_transactions']['columns']['security_type']['distribution']
        status_dist = self.schema['tables']['investment_transactions']['columns']['settlement_status']['distribution']

        for i in range(row_count):
            portfolio = random.choice(self.wealth_portfolios)

            # Transaction type and security type
            tx_type = random.choices(list(tx_type_dist.keys()), weights=list(tx_type_dist.values()))[0]
            security_type = random.choices(list(security_type_dist.keys()), weights=list(security_type_dist.values()))[0]

            # Security name - COHERENT with security type
            security_name = random.choice(self.securities[security_type])

            # Quantity and price (depends on transaction type)
            if tx_type in ('buy', 'sell'):
                if security_type == 'stock':
                    quantity = round(random.uniform(1, 500), 4)
                    price_per_unit = round(random.uniform(10, 500), 4)
                elif security_type == 'bond':
                    quantity = round(random.uniform(1, 100), 4)
                    price_per_unit = round(random.uniform(95, 105), 4)  # Bonds trade near par
                elif security_type in ('mutual_fund', 'etf'):
                    quantity = round(random.uniform(1, 1000), 4)
                    price_per_unit = round(random.uniform(20, 300), 4)
                else:  # real_estate
                    quantity = round(random.uniform(1, 50), 4)
                    price_per_unit = round(random.uniform(1000, 50000), 4)

                transaction_amount = round(quantity * price_per_unit, 2)
            else:  # dividend, interest, fee
                quantity = None
                price_per_unit = None
                transaction_amount = round(random.uniform(50, 5000), 2)

            # Transaction fee
            if tx_type in ('buy', 'sell'):
                fee = round(transaction_amount * random.uniform(0.001, 0.01), 2)
            else:
                fee = 0.0

            # Settlement status
            status = random.choices(list(status_dist.keys()), weights=list(status_dist.values()))[0]

            # Transaction and settlement dates (T+1 to T+3)
            tx_date = self._random_date(self.start_date, self.end_date)
            settlement_date = None
            if status == 'settled':
                settlement_date = tx_date + timedelta(days=random.randint(1, 3))

            inv_tx = {
                'investment_tx_id': str(uuid.uuid4()),
                'portfolio_id': portfolio['portfolio_id'],
                'transaction_type': tx_type,
                'security_name': security_name,
                'security_type': security_type,
                'quantity': quantity,
                'price_per_unit': price_per_unit,
                'transaction_amount': transaction_amount,
                'transaction_fee': fee,
                'transaction_currency': 'USD',
                'settlement_status': status,
                'transaction_date': tx_date.strftime('%Y-%m-%d %H:%M:%S'),
                'settlement_date': settlement_date.strftime('%Y-%m-%d %H:%M:%S') if settlement_date else None,
            }

            self.investment_transactions.append(inv_tx)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} investment transactions...")

        self._write_csv('investment_transactions', self.investment_transactions)
        print(f"  ✅ Generated {len(self.investment_transactions)} investment transactions")

    def generate_atm_transactions(self):
        """Generate ATM transactions."""
        print("📊 Generating ATM transactions...")
        row_count = self.schema['tables']['atm_transactions']['row_count']

        tx_type_dist = self.schema['tables']['atm_transactions']['columns']['transaction_type']['distribution']
        network_dist = self.schema['tables']['atm_transactions']['columns']['atm_network']['distribution']
        status_dist = self.schema['tables']['atm_transactions']['columns']['transaction_status']['distribution']

        for i in range(row_count):
            account = random.choice(self.accounts)

            # Find a card for this account
            account_cards = [c for c in self.cards if c['account_id'] == account['account_id']]
            card = random.choice(account_cards) if account_cards else None

            # ATM location
            location = self.location_gen.generate_location()
            atm_location = f"{location['city']}, {location['state']}"
            atm_id = f"ATM-{random.randint(10000, 99999)}"

            # Transaction type
            tx_type = random.choices(list(tx_type_dist.keys()), weights=list(tx_type_dist.values()))[0]

            # Amount (null for balance inquiry)
            if tx_type == 'balance_inquiry':
                amount = None
            elif tx_type == 'withdrawal':
                # Common withdrawal amounts
                amount = random.choice([20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 300, 400, 500])
            elif tx_type == 'deposit':
                amount = round(random.uniform(20, 1000), 2)
            else:  # transfer
                amount = round(random.uniform(50, 500), 2)

            # ATM network and fee
            network = random.choices(list(network_dist.keys()), weights=list(network_dist.values()))[0]
            if network == 'liberty_national':
                fee = 0.0
            elif network == 'partner_bank':
                fee = round(random.uniform(2.50, 3.50), 2)
            else:  # international
                fee = round(random.uniform(3.50, 5.00), 2)

            # Status
            status = random.choices(list(status_dist.keys()), weights=list(status_dist.values()))[0]

            # Transaction date
            tx_date = self._random_date(self.start_date, self.end_date)

            atm_tx = {
                'atm_tx_id': str(uuid.uuid4()),
                'account_id': account['account_id'],
                'card_id': card['card_id'] if card else None,
                'atm_id': atm_id,
                'atm_location': atm_location,
                'transaction_type': tx_type,
                'amount': amount,
                'transaction_fee': fee,
                'atm_network': network,
                'transaction_status': status,
                'transaction_date': tx_date.strftime('%Y-%m-%d %H:%M:%S'),
            }

            self.atm_transactions.append(atm_tx)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} ATM transactions...")

        self._write_csv('atm_transactions', self.atm_transactions)
        print(f"  ✅ Generated {len(self.atm_transactions)} ATM transactions")

    def generate_loan_payments(self):
        """Generate loan payment transactions."""
        print("📊 Generating loan payments...")
        row_count = self.schema['tables']['loan_payments']['row_count']

        status_dist = self.schema['tables']['loan_payments']['columns']['payment_status']['distribution']
        method_dist = self.schema['tables']['loan_payments']['columns']['payment_method']['distribution']

        for i in range(row_count):
            loan = random.choice(self.loans)

            # Find an account for the loan's customer
            loan_customer_accounts = [a for a in self.accounts if a['customer_id'] == loan['customer_id']]
            account = random.choice(loan_customer_accounts) if loan_customer_accounts else random.choice(self.accounts)

            # Payment amount (usually the monthly payment, but can vary)
            base_payment = loan['monthly_payment']
            payment_status = random.choices(list(status_dist.keys()), weights=list(status_dist.values()))[0]

            if payment_status == 'partial':
                payment_amount = round(base_payment * random.uniform(0.3, 0.8), 2)
            elif payment_status == 'missed':
                payment_amount = 0.0
            else:
                payment_amount = round(base_payment * random.uniform(0.98, 1.02), 2)  # Slight variation

            # Principal and interest split (simplified)
            interest_paid = round(payment_amount * loan['interest_rate'] / 12, 2)
            principal_paid = round(payment_amount - interest_paid, 2)

            # Late fee
            if payment_status == 'late':
                late_fee = round(random.uniform(25, 50), 2)
            else:
                late_fee = 0.0

            # Payment method
            method = random.choices(list(method_dist.keys()), weights=list(method_dist.values()))[0]

            # Payment and due dates
            origination = datetime.strptime(loan['origination_date'], '%Y-%m-%d')
            months_offset = random.randint(0, loan['loan_term_months'])
            due_date = origination + timedelta(days=months_offset * 30)

            # Payment date relative to due date
            if payment_status == 'on_time':
                payment_date = due_date + timedelta(days=random.randint(-3, 1))
            elif payment_status == 'late':
                payment_date = due_date + timedelta(days=random.randint(1, 30))
            else:
                payment_date = due_date + timedelta(days=random.randint(-5, 35))

            loan_payment = {
                'payment_id': str(uuid.uuid4()),
                'loan_id': loan['loan_id'],
                'account_id': account['account_id'],
                'payment_amount': payment_amount,
                'principal_paid': principal_paid,
                'interest_paid': interest_paid,
                'late_fee': late_fee,
                'payment_status': payment_status,
                'payment_method': method,
                'payment_date': payment_date.strftime('%Y-%m-%d %H:%M:%S'),
                'due_date': due_date.strftime('%Y-%m-%d'),
            }

            self.loan_payments.append(loan_payment)

            if (i + 1) % 1000 == 0:
                print(f"  Generated {i + 1}/{row_count} loan payments...")

        self._write_csv('loan_payments', self.loan_payments)
        print(f"  ✅ Generated {len(self.loan_payments)} loan payments")

    def _write_csv(self, table_name: str, data: List[Dict]):
        """Write data to CSV file."""
        if not data:
            return

        file_path = self.output_dir / f"{table_name}.csv"
        columns = list(data[0].keys())

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)

    def generate_all(self):
        """Generate all tables in dependency order."""
        print("🚀 Starting coherent banking data generation...")

        # Initialize storage
        self.card_transactions = []
        self.wire_transfers = []
        self.bill_payments = []
        self.investment_transactions = []
        self.atm_transactions = []
        self.loan_payments = []

        # Generate in dependency order
        self.generate_customers()
        self.generate_accounts()
        self.generate_loans()
        self.generate_cards()
        self.generate_wealth_management_accounts()

        # Transactions (depend on above)
        self.generate_card_transactions()
        self.generate_wire_transfers()
        self.generate_bill_payments()
        self.generate_investment_transactions()
        self.generate_atm_transactions()
        self.generate_loan_payments()

        print("\n✅ All data generation complete!")
        print(f"📁 Output files written to: {self.output_dir}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python generate_coherent_banking_data.py <schema.json> <output_dir>")
        sys.exit(1)

    schema_path = sys.argv[1]
    output_dir = sys.argv[2]

    generator = CoherentBankingDataGenerator(schema_path, output_dir)
    generator.generate_all()
