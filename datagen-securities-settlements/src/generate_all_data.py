#!/usr/bin/env python3
"""
Master data generation script for hybrid PostgreSQL + MongoDB settlement data.

This script orchestrates the complete data generation process:
1. Generate PostgreSQL data (core settlement tables)
2. Export fails data to MongoDB JSON format
3. Output all data to ./data directory
"""

import sys
import argparse
import subprocess
from pathlib import Path


def run_command(cmd: list, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print(f"✅ {description} - Complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Generate hybrid PostgreSQL + MongoDB settlement data'
    )
    parser.add_argument(
        '--postgres-schema',
        default='assets/settlements_postgres_schema.json',
        help='PostgreSQL schema JSON file'
    )
    parser.add_argument(
        '--output-dir',
        default='./data',
        help='Output directory for all generated data'
    )
    parser.add_argument(
        '--fail-rate',
        type=float,
        default=0.15,
        help='Target settlement fail rate (default: 0.15)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed for reproducibility'
    )

    args = parser.parse_args()

    # Get script directory
    script_dir = Path(__file__).parent

    # Create output directories
    output_dir = Path(args.output_dir)
    postgres_dir = output_dir / 'postgres'
    mongodb_dir = output_dir / 'mongodb'

    print("🚀 Securities Settlement Data Generator (Hybrid PostgreSQL + MongoDB)")
    print(f"\n📂 Output directory: {output_dir.absolute()}")
    print(f"   - PostgreSQL CSV: {postgres_dir}")
    print(f"   - MongoDB JSON: {mongodb_dir}")
    print(f"\n⚙️  Configuration:")
    print(f"   - Schema: {args.postgres_schema}")
    print(f"   - Fail rate: {args.fail_rate * 100:.1f}%")
    if args.seed:
        print(f"   - Random seed: {args.seed}")

    # Step 1: Generate PostgreSQL data
    print("\n" + "="*60)
    print("STEP 1: Generate PostgreSQL Data (Core Settlement Tables)")
    print("="*60)

    pg_cmd = [
        sys.executable,
        str(script_dir / 'generate_securities_data.py'),
        args.postgres_schema,
        str(postgres_dir),
        '--fail-rate', str(args.fail_rate)
    ]

    if args.seed:
        pg_cmd.extend(['--seed', str(args.seed)])

    if not run_command(pg_cmd, "PostgreSQL data generation"):
        print("\n❌ PostgreSQL data generation failed. Stopping.")
        sys.exit(1)

    # Step 2: Export fails to MongoDB
    print("\n" + "="*60)
    print("STEP 2: Export Fails to MongoDB JSON")
    print("="*60)

    mongo_cmd = [
        sys.executable,
        str(script_dir / 'export_fails_to_mongodb.py'),
        str(postgres_dir),
        str(mongodb_dir)
    ]

    if not run_command(mongo_cmd, "MongoDB export"):
        print("\n⚠️  MongoDB export failed, but PostgreSQL data was generated successfully.")
        print("   You can manually run the export later if needed.")

    # Summary
    print("\n" + "="*60)
    print("✅ DATA GENERATION COMPLETE")
    print("="*60)

    print(f"\n📊 Generated Files:")
    print(f"\n PostgreSQL CSV files (./data/postgres/):")
    if postgres_dir.exists():
        for csv_file in sorted(postgres_dir.glob('*.csv')):
            size = csv_file.stat().st_size / 1024  # KB
            print(f"   ✓ {csv_file.name} ({size:.1f} KB)")

    print(f"\n📦 MongoDB JSON files (./data/mongodb/fails_db/):")
    mongodb_fails_dir = mongodb_dir / 'fails_db'
    if mongodb_fails_dir.exists():
        for json_file in sorted(mongodb_fails_dir.glob('*.json')):
            size = json_file.stat().st_size / 1024  # KB
            print(f"   ✓ {json_file.name} ({size:.1f} KB)")

    print("\n🔧 Next Steps:")
    print("\n1. Load PostgreSQL data:")
    print(f"   python src/create_postgres_schema.py {args.postgres_schema} --output ./data/schema.sql")
    print(f"   psql -d your_db -f ./data/schema.sql")
    print(f"   python src/insert_data.py {args.postgres_schema} ./data/postgres -d your_db -U user")

    print("\n2. Load MongoDB data:")
    print("   mongoimport --db fails_db --collection Fails --file ./data/mongodb/fails_db/Fails.json --jsonArray")
    print("   mongoimport --db fails_db --collection Statistics --file ./data/mongodb/fails_db/Statistics.json --jsonArray")

    print("\n3. Query Examples:")
    print("   PostgreSQL: SELECT * FROM settlements WHERE settlement_status = 'failed';")
    print("   MongoDB:    db.Fails.find({'state.fail_status': 'OPEN'})")

    print("\n🎉 Done!")


if __name__ == '__main__':
    main()
