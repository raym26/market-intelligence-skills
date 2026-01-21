---
name: sankey-revenue-flow-memory-semiconductors
description: Generate interactive Sankey diagrams visualizing revenue flows for memory semiconductor companies. Shows breakdowns from total revenue to product segments (DRAM, NAND, Emerging) to end markets (AI/Datacenter, Mobile, Enterprise, PC, Automotive). Use for visualizing revenue composition, earnings presentations, or competitive comparisons.
version: 1.0.0
---

# Sankey Revenue Flow Diagrams for Memory Semiconductors

## Overview

This skill enables Claude to generate interactive Sankey diagrams that visualize revenue flows for memory semiconductor companies. The diagrams show how revenue breaks down from total revenue through product segments to end markets, providing clear visualization of business composition and revenue distribution.

**Typical output**: Interactive HTML Sankey diagram with optional PNG/SVG static export.

## When to Use This Skill

Invoke this skill when:
- User requests "Sankey diagram", "revenue flow", "revenue breakdown visualization"
- Visualizing segment-to-market revenue distribution for Micron, SK Hynix, Samsung Memory, etc.
- Creating earnings presentation visualizations
- Comparing revenue composition across competitors
- Analyzing revenue mix changes over time
- User wants to "show revenue flow" or "visualize revenue breakdown"

## Data Flow Layers

The Sankey diagram supports multiple layers of revenue flow:

### Layer 1: Total Revenue → Product Segments
- **DRAM**: Commodity and specialty DRAM (DDR4, DDR5, LPDDR, HBM)
- **NAND**: Flash storage products (SSDs, mobile NAND, enterprise)
- **Emerging/Other**: CXL memory, specialty products, other revenue

### Layer 2: Product Segments → End Markets
- **AI/Datacenter**: HBM, high-bandwidth memory, datacenter SSDs
- **Mobile**: LPDDR, mobile NAND, smartphone memory
- **Enterprise**: Server DRAM, enterprise SSDs
- **PC/Client**: Desktop/laptop DRAM and SSDs
- **Automotive**: Automotive-grade memory products
- **Industrial/IoT**: Industrial applications, embedded

### Layer 3 (Optional): End Markets → Profitability
- **Gross Profit**: Revenue minus COGS
- **COGS**: Cost of goods sold by segment

## Input Data Format

### CSV Structure
The skill expects CSV data with these columns:

| Column | Required | Description |
|--------|----------|-------------|
| source | Yes | Source node (e.g., "Total Revenue", "DRAM", "AI/Datacenter") |
| target | Yes | Target node (e.g., "DRAM", "AI/Datacenter", "Gross Profit") |
| value | Yes | Flow value in billions USD |
| color | No | Custom color for the flow (hex code) |
| label | No | Custom label for hover text |

### Example CSV
```csv
source,target,value
Total Revenue,DRAM,6.75
Total Revenue,NAND,2.20
Total Revenue,Emerging,0.10
DRAM,AI/Datacenter,3.50
DRAM,Mobile,1.80
DRAM,Enterprise,0.90
DRAM,PC,0.45
DRAM,Automotive,0.10
NAND,AI/Datacenter,0.80
NAND,Mobile,0.60
NAND,Enterprise,0.40
NAND,PC,0.30
NAND,Automotive,0.10
```

## Company Color Schemes

Use consistent colors for each company:

### Micron
- Primary: #0066B3 (Blue)
- DRAM: #A23B72 (Purple-red)
- NAND: #F18F01 (Orange)
- Emerging: #C2C5BB (Gray)

### SK Hynix
- Primary: #ED1C24 (Red)
- DRAM: #E74C3C (Light red)
- NAND: #F39C12 (Yellow-orange)
- Emerging: #95A5A6 (Gray)

### Samsung Memory
- Primary: #1428A0 (Samsung blue)
- DRAM: #3498DB (Blue)
- NAND: #9B59B6 (Purple)
- Emerging: #BDC3C7 (Gray)

### End Market Colors
- AI/Datacenter: #2E86AB (Teal)
- Mobile: #06A77D (Green)
- Enterprise: #D62839 (Red)
- PC: #717568 (Gray-green)
- Automotive: #F26419 (Orange)
- Industrial: #8338EC (Purple)
- Consumer: #3A86FF (Blue)

## Output Specifications

### HTML Output (Default/Preferred)
- Interactive Sankey diagram using Plotly
- Hover tooltips showing flow values
- Responsive design for different screen sizes
- Self-contained single HTML file

### PNG Output (Presentations)
- High-resolution static image (1200x600 default)
- Suitable for PowerPoint/Google Slides
- Clean white background

### SVG Output (Editing)
- Vector format for graphic editing
- Scalable without quality loss
- Editable in Adobe Illustrator, Inkscape, etc.

## Python Scripts

