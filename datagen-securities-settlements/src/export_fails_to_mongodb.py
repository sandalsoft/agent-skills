#!/usr/bin/env python3
"""
Export settlement fails data to MongoDB JSON format.

Reads PostgreSQL CSV files for settlement fails and transforms them into
MongoDB documents matching the fails_db schema.
"""

import csv
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
import argparse
from typing import List, Dict, Any


class FailsMongoDBExporter:
    """Exports settlement fails to MongoDB JSON format."""

    def __init__(self, csv_dir: Path, output_dir: Path):
        self.csv_dir = Path(csv_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Storage for MongoDB documents
        self.fails_docs = []
        self.statistics_docs = {}

        # Load reference data
        self.trades = {}
        self.securities = {}
        self.settlements = {}

    def load_reference_data(self):
        """Load reference data from CSV files."""
        print("📖 Loading reference data...")

        # Load trades
        with open(self.csv_dir / 'trades.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.trades[row['trade_id']] = row

        # Load securities
        with open(self.csv_dir / 'securities.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.securities[row['security_id']] = row

        # Load settlements
        with open(self.csv_dir / 'settlements.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.settlements[row['settlement_id']] = row

        print(f"  ✓ Loaded {len(self.trades)} trades")
        print(f"  ✓ Loaded {len(self.securities)} securities")
        print(f"  ✓ Loaded {len(self.settlements)} settlements")

    def transform_fail_to_mongodb(self, fail_row: Dict, charges: List[Dict]) -> Dict:
        """Transform a fail CSV row to MongoDB document format."""

        # Get related data
        settlement = self.settlements.get(fail_row['settlement_id'], {})
        trade = self.trades.get(fail_row['trade_id'], {})
        security = self.securities.get(trade.get('security_id', ''), {})

        # Map fail category to exceptions
        exceptions = self._create_exceptions_from_fail(fail_row)

        # Determine settlement system and region from market
        market = security.get('market', 'US')
        settlement_system, settlement_region = self._get_settlement_location(market)

        # Map settlement location to market clearinghouse
        settlement_location = settlement.get('settlement_location', 'DTC')

        # Determine fail type based on age
        fail_age = int(fail_row['fail_age_days'])
        if fail_age <= 3:
            fail_type = "PENDING"
        elif fail_age <= 20:
            fail_type = "AGED"
        else:
            fail_type = "CHRONIC"

        # Map fail status
        fail_status_map = {
            'active': 'OPEN',
            'resolved': 'RESOLVED',
            'buy_in_initiated': 'BUY_IN_INITIATED',
            'closed_out': 'CLOSED_OUT',
            'disputed': 'OPEN'
        }
        fail_status = fail_status_map.get(fail_row['fail_status'], 'OPEN')

        # Map trade status
        trade_status_map = {
            'executed': 'OPEN',
            'confirmed': 'OPEN',
            'allocated': 'OPEN',
            'cancelled': 'CANCELLED'
        }
        trade_status = trade_status_map.get(trade.get('trade_status', 'confirmed'), 'OPEN')

        # Determine trade product
        trade_side = trade.get('trade_side', 'buy')
        trade_product = "Receivesecurities" if trade_side == "buy" else "Deliversecurities"

        # Calculate total charges
        total_charges = sum(float(c['charge_amount']) for c in charges)

        # Create MongoDB document
        doc = {
            "id": uuid.uuid4().hex[:24],  # 24-char hex string
            "last_update_time": datetime.now(timezone.utc).isoformat(),
            "expiration_time": "9999-01-31T00:00:00Z",
            "aggregate_id": fail_row['fail_reference'][:9],  # Use first 9 chars of reference
            "state": {
                "trade_id": fail_row['trade_id'],
                "trade_reference": trade.get('trade_reference', ''),
                "trade_date": trade.get('trade_date', ''),
                "trade_product": trade_product,
                "trade_status": trade_status,
                "trade_event_type": "OPENED",
                "settlement_system": settlement_system,
                "settlement_region": settlement_region,
                "primary_product_type": "SECURITY",
                "market": settlement_location,
                "fail_id": fail_row['fail_id'],
                "fail_type": fail_type,
                "fail_status": fail_status,
                "fail_assessment": None,
                "fail_category": fail_row['fail_category'],
                "fail_reason": fail_row['fail_reason'],
                "failing_party": fail_row['failing_party'],
                "fail_quantity": int(fail_row['fail_quantity']),
                "fail_value": float(fail_row['fail_value']),
                "fail_start_date": fail_row['fail_start_date'],
                "fail_age_days": fail_age,
                "resolution_method": fail_row.get('resolution_method'),
                "resolution_date": fail_row.get('resolution_date'),
                "buy_in_date": fail_row.get('buy_in_date'),
                "regulatory_threshold_breach": fail_row['regulatory_threshold_breach'].lower() == 'true',
                "total_charges": total_charges,
                "expiration_time": "9999-01-31T00:00:00Z",
                "exceptions": exceptions
            }
        }

        return doc

    def _create_exceptions_from_fail(self, fail_row: Dict) -> List[Dict]:
        """Create exception records from fail data."""
        exceptions = []

        # Always add a FAI (Fail) exception
        exceptions.append({
            "actionable": True,
            "exception_type": None,
            "exception_status": "UNRESOLVED" if fail_row['fail_status'] in ['active', 'buy_in_initiated'] else "RESOLVED",
            "exception_reason": fail_row['fail_reason'],
            "exception_user_id": None,
            "legacy_exception_type": "FAI"
        })

        # Add OMN (Operations Manual) exception for operational fails
        if fail_row['fail_category'] == 'operational':
            exceptions.append({
                "actionable": True,
                "exception_type": None,
                "exception_status": "UNRESOLVED" if fail_row['fail_status'] == 'active' else "RESOLVED",
                "exception_reason": fail_row['fail_reason'],
                "exception_user_id": "MBSQA",  # Operations queue
                "legacy_exception_type": "OMN"
            })

        return exceptions

    def _get_settlement_location(self, market: str) -> tuple:
        """Get settlement system and region from market."""
        location_map = {
            'US': ('NY', 'NORTH_AMERICA'),
            'JP': ('TOKYO', 'ASIA_PACIFIC'),
            'EU': ('LONDON', 'EUROPE')
        }
        return location_map.get(market, ('NY', 'NORTH_AMERICA'))

    def create_statistics_doc(self, cusip: str, counter_party: str, market: str) -> str:
        """Create or update a statistics document."""
        key = f"{cusip}_{counter_party}_{market}"

        if key not in self.statistics_docs:
            self.statistics_docs[key] = {
                "id": uuid.uuid4().hex[:24],
                "cusip": cusip,
                "counter_party_account_number": counter_party,
                "type": "MS_ACTION",
                "market": market,
                "settlement_category": None,
                "fail_count": 0,
                "total_fail_value": 0.0,
                "avg_fail_age_days": 0.0,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }

        return key

    def export_to_mongodb(self):
        """Export fails and statistics to MongoDB JSON format."""
        print("\n🔄 Transforming fails data to MongoDB format...")

        # Check if fail files exist
        settlement_fails_csv = self.csv_dir / 'settlement_fails.csv'
        fail_charges_csv = self.csv_dir / 'fail_charges.csv'

        if not settlement_fails_csv.exists():
            print(f"⚠️  No settlement_fails.csv found in {self.csv_dir}")
            print("   Skipping MongoDB export")
            return

        # Load fails
        fails = []
        with open(settlement_fails_csv, 'r') as f:
            reader = csv.DictReader(f)
            fails = list(reader)

        # Load charges
        charges_by_fail = {}
        if fail_charges_csv.exists():
            with open(fail_charges_csv, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    fail_id = row['fail_id']
                    if fail_id not in charges_by_fail:
                        charges_by_fail[fail_id] = []
                    charges_by_fail[fail_id].append(row)

        # Transform each fail
        for fail_row in fails:
            fail_id = fail_row['fail_id']
            charges = charges_by_fail.get(fail_id, [])

            # Create MongoDB document
            mongo_doc = self.transform_fail_to_mongodb(fail_row, charges)
            self.fails_docs.append(mongo_doc)

            # Update statistics
            trade = self.trades.get(fail_row['trade_id'], {})
            security = self.securities.get(trade.get('security_id', ''), {})
            cusip = security.get('cusip') or security.get('isin', '')[:9]  # Use first 9 chars of ISIN if no CUSIP
            counter_party_account = trade.get('counterparty_broker_id', '')[:9]  # Simplified account number
            market = mongo_doc['state']['market']

            stat_key = self.create_statistics_doc(cusip, counter_party_account, market)

            # Update statistics
            stat = self.statistics_docs[stat_key]
            stat['fail_count'] += 1
            stat['total_fail_value'] += float(fail_row['fail_value'])

        # Calculate average fail age for statistics
        for stat in self.statistics_docs.values():
            if stat['fail_count'] > 0:
                # Recalculate average
                related_fails = [f for f in self.fails_docs
                               if f['state']['market'] == stat['market']]
                if related_fails:
                    stat['avg_fail_age_days'] = sum(f['state']['fail_age_days'] for f in related_fails) / len(related_fails)

        print(f"  ✓ Transformed {len(self.fails_docs)} fail documents")
        print(f"  ✓ Created {len(self.statistics_docs)} statistics documents")

        # Write MongoDB JSON files
        self._write_mongodb_files()

    def _write_mongodb_files(self):
        """Write MongoDB JSON files."""
        print("\n📝 Writing MongoDB JSON files...")

        # Create fails_db directory
        fails_db_dir = self.output_dir / 'fails_db'
        fails_db_dir.mkdir(parents=True, exist_ok=True)

        # Write Fails collection
        fails_file = fails_db_dir / 'Fails.json'
        with open(fails_file, 'w') as f:
            json.dump(self.fails_docs, f, indent=2, default=str)
        print(f"  ✓ fails_db/Fails.json ({len(self.fails_docs)} documents)")

        # Write Statistics collection
        statistics_file = fails_db_dir / 'Statistics.json'
        statistics_list = list(self.statistics_docs.values())
        with open(statistics_file, 'w') as f:
            json.dump(statistics_list, f, indent=2, default=str)
        print(f"  ✓ fails_db/Statistics.json ({len(statistics_list)} documents)")

        print(f"\n✅ MongoDB files written to {fails_db_dir}/")

    def run(self):
        """Execute the export process."""
        self.load_reference_data()
        self.export_to_mongodb()


def main():
    parser = argparse.ArgumentParser(
        description='Export settlement fails to MongoDB JSON format'
    )
    parser.add_argument('csv_dir', help='Directory containing CSV files')
    parser.add_argument('output_dir', help='Output directory for MongoDB JSON files')

    args = parser.parse_args()

    exporter = FailsMongoDBExporter(args.csv_dir, args.output_dir)
    exporter.run()

    print("\n🎉 Export complete!")
    print("\nNext steps:")
    print(f"  1. Review MongoDB JSON files in {args.output_dir}/fails_db/")
    print("  2. Import to MongoDB:")
    print(f"     mongoimport --db fails_db --collection Fails --file {args.output_dir}/fails_db/Fails.json --jsonArray")
    print(f"     mongoimport --db fails_db --collection Statistics --file {args.output_dir}/fails_db/Statistics.json --jsonArray")


if __name__ == '__main__':
    main()
