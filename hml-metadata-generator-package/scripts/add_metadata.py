#!/usr/bin/env python3
"""
HML Metadata Enrichment Script

This script analyzes .hml files containing Hasura DDN metadata (Models, Types, Commands, etc.)
and automatically adds or enhances descriptive metadata fields based on the structure and content.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml


def parse_hml_file(file_path: str) -> List[Dict[str, Any]]:
    """Parse an HML file and return list of metadata objects."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # HML files can contain multiple YAML documents separated by ---
        documents = list(yaml.safe_load_all(content))
        return [doc for doc in documents if doc is not None]
    except Exception as e:
        print(f"Error parsing {file_path}: {e}", file=sys.stderr)
        return []


def generate_model_description(model_def: Dict[str, Any]) -> str:
    """Generate a descriptive string for a Model."""
    name = model_def.get('name', 'Unknown')
    object_type = model_def.get('objectType', 'unknown type')
    
    # Analyze source information
    source = model_def.get('source')
    source_info = ""
    if source:
        collection = source.get('collection', '')
        connector = source.get('dataConnectorName', '')
        if collection:
            source_info = f" backed by the '{collection}' collection"
        if connector:
            source_info += f" in the {connector} connector"
    
    # Check for GraphQL operations
    graphql = model_def.get('graphql', {})
    operations = []
    if graphql.get('selectMany'):
        operations.append("query multiple records")
    if graphql.get('selectUniques'):
        operations.append("query by unique identifiers")
    
    ops_desc = ""
    if operations:
        ops_desc = f". Supports operations to {' and '.join(operations)}"
    
    desc = f"Model representing a collection of {object_type} objects{source_info}{ops_desc}."
    
    return desc


def generate_field_description(field_name: str, field_type: str, parent_type: str) -> str:
    """Generate a descriptive string for an object type field."""
    # Clean the type (remove ! and [])
    clean_type = field_type.replace('!', '').replace('[', '').replace(']', '')
    
    # Convert camelCase/PascalCase field names to readable text
    readable_name = re.sub(r'([A-Z])', r' \1', field_name).strip().lower()
    readable_name = re.sub(r'_', ' ', readable_name)
    
    # Determine nullability
    nullable_text = "" if "!" in field_type else " (nullable)"
    is_array = "[" in field_type
    
    if is_array:
        desc = f"Array of {clean_type} representing the {readable_name} for this {parent_type}{nullable_text}"
    else:
        desc = f"The {readable_name} for this {parent_type}{nullable_text}"
    
    return desc


def generate_objecttype_description(type_def: Dict[str, Any]) -> str:
    """Generate a descriptive string for an ObjectType."""
    name = type_def.get('name', 'Unknown')
    fields = type_def.get('fields', [])
    
    # Count field types
    field_count = len(fields)
    
    # Check for data connector mapping
    mapping = type_def.get('dataConnectorTypeMapping', [])
    mapping_info = ""
    if mapping:
        connector_type = mapping[0].get('dataConnectorObjectType', '')
        if connector_type:
            mapping_info = f" mapped to {connector_type}"
    
    desc = f"Type definition for {name} with {field_count} field{'s' if field_count != 1 else ''}{mapping_info}."
    
    return desc


def generate_command_description(cmd_def: Dict[str, Any]) -> str:
    """Generate a descriptive string for a Command."""
    name = cmd_def.get('name', 'Unknown')
    output_type = cmd_def.get('outputType', 'unknown')
    
    # Analyze arguments
    arguments = cmd_def.get('arguments', [])
    arg_count = len(arguments)
    arg_info = ""
    if arg_count > 0:
        arg_names = [arg.get('name', '') for arg in arguments[:3]]
        arg_info = f" Accepts {arg_count} argument{'s' if arg_count != 1 else ''}"
        if arg_names:
            arg_info += f": {', '.join(arg_names)}"
        if arg_count > 3:
            arg_info += ", etc."
    
    # Check source information
    source = cmd_def.get('source')
    source_info = ""
    if source:
        connector = source.get('dataConnectorName', '')
        if connector:
            source_info = f" via {connector} connector"
    
    desc = f"Command operation '{name}' that returns {output_type}{arg_info}{source_info}."
    
    return desc


