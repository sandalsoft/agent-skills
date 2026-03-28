# OLW Bootstrap Skill

## Overview
The OLW Bootstrap skill automatically generates comprehensive Operational Language Wiki (OLW) systems from domain knowledge and institutional context. It creates interconnected wiki pages that document concepts, terminology, processes, and relationships.

## What It Creates

A complete wiki system with 15-25 pages covering:
- Core entities and organizational concepts
- Classification schemes and segmentation
- Products, services, and offerings
- Metrics, KPIs, and calculations
- Processes and operations
- Events, patterns, and triggers
- Strategic initiatives and business rules
- Data concepts and transaction types

## Features

- **Automatic Concept Extraction**: Analyzes domain context to identify key concepts
- **Cross-Linking**: Creates wiki:// links between related concepts
- **Semantic Richness**: Adds aliases and context for AI-powered search
- **Structured Content**: Organizes information with definitions, details, and sections
- **WikiPage v1 Compliance**: Generates valid YAML following specification
- **Comprehensive Coverage**: Ensures all major domain concepts are documented

## Usage

### Basic Invocation
```
Use the olw-bootstrap skill to create a wiki from [source] outputting to [directory]
```

### With Config File
```
Use olw-bootstrap to generate a wiki from globals/metadata/promptql-config.hml
```

### With Direct Description
```
Use olw-bootstrap to create a wiki for our e-commerce platform. We have customer tiers (bronze, silver, gold), product categories (electronics, clothing, home goods), and focus on conversion rates and customer lifetime value.
```

## Input Requirements

1. **Domain Context** (required):
   - Path to configuration/documentation files, OR
   - Direct description of domain concepts and terminology

2. **Output Directory** (optional):
   - Defaults to `globals/metadata/wiki/`
   - Specify custom path if needed

## Output

Creates multiple YAML files in WikiPage v1 format:

```yaml
kind: WikiPage
version: v1
definition:
  title: "Concept Name"
  definition: |
    Brief definition of the concept.
  details: |
    Expanded information with wiki:// cross-links.
  aliases:
    - "Alternative Name"
  sections:
    - title: "Section Name"
      content: |
        Detailed content.
```

## Examples

### Banking Domain
Input: Banking system with wealth/priority customer segments, 8% lending rate
Output: 20+ pages covering customer segments, financial products, rates, metrics, payment processing

### Healthcare Domain
Input: Healthcare system with patient types, treatment protocols, billing codes
Output: Pages for patient classifications, procedures, insurance concepts, billing processes

### E-commerce Domain
Input: Online retail with product catalogs, shopping cart, order fulfillment
Output: Pages for customer segments, product concepts, order lifecycle, conversion metrics

## Integration with PromptQL

The generated wiki integrates with PromptQL's Operational Language Wiki feature:

1. Enable OLW in project settings
2. Run olw-bootstrap skill to generate pages
3. Rebuild project to load wiki metadata
4. Access via Wiki tab in PromptQL interface
5. Use semantic search to explore concepts
6. Hover over wiki:// links for previews

## Best Practices

1. **Provide Rich Context**: The more detailed your domain description, the better the wiki
2. **Use Institutional Terminology**: Include specific terms your organization uses
3. **Include Numbers**: Specific rates, percentages, and thresholds improve documentation
4. **Describe Relationships**: Explain how concepts relate to each other
5. **Mention Assumptions**: Document business rules and operational assumptions

## Skill Architecture

- `skill.md`: Public-facing description and metadata
- `prompt.md`: Detailed instructions for the skill agent
- `skill.json`: Machine-readable configuration
- `README.md`: This comprehensive guide

## Version History

- **v1.0.0**: Initial release with comprehensive wiki generation capabilities

## Support

This skill is part of the Claude Code skill ecosystem. For issues or enhancements, refer to the Claude Code documentation.