### sankey_generator.py
Main script for generating Sankey diagrams.

**Usage:**
```bash
# Generate from CSV data
python scripts/sankey_generator.py --data revenue_data.csv --output sankey.html

# Generate with title and company
python scripts/sankey_generator.py --data revenue_data.csv --company "Micron" --quarter "Q2 FY25"

# Generate PNG for presentations
python scripts/sankey_generator.py --data revenue_data.csv --format png --output sankey.png

# Create template CSV
python scripts/sankey_generator.py --create-template
```

### extract_revenue_data.py
Extract revenue breakdowns from earnings materials.

**Usage:**
```bash
# Extract from earnings PDF
python scripts/extract_revenue_data.py --pdf earnings.pdf --output revenue_data.csv

# Use manual template
python scripts/extract_revenue_data.py --create-template --company "Micron"
```

### compare_companies.py
Generate side-by-side Sankey comparisons.

**Usage:**
```bash
# Compare two companies
python scripts/compare_companies.py --company1 micron_data.csv --company2 skhynix_data.csv

# Compare same company across quarters
python scripts/compare_companies.py --data company_data.csv --quarters "Q1,Q2"
```

## Example Triggers

When user says:
- "Create a Sankey diagram for Micron's revenue"
- "Show me revenue flow from segments to end markets"
- "Visualize how revenue breaks down for [company]"
- "Generate revenue flow diagram for [company] [quarter]"
- "Compare Micron and SK Hynix revenue breakdown side by side"
- "Create a revenue composition visualization"

→ Invoke this skill and follow the methodology.

## Workflow

### Step 1: Data Collection
- Gather segment revenue data from earnings (10-Q, earnings presentation)
- Identify end market breakdown (often in earnings call commentary)
- Estimate splits if exact data not disclosed (note assumptions)

### Step 2: Prepare CSV
- Create CSV with source-target-value structure
- Include all three layers if data available
- Use template for consistent format

### Step 3: Generate Diagram
```bash
python scripts/sankey_generator.py --data [company]_revenue.csv \
  --company "[Company]" --quarter "[Quarter]" --output [company]_sankey.html
```

### Step 4: Review and Export
- Open HTML in browser to verify
- Export PNG for presentations if needed
- Include in earnings analysis report

## Data Sources

### Primary
1. **Quarterly Earnings**: Revenue by segment from 10-Q/10-K
2. **Earnings Presentation**: Visual breakdowns, pie charts
3. **Earnings Call**: Management commentary on end market mix

### Secondary
1. **TrendForce/Gartner**: Industry estimates by application
2. **Prior Quarters**: Historical data for consistency
3. **Competitor Comparisons**: Industry reports

### Data Estimation
When exact data isn't disclosed:
- Use management commentary percentages
- Apply industry average splits
- Note assumptions clearly in output
- Flag estimated vs. reported data

## Tips for Excellence

1. **Consistency**: Use same color scheme for same segments across diagrams
2. **Labels**: Include dollar values and percentages in node labels
3. **Interactivity**: Prefer HTML output for detailed exploration
4. **Context**: Always include quarter and fiscal year in title
5. **Accuracy**: Flag estimated values vs. reported values
6. **Comparability**: Maintain consistent category definitions across companies
7. **Updates**: Regenerate after each earnings for latest data

## Integration with Other Skills

This skill works well with:
- **earnings-analysis-skill**: Include Sankey in "Bonus Visualization" section
- **competitor-battle-card-skill**: Revenue composition comparison for battle cards

## Output Format

When generating Sankey diagrams, provide:
1. The generated HTML/PNG file path
2. Summary table of revenue by segment
3. Summary table of revenue by end market
4. Total revenue figure
5. Any assumptions made for estimated data

## Memory Semiconductor Context

### Segment Revenue Drivers
- **DRAM**: Price-per-bit, bit shipments, product mix (commodity vs. HBM)
- **NAND**: Enterprise SSD vs. consumer, QLC adoption, supply discipline
- **Emerging**: CXL adoption, specialty memory design wins

### End Market Dynamics
- **AI/Datacenter**: HBM demand from NVIDIA, AMD; enterprise AI buildout
- **Mobile**: Smartphone volume, content per device, LPDDR5 adoption
- **Enterprise**: Server refresh cycles, cloud CapEx
- **PC**: Consumer PC demand, DDR5 transition
- **Automotive**: EV content growth, ADAS requirements

### Typical Revenue Mix (Memory Industry)
- DRAM: 65-75% of total revenue
- NAND: 25-35% of total revenue
- Emerging: 1-5% of total revenue

### Typical End Market Mix (DRAM)
- AI/Datacenter: 35-45% (growing rapidly)
- Mobile: 20-30%
- Enterprise: 10-15%
- PC: 15-20%
- Automotive: 3-5%