def enrich_metadata_object(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Add or enhance description fields in a metadata object."""
    if not isinstance(obj, dict):
        return obj
    
    kind = obj.get('kind')
    definition = obj.get('definition', {})
    
    # Skip if description already exists and is meaningful
    existing_desc = definition.get('description', '').strip()
    if existing_desc and len(existing_desc) > 20:
        return obj
    
    # Generate descriptions based on object type
    if kind == 'Model':
        definition['description'] = generate_model_description(definition)
        
        # Add field descriptions if missing
        object_type = definition.get('objectType')
        if object_type:
            # Note: Field descriptions would typically be in the ObjectType definition
            pass
    
    elif kind == 'ObjectType':
        definition['description'] = generate_objecttype_description(definition)
        
        # Add descriptions to fields
        fields = definition.get('fields', [])
        for field in fields:
            if not field.get('description'):
                field_name = field.get('name', '')
                field_type = field.get('type', '')
                type_name = definition.get('name', 'object')
                field['description'] = generate_field_description(field_name, field_type, type_name)
    
    elif kind == 'Command':
        definition['description'] = generate_command_description(definition)
    
    elif kind == 'Relationship':
        name = definition.get('name', 'Unknown')
        source = definition.get('source', 'source')
        target = definition.get('target', {}).get('model', {}).get('name', 'target')
        definition['description'] = f"Relationship '{name}' connecting {source} to {target}."
    
    elif kind == 'BooleanExpressionType':
        name = definition.get('name', 'Unknown')
        definition['description'] = f"Boolean expression type for filtering {name} objects."
    
    elif kind == 'OrderByExpression':
        name = definition.get('name', 'Unknown')
        definition['description'] = f"Order by expression for sorting {name} objects."
    
    elif kind == 'AggregateExpression':
        name = definition.get('name', 'Unknown')
        definition['description'] = f"Aggregate expression for computing aggregates on {name}."
    
    return obj


def write_hml_file(file_path: str, documents: List[Dict[str, Any]]) -> None:
    """Write enriched metadata back to HML file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, doc in enumerate(documents):
                if i > 0:
                    f.write('\n---\n')
                yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"✅ Successfully enriched: {file_path}")
    except Exception as e:
        print(f"❌ Error writing {file_path}: {e}", file=sys.stderr)


def process_hml_file(file_path: str, dry_run: bool = False) -> None:
    """Process a single HML file to add metadata."""
    documents = parse_hml_file(file_path)
    if not documents:
        return
    
    enriched_documents = [enrich_metadata_object(doc) for doc in documents]
    
    if dry_run:
        print(f"🔍 Would enrich: {file_path}")
        return
    
    write_hml_file(file_path, enriched_documents)


def find_hml_files(directory: str) -> List[str]:
    """Recursively find all .hml files in directory."""
    hml_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.hml'):
                hml_files.append(os.path.join(root, file))
    return hml_files


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Add descriptive metadata to Hasura DDN .hml files'
    )
    parser.add_argument(
        'path',
        help='Path to .hml file or directory containing .hml files'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Process all .hml files in directory recursively'
    )
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if not path.exists():
        print(f"❌ Error: Path '{path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Collect files to process
    files_to_process = []
    if path.is_file():
        if path.suffix == '.hml':
            files_to_process.append(str(path))
        else:
            print(f"❌ Error: '{path}' is not an .hml file", file=sys.stderr)
            sys.exit(1)
    elif path.is_dir():
        if args.recursive:
            files_to_process = find_hml_files(str(path))
        else:
            files_to_process = [str(f) for f in path.glob('*.hml')]
    
    if not files_to_process:
        print(f"⚠️  No .hml files found in '{path}'")
        sys.exit(0)
    
    print(f"📁 Found {len(files_to_process)} .hml file(s) to process")
    
    # Process each file
    for file_path in files_to_process:
        process_hml_file(file_path, dry_run=args.dry_run)
    
    if args.dry_run:
        print("\n💡 Run without --dry-run to apply changes")
    else:
        print(f"\n✨ Completed! Processed {len(files_to_process)} file(s)")


if __name__ == '__main__':
    main()
