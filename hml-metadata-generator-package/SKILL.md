---
name: hml-metadata-generator
description: Automatically create and fill in descriptive metadata for Hasura DDN models, types, commands, and fields in .hml (Hasura Metadata Language) files. Use when working with Hasura DDN metadata files that need descriptions added or enhanced, when generating new .hml files from data sources, or when improving PromptQL's understanding of data models through better semantic metadata.
---

# HML Metadata Generator

## Overview

This skill enables automatic generation of descriptive metadata for Hasura DDN .hml files. It analyzes the structure of Models, ObjectTypes, Commands, Relationships, and other metadata objects to generate clear, contextual descriptions that help PromptQL better understand and query your data.

## When to Use This Skill

Use this skill when:
- Creating new .hml files from introspected data sources that lack descriptions
- Enriching existing .hml metadata with better descriptions
- Improving PromptQL's semantic understanding of your data models
- Standardizing description formats across your metadata files
- Documenting models, types, fields, and commands for team collaboration

## Quick Start

### Automated Approach (Recommended)

Use the provided Python script to automatically enrich single files or entire directories:

```bash
# Process a single .hml file
python scripts/add_metadata.py path/to/Model.hml

# Process all .hml files in a directory
python scripts/add_metadata.py path/to/metadata/ --recursive

# Preview changes without modifying files
python scripts/add_metadata.py path/to/metadata/ --dry-run --recursive
```

The script will:
1. Parse each .hml file (which may contain multiple YAML documents)
2. Analyze the structure of each metadata object (Model, ObjectType, Command, etc.)
3. Generate appropriate descriptions based on the object's properties
4. Add descriptions to objects and fields that are missing them
5. Write the enriched metadata back to the file

### Manual Approach

For more control or custom descriptions, read the HML structure reference and manually add descriptions:

1. Read `references/hml_structure.md` for detailed guidance on description formats
2. Identify which objects need descriptions (Models, ObjectTypes, Commands, etc.)
3. Follow the patterns and best practices for each object kind
4. Add descriptions using consistent, informative language

## Core Capabilities

### 1. Model Descriptions

Generates descriptions for Model objects that include:
- The object type being modeled
- The backing data source (connector and collection)
- Available operations (query, mutations, unique lookups)

**Example output:**
```yaml
kind: Model
version: v1
definition:
  name: Users
  objectType: User
  description: "Model representing a collection of User objects backed by the 'users' table in the postgres connector. Supports operations to query multiple records and query by unique identifiers."
```

### 2. ObjectType Descriptions

Generates descriptions for custom types that include:
- The number of fields
- Data connector mapping information

Additionally adds field-level descriptions that specify:
- What each field represents
- Nullability status
- Array vs scalar types
- Relationship to the parent type

**Example output:**
```yaml
kind: ObjectType
version: v1
definition:
  name: User
  description: "Type definition for User with 6 fields mapped to users."
  fields:
    - name: userId
      type: Int!
      description: "The user id for this User"
    - name: email
      type: String!
      description: "The email for this User"
    - name: orderIds
      type: [Int!]!
      description: "Array of Int representing the order ids for this User"
```

### 3. Command Descriptions

Generates descriptions for Command objects that include:
- The command name and purpose
- Return type
- Argument count and key argument names
- Data connector information

**Example output:**
```yaml
kind: Command
version: v1
definition:
  name: CreateUser
  outputType: User
  description: "Command operation 'CreateUser' that returns User. Accepts 2 arguments: email, name via postgres connector."
```

### 4. Relationship Descriptions

Generates descriptions for relationships connecting models:

**Example output:**
```yaml
kind: Relationship
version: v1
definition:
  name: orders
  description: "Relationship 'orders' connecting User to Orders."
```

### 5. Expression Type Descriptions

Generates descriptions for BooleanExpressions, OrderByExpressions, and AggregateExpressions:

**Example output:**
```yaml
kind: BooleanExpressionType
version: v1
definition:
  name: User_bool_exp
  description: "Boolean expression type for filtering User objects."
```

## Description Best Practices

### Be Specific and Informative
- Include actual entity names (model names, types, fields)
- Reference data sources when relevant (connector, collection/table)
- Mention key capabilities (query operations, unique lookups)

