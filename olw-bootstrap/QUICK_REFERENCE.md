# OLW Bootstrap - Quick Reference Card

## Basic Usage

```
Use the olw-bootstrap skill to create a wiki from [SOURCE] outputting to [DIRECTORY]
```

## Common Patterns

### From Config File
```
Use olw-bootstrap to generate a wiki from globals/metadata/promptql-config.hml
```

### From Documentation
```
Use olw-bootstrap with domain context from docs/domain-model.md outputting to wiki/
```

### Direct Description
```
Use olw-bootstrap to create a wiki for [DOMAIN DESCRIPTION]
Output to: [DIRECTORY]
```

### Hybrid Approach
```
Use olw-bootstrap combining:
- Config: app/config/settings.hml
- Additional: We use "Enterprise" not "Premium", 14-day free trial
```

## Input Checklist

Provide these elements for best results:

- [ ] Domain name/description
- [ ] Key entities and concepts
- [ ] Classification schemes (tiers, types, categories)
- [ ] Products/services offered
- [ ] Metrics and calculations
- [ ] Processes and workflows
- [ ] Institutional terminology (what to use, what to avoid)
- [ ] Specific numbers (rates, percentages, thresholds)
- [ ] Business rules and assumptions
- [ ] Relationships between concepts

## Output Structure

Each wiki page includes:

```yaml
kind: WikiPage
version: v1
definition:
  title: "Concept Name"           # Clear, descriptive title
  definition: |                   # 1-3 sentence definition
    Brief explanation
  details: |                      # 2-4 paragraph expansion
    With wiki://cross-links
  aliases:                        # Alternative names
    - "Alt Name"
  sections:                       # Organized details
    - title: "Section"
      content: |
        Details
```

## Expected Output

- **File Count**: 15-25 HML files
- **Cross-Links**: 3-5 per page average
- **Coverage**: 90%+ of input concepts
- **Structure**: Definition + Details + Sections
- **Aliases**: 2+ per page for searchability

## Validation

```bash
# Count pages
ls [WIKI_DIR]/*.hml | wc -l

# Check cross-links
grep -r "wiki://" [WIKI_DIR]/

# Validate YAML
for f in [WIKI_DIR]/*.hml; do
  python -c "import yaml; yaml.safe_load(open('$f'))"
done
```

## Quality Indicators

✓ **Good Coverage**: All major concepts from input have pages
✓ **Well-Linked**: Pages reference related concepts
✓ **Clear Definitions**: Standalone, understandable explanations
✓ **Consistent Terms**: Uses institutional terminology
✓ **Rich Context**: Details provide business significance
✓ **Searchable**: Aliases capture alternative names

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Too few pages | Provide more detailed domain context |
| Missing links | Explain relationships explicitly |
| Generic terms | Specify institutional terminology |
| Shallow content | Include specific examples and calculations |
| Incomplete | List all categories, types, or states |

## Integration with PromptQL

1. Enable OLW: `featureFlags: { enable_wiki: true }`
2. Generate wiki: Use olw-bootstrap skill
3. Rebuild: `hasura ddn supergraph build local`
4. Access: Wiki tab in PromptQL UI
5. Search: Semantic AI-powered search
6. Navigate: Click pages, hover for previews

## Pro Tips

1. **Be Specific**: "Premium customers spend >$10K/year" beats "high-value customers"
2. **Use Exact Terms**: "Diamond Elite (not VIP)" ensures correct terminology
3. **Show Calculations**: "ROI = (Revenue - Cost) / Cost × 100" with examples
4. **Explain Relationships**: "Process uses metrics to determine strategy"
5. **Document Assumptions**: "Assumes 24-hour processing, no holidays"

## Performance

- Small domain (5-10 concepts): ~2-3 minutes
- Medium domain (15-25 concepts): ~3-5 minutes  
- Large domain (30+ concepts): ~5-8 minutes

## Files Generated

Pattern: `[concept-name].hml`

Examples:
- `customer-segmentation.hml`
- `wealth-customer.hml`
- `net-interest-margin.hml`
- `cash-flow-stress.hml`

## Categories Covered

1. Core entities (organization, system)
2. Classifications (segments, tiers)
3. Products/services
4. Metrics (KPIs, rates, calculations)
5. Processes (operations, workflows)
6. Events (patterns, triggers)
7. Strategic (initiatives, rules)
8. Data (fields, statuses)

## Version

Current: v1.0.0
Location: `~/.claude/skills/olw-bootstrap/`

## Getting Help

- Full guide: `README.md`
- Examples: `EXAMPLES.md`
- Testing: `TEST.md`
- Changes: `CHANGELOG.md`
