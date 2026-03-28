# Testing the OLW Bootstrap Skill

## Quick Test

To test the olw-bootstrap skill, use this command:

```
Use the olw-bootstrap skill to create a test wiki.

Domain: Coffee Shop Chain

Context:
- Locations: Flagship Store (downtown), Neighborhood Cafe, Drive-Thru Express
- Customer tiers: Casual (0-5 visits/month), Regular (6-15), Frequent (16+)
- Drink sizes: Tall (12oz), Grande (16oz), Venti (20oz)
- Loyalty program: 1 star per $1 spent, 50 stars = free drink
- Drink categories: Espresso, Brewed Coffee, Tea, Specialty Beverages
- Peak hours: 7-9am (morning rush), 2-4pm (afternoon peak)
- Order channels: In-store, Mobile App, Drive-Thru
- Prep time targets: Hot drinks <3min, Cold drinks <4min

Output to: /tmp/coffee-wiki/
```

This should create approximately 15-18 wiki pages covering:
- Coffee Shop Chain (core)
- Location types (3 pages)
- Customer tiers (4 pages including parent)
- Products (drink sizes, categories)
- Loyalty program
- Operations (peak hours, channels, prep times)

## Validation Checklist

After running the skill:

- [ ] Files created in output directory
- [ ] 15-25 HML files generated
- [ ] Each file follows WikiPage v1 format
- [ ] Files contain proper YAML structure
- [ ] Cross-links use wiki:// protocol
- [ ] Aliases are present where appropriate
- [ ] Sections organize content logically
- [ ] Terminology matches input (e.g., "Frequent" not "VIP")
- [ ] Calculations include examples where relevant
- [ ] All major concepts from input are covered

## Sample Validation Commands

```bash
# Count wiki pages
ls /tmp/coffee-wiki/*.hml | wc -l

# Check for cross-links
grep -r "wiki://" /tmp/coffee-wiki/

# Verify YAML structure
head -20 /tmp/coffee-wiki/coffee-shop-chain.hml

# Check for aliases
grep -A5 "aliases:" /tmp/coffee-wiki/*.hml

# Validate YAML syntax
for f in /tmp/coffee-wiki/*.hml; do
  python -c "import yaml; yaml.safe_load(open('$f'))" && echo "$f: OK" || echo "$f: ERROR"
done
```

## Expected Output Structure

### Core Page: coffee-shop-chain.hml
```yaml
kind: WikiPage
version: v1
definition:
  title: "Coffee Shop Chain"
  definition: |
    A multi-location coffee retail business operating Flagship Stores,
    Neighborhood Cafes, and Drive-Thru Express locations serving espresso,
    brewed coffee, tea, and specialty beverages.
  details: |
    The coffee shop chain serves customers across three location types...
    Wiki links to wiki://flagship-store, wiki://customer-tiers, wiki://loyalty-program
  sections:
    - title: "Business Model"
      content: |
        ...
```

### Example Cross-Linked Page: frequent-customer.hml
```yaml
kind: WikiPage
version: v1
definition:
  title: "Frequent Customer"
  definition: |
    The highest tier in customer segmentation, representing customers who
    visit 16 or more times per month.
  details: |
    Frequent customers are part of the wiki://customer-tiers system...
    They benefit most from the wiki://loyalty-program due to high visit frequency.
  aliases:
    - "Frequent Tier"
    - "Top Customer"
```

## Integration Test

After generating wiki files, test integration:

1. **Copy to PromptQL Project**
   ```bash
   cp /tmp/coffee-wiki/*.hml path/to/promptql-project/globals/metadata/wiki/
   ```

2. **Enable OLW Feature**
   - Add to promptql-config.hml:
   ```yaml
   featureFlags:
     enable_wiki: true
   ```

3. **Rebuild Project**
   ```bash
   hasura ddn supergraph build local
   ```

4. **Test in PromptQL UI**
   - Navigate to Wiki tab
   - Search for "loyalty"
   - Click on "Frequent Customer"
   - Hover over wiki:// links
   - Verify previews appear

## Troubleshooting

### Skill Not Found
```
Error: skill 'olw-bootstrap' not found
```
**Solution**: Ensure skill files are in `~/.claude/skills/olw-bootstrap/`

### Invalid YAML
```
Error: invalid YAML syntax
```
**Solution**: Check indentation (2 spaces), ensure pipe characters for multi-line

### Missing Cross-Links
**Solution**: Provide more context about relationships between concepts

### Too Few Pages
**Solution**: Add more detail to domain context, list more concepts

### Generic Names
**Solution**: Be explicit about institutional terminology in the input

## Advanced Testing

### Test with Real Config
```
Use olw-bootstrap with globals/metadata/promptql-config.hml
```

### Test with Multiple Sources
```
Use olw-bootstrap combining:
- Config: app/config/business.hml
- Docs: docs/domain-model.md
- Additional context: We use "Pro" not "Professional" for mid-tier
```

### Test with Minimal Input
```
Use olw-bootstrap for a simple task tracker.
Context: Tasks have statuses (Todo, In Progress, Done), priorities (Low, Medium, High), and assignees.
```

## Performance Expectations

- **Small domain** (5-10 concepts): ~10-15 pages, 2-3 minutes
- **Medium domain** (15-25 concepts): ~15-20 pages, 3-5 minutes
- **Large domain** (30+ concepts): ~20-25 pages, 5-8 minutes

## Quality Metrics

Good wiki output should have:
- **Coverage**: 90%+ of input concepts documented
- **Interconnection**: Average 3-5 cross-links per page
- **Completeness**: 100% of pages have definition + details
- **Structure**: 60%+ of pages have 2+ sections
- **Searchability**: 70%+ of pages have 2+ aliases