### Use Consistent Formatting
- Models: "Model representing a collection of {Type} objects..."
- Types: "Type definition for {Name} with N fields..."
- Fields: "The {readable_name} for this {ParentType}"
- Commands: "Command operation '{Name}' that returns {Type}..."

### Include Contextual Information
- For nullable fields, add "(nullable)" notation
- For array fields, specify "Array of {Type} representing..."
- For commands, list key arguments (first 3 if many)
- For models, mention backing collection/table name

### Convert Technical Names to Readable Text
- `userId` → "user id"
- `createdAt` → "created at"  
- `orderTotal` → "order total"
- `user_email` → "user email"

## Working with the Script

### Script Options

```bash
python scripts/add_metadata.py <path> [options]

Arguments:
  path              Path to .hml file or directory

Options:
  --recursive       Process all .hml files in subdirectories
  --dry-run         Preview changes without modifying files
```

### Safety Features

The script includes several safety features:
- **Preserves existing descriptions**: Won't overwrite meaningful descriptions (>20 chars)
- **Dry-run mode**: Preview all changes before applying
- **Validation**: Handles malformed YAML gracefully with error messages
- **Backup recommended**: Always commit or backup before bulk operations

### Common Workflows

**Initial metadata enrichment:**
```bash
# Preview changes across all metadata
python scripts/add_metadata.py app/metadata/ --recursive --dry-run

# Apply changes
python scripts/add_metadata.py app/metadata/ --recursive
```

**Single file update:**
```bash
python scripts/add_metadata.py app/metadata/Users.hml
```

**After introspecting a new connector:**
```bash
# New models typically lack descriptions
python scripts/add_metadata.py app/metadata/NewConnector*.hml
```

## Advanced Customization

### Custom Description Logic

To customize how descriptions are generated, modify the script's generator functions:
- `generate_model_description()` - Customize model descriptions
- `generate_field_description()` - Customize field descriptions
- `generate_objecttype_description()` - Customize type descriptions
- `generate_command_description()` - Customize command descriptions

### Domain-Specific Descriptions

For domain-specific terminology or business logic, you can:
1. Add conditional logic based on model/field names
2. Load custom terminology mappings from a configuration file
3. Use naming patterns to infer semantic meaning

Example modification:
```python
def generate_field_description(field_name: str, field_type: str, parent_type: str) -> str:
    # Add custom logic for specific domains
    if parent_type == "Customer" and field_name == "ltv":
        return "Lifetime value of this customer in USD"
    
    # Fall back to default logic
    return default_field_description(field_name, field_type, parent_type)
```

## Reference Material

For detailed information about HML structure and metadata fields, see:
- `references/hml_structure.md` - Complete reference for all metadata object kinds

This reference includes:
- Detailed structure for each object kind (Model, ObjectType, Command, etc.)
- Key fields to consider when writing descriptions
- Description patterns and examples
- Naming conventions and best practices

## Integration with PromptQL

Well-described metadata dramatically improves PromptQL's ability to:
- **Understand intent**: Better map natural language to the correct models and fields
- **Generate accurate queries**: Use appropriate fields based on semantic meaning
- **Provide context**: Explain what data represents to users
- **Handle ambiguity**: Disambiguate similar field names using descriptions

**Before:**
```yaml
fields:
  - name: amt
    type: Float
```

**After:**
```yaml
fields:
  - name: amt
    type: Float
    description: "The transaction amount in USD for this Payment"
```

With the improved description, PromptQL can confidently map "Show me payments over $100" to the `amt` field.

## Troubleshooting

### Script doesn't find .hml files
- Ensure you're using the correct path
- Use `--recursive` flag for subdirectories
- Check file extensions are exactly `.hml`

### Descriptions not being added
- Check if descriptions already exist (script preserves meaningful ones)
- Verify the YAML structure is valid
- Look for error messages in output

### Generated descriptions seem generic
- Consider manual editing for business-critical fields
- Customize the generator functions for domain-specific terms
- Use the reference guide for better patterns

### PyYAML not installed
```bash
pip install pyyaml --break-system-packages
```
