---
skill: promptql-bootstrap
description: Analyze HML metadata files to understand the data model and generate a high-level project description for PromptQL configuration
tags: [hasura, metadata, promptql, bootstrap]
---

# PromptQL Bootstrap

This skill analyzes ObjectType and ModelType definitions in Hasura DDN metadata files to understand the data model, then generates a comprehensive project description and updates the PromptQL configuration.

## Task

1. **Discover and Read HML Files**
   - Find all .hml files in `app/metadata/` directory
   - Read each file to extract ObjectType and ModelType definitions
   - Pay special attention to:
     - Object and field descriptions
     - Field types and relationships
     - Model definitions and their purposes

2. **Analyze the Data Model**
   - Catalog all entities (ObjectTypes) and their purposes
   - Understand relationships between entities
   - Identify key business domains represented in the data
   - Note any patterns or conventions in the naming and structure

3. **Generate Project Description**
   - Use your domain knowledge to understand the business context
   - Create a high-level description that includes:
     - What domain/industry this project serves
     - The main entities and their relationships
     - Key use cases or workflows supported
     - Any notable business rules or constraints
   - The description should be clear, concise, and help PromptQL understand the data context
   - Format as a comprehensive system instruction (2-4 paragraphs)

4. **Update PromptQL Configuration**
   - Read the current `./globals/promptql-config.hml` file
   - Locate the `definition.systemInstructions` field
   - Update it with the generated project description
   - Preserve all other configuration settings

## Output

Provide a summary showing:
- Number of ObjectTypes and ModelTypes discovered
- List of main entities found
- The generated project description
- Confirmation that promptql-config.hml was updated

## Example System Instructions Format

The system instructions should be comprehensive and informative, for example:

```
This is a banking and financial services data model for [Bank Name], focusing on [key aspects like transactions, accounts, customers, etc.]. The model includes entities for [list main entities] and supports workflows such as [key workflows]. Key relationships include [important relationships]. The data is structured to handle [specific business requirements] with particular attention to [notable features or constraints].
```

## Notes

- If app/metadata/ or globals/ directories don't exist, inform the user that this appears to be a pre-Hasura DDN setup
- Be thorough in analyzing descriptions - they contain valuable business context
- Use your knowledge of banking, finance, or other relevant domains to enrich the description
- The system instructions will be used by PromptQL to better understand natural language queries
