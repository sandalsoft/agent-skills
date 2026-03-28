---
name: olw-bootstrap
description: Generates a comprehensive Operational Language Wiki (OLW) system from domain knowledge. Creates interconnected wiki pages following WikiPage v1 spec with cross-linking, aliases, and structured sections.
---

# OLW Bootstrap Skill

**Version**: 1.2.1

## Description
Automatically generates a comprehensive Operational Language Wiki (OLW) system from domain knowledge and institutional context. Creates interconnected wiki pages following the WikiPage v1 specification with proper cross-linking, aliases, and structured sections.

## Usage
Use this skill when you need to:
- Build a complete wiki system from scratch based on domain knowledge
- Document institutional terminology and operational concepts
- Create interconnected knowledge bases with semantic search support
- Transform system instructions or domain documentation into structured wiki pages

## Input Required
- **Domain Context**: Either a path to configuration/documentation files OR direct description of the domain
- **Output Directory**: Path to the wiki metadata directory (typically `globals/metadata/wiki/`)

## What This Skill Does
1. Analyzes domain knowledge and institutional context
2. Identifies key concepts, terminology, and relationships
3. Creates a comprehensive set of wiki pages covering:
   - Core entities and concepts
   - Business processes and operations
   - Metrics and measurements
   - Products and services
   - Strategic initiatives
   - Operational rules and assumptions
4. Establishes cross-links between related concepts using [Title](<wiki://Title>) format
5. Adds aliases for searchability
6. Structures content with definition, details, and optional sections
7. Ensures semantic coherence across the wiki system

## WikiPage v1 Specification

Each wiki page follows this HML structure (saved as `.hml` files):

```yaml
kind: WikiPage
version: v1
definition:
  title: "Page Title"
  definition: |
    Brief one-sentence definition of the concept
  details: |
    Comprehensive explanation with cross-links to related concepts.
    Use [Concept Name](<wiki://Concept Name>) format for cross-references.
  aliases:
    - "Alternative Name 1"
    - "Search Term 2"
    - "Common Abbreviation"
  sections:  # Optional structured sections
    - title: "Section Title"
      content: |
        Section content with additional detail
    - title: "Another Section"
      content: |
        More structured information
```

**Key Fields**:
- **title**: The canonical page title (used in cross-links)
- **definition**: A concise, one-sentence definition
- **details**: Comprehensive explanation with context and cross-links
- **aliases**: Array of alternative search terms and names
- **sections**: Optional array of titled content sections for structured information

## Output
- Multiple HML files (one per concept) in WikiPage v1 format
- Each file saved with `.hml` extension (e.g., `customer-profile.hml`)
- Proper cross-linking using [Title](<wiki://Title>) format where Title matches the WikiPage.definition.title exactly
- Comprehensive coverage of domain concepts
- Ready for semantic AI-powered search

## Example Invocation
```
Use the olw-bootstrap skill to create a wiki system from the domain context in globals/metadata/promptql-config.hml, outputting to globals/metadata/wiki/
```

## Notes
- The skill will create 15-25 wiki pages depending on domain complexity
- Each page follows WikiPage v1 specification with definition/details structure
- Cross-links are automatically identified and created
- Aliases improve semantic search effectiveness
- Use sections for structured content like rules, examples, or step-by-step processes
