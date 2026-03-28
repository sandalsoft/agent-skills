# OLW Bootstrap Skill - Usage Examples

## Example 1: Banking Domain (From Config File)

### Command
```
Use the olw-bootstrap skill to create a wiki from globals/metadata/promptql-config.hml, outputting to globals/metadata/wiki/
```

### Input Context (from config file)
- Customer segments: "wealth" and "priority" (not "VIP")
- 8% lending rate for deposits
- 4% deposit rate for liquidity products
- Bill payment analysis with 7 categories
- 25% capture rate assumption
- 3-month product duration
- Cash flow stress periods based on payment variance

### Output
20 wiki pages created covering:
- Liberty National Bank (core entity)
- Customer segments (wealth, priority)
- Financial rates (lending, deposit, NIM)
- Products (liquidity management, deposit products)
- Metrics (capture rate, variance, excess cash flow)
- Operations (lending, bill payments)
- Analysis concepts (seasonal patterns, cash flow stress)

## Example 2: E-commerce Platform (Direct Description)

### Command
```
Use olw-bootstrap to create a wiki for our e-commerce platform.

Context:
- Customer tiers: Bronze (0-$500 annual spend), Silver ($500-$2000), Gold ($2000+)
- Product categories: Electronics, Clothing, Home Goods, Books, Toys
- Key metrics: Conversion Rate (2.5% target), Average Order Value ($75), Customer Lifetime Value
- Order states: Pending, Processing, Shipped, Delivered, Returned
- Shipping tiers: Standard (5-7 days), Express (2-3 days), Overnight
- Return window: 30 days from delivery
- Loyalty program: 1 point per dollar, 100 points = $5 credit
```

### Expected Output
~18 wiki pages covering:
- Core: E-commerce Platform
- Tiers: Bronze Customer, Silver Customer, Gold Customer, Customer Tiers
- Categories: Product Categories, Electronics, Clothing, Home Goods
- Metrics: Conversion Rate, Average Order Value, Customer Lifetime Value
- Process: Order Lifecycle, Shipping Process, Returns Process
- Program: Loyalty Program, Points System
- Data: Order Status, Shipping Tier

## Example 3: Healthcare System (From Documentation)

### Command
```
Use olw-bootstrap with domain context from docs/healthcare-domain.md
```

### Input Context (from markdown doc)
- Patient types: Inpatient, Outpatient, Emergency
- Insurance tiers: Medicare, Medicaid, Private, Self-Pay
- Treatment protocols: Standard Care, Intensive Care, Critical Care
- Billing codes: CPT (procedures), ICD-10 (diagnoses), DRG (diagnosis groups)
- Quality metrics: Patient satisfaction (>4.0/5.0), Readmission rate (<5%), Wait time (<15 min)
- Care transitions: Admission → Treatment → Discharge → Follow-up

### Expected Output
~22 wiki pages covering:
- Core: Healthcare System
- Patient Types: Inpatient, Outpatient, Emergency Patient
- Insurance: Medicare, Medicaid, Private Insurance, Self-Pay
- Care Levels: Standard Care, Intensive Care, Critical Care
- Billing: CPT Codes, ICD-10 Codes, DRG Codes, Billing Process
- Metrics: Patient Satisfaction, Readmission Rate, Wait Time
- Process: Care Transitions, Admission Process, Discharge Planning

## Example 4: SaaS Platform (Hybrid Approach)

### Command
```
Use olw-bootstrap for our SaaS platform.

Config file: app/config/business-rules.hml
Additional context:
- We use "Enterprise" not "Premium" for top tier
- Churn rate target is <3% monthly
- Free trial is 14 days, no credit card required
```

### Input Context (combined)
- Subscription tiers: Free, Pro ($29/mo), Enterprise ($99/mo)
- Feature gates: API calls (Free: 100/day, Pro: 10K/day, Enterprise: unlimited)
- User roles: Viewer, Editor, Admin, Owner
- Billing cycles: Monthly, Annual (2 months free)
- Support levels: Community (Free), Email (Pro), Priority+Phone (Enterprise)
- Key metrics: MRR, Churn Rate, ARPU, NRR

### Expected Output
~19 wiki pages covering:
- Core: SaaS Platform
- Tiers: Free Tier, Pro Tier, Enterprise Tier, Subscription Tiers
- Roles: User Roles, Viewer, Editor, Admin, Owner
- Features: API Rate Limits, Feature Gates
- Billing: Billing Cycles, Monthly Subscription, Annual Subscription
- Support: Support Levels, Priority Support
- Metrics: Monthly Recurring Revenue, Churn Rate, ARPU, Net Revenue Retention

## Example 5: Supply Chain System

### Command
```
Create a wiki for our supply chain management system using the domain model in models/supply-chain.json
```

### Input Context
- Facilities: Warehouse, Distribution Center, Retail Store
- Inventory states: In Stock, Low Stock (<10 units), Out of Stock, Backordered
- Shipping carriers: USPS, UPS, FedEx, DHL
- Lead times: Domestic (3-5 days), International (10-14 days)
- SKU categories: Fast-moving (>100/mo), Moderate (20-100/mo), Slow (<20/mo)
- Fulfillment SLA: 24 hours from order to ship

### Expected Output
~16 wiki pages covering:
- Core: Supply Chain System
- Facilities: Warehouse, Distribution Center, Retail Store
- Inventory: Inventory States, In Stock, Low Stock, Out of Stock, Backordered
- Shipping: Shipping Carriers, Lead Times, Domestic Shipping, International Shipping
- SKU: SKU Categories, Fast-Moving SKU, Slow-Moving SKU
- Operations: Fulfillment Process, Fulfillment SLA

## Tips for Best Results

### 1. Provide Specific Numbers
**Good**: "Premium customers spend >$10,000 annually"
**Better**: "Premium tier requires $10,000 minimum annual spend, averaging $15,500"

### 2. Use Institutional Terminology
**Good**: "Top customers"
**Better**: "Diamond Elite customers (not VIP or Premium)"

### 3. Explain Relationships
**Good**: "We have three product lines"
**Better**: "Product lines (Consumer, Business, Enterprise) map to customer segments and determine pricing tiers"

### 4. Include Calculations
**Good**: "We calculate retention"
**Better**: "Retention Rate = (Customers at End - New Customers) / Customers at Start × 100"

### 5. Document Assumptions
**Good**: "Fast shipping"
**Better**: "Standard fulfillment assumes 24-hour processing, 99% on-time ship rate, no holiday delays"

## Validation

After the skill runs, verify:

1. **File Count**: Should have 15-25 HML files
2. **Cross-Links**: Pages should reference related concepts with wiki://
3. **Structure**: Each page has title, definition, details, optional sections
4. **Aliases**: Alternative terms are captured
5. **Coverage**: All major concepts from input are documented
6. **Consistency**: Terminology matches institutional usage

## Common Issues

### Too Few Pages
- Provide more detailed domain context
- Include more concepts, metrics, and processes
- Add specific examples and numbers

### Missing Cross-Links
- Explain relationships between concepts explicitly
- Mention how processes use metrics
- Describe hierarchies and dependencies

### Generic Terminology
- Specify exact institutional terms
- Note what terms to avoid (e.g., "not VIP, use Diamond Elite")
- Include acronyms and abbreviations

### Incomplete Coverage
- List all categories, types, or tiers
- Document all states in a lifecycle
- Include both operational and strategic concepts
