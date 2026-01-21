s# Sankey Revenue Flow Skill for Memory Semiconductors

Generate interactive Sankey diagrams visualizing revenue flows for individual memory semiconductor companies.

## Overview

This skill creates visual representations of how revenue flows from total revenue through product segments (DRAM, NAND, Emerging) to end markets (AI/Datacenter, Mobile, Enterprise, PC, Automotive). Each diagram visualizes **one company at a time**.

**Supported companies** (with branded color schemes):
- Micron
- SK Hynix
- Samsung
- Western Digital
- Kioxia

**Use cases**: Earnings presentations, competitive analysis, strategic planning, quarterly performance reviews

**Typical output**: Interactive HTML Sankey diagram with optional PNG/SVG static export.

## Installation

### For Claude Code (Recommended)

1. Copy this folder to your skills location:

   **Project-specific** (shared via git):
   ```bash
   your-project/.claude/skills/sankey-revenue-flow-memory-semiconductors/
   ```

   **User-wide** (available across all projects):
   ```bash
   ~/.claude/skills/sankey-revenue-flow-memory-semiconductors/
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```

### For Claude.ai

Upload the skill folder as a project resource, or copy SKILL.md content into your conversation.

## Quick Start

### Recommended Workflow

**1. Extract data automatically** (Claude-assisted when using as a skill):
```bash
# Claude will help extract data from earnings reports, transcripts, or PDFs
# When using Claude Code: Just ask "Create a Sankey for Micron Q2 FY25"
```

**2. Verify and correct** the generated CSV:
- Data is pulled from latest earnings materials
- ⚠️ **IMPORTANT: Always verify the numbers against official sources**
- Make corrections directly in the generated CSV file (e.g., `micron_q2_fy25_data.csv`)

**3. Generate diagram**:
```bash
python scripts/sankey_generator.py --data micron_q2_fy25_data.csv --company "Micron" --quarter "Q2 FY25"
```

**4. View output**:
Open the generated HTML file in any web browser for interactive exploration.

### Alternative: Manual Template Entry
```bash
# Create empty template
python scripts/extract_revenue_data.py --create-template --company "Micron"

# Fill in values manually, then generate
python scripts/sankey_generator.py --data micron_revenue_template.csv --company "Micron" --quarter "Q2 FY25"
```

## Skill Components

### SKILL.md
Main instruction file that Claude reads for:
- When to use the skill
- Data format specifications
- Color schemes by company
- Output format options
- Workflow methodology

### Python Scripts

| Script | Purpose |
|--------|---------|
| `sankey_generator.py` | Core Sankey diagram generation (one company) |
| `extract_revenue_data.py` | Extract revenue data from earnings PDFs |
| `compare_companies.py` | Side-by-side comparison (2 companies OR 2 quarters) |

### Templates
- `scripts/templates/revenue_template.csv`: Input data template

### Examples
- `examples/example_data.csv`: Sample Micron Q2 FY25 data
- `examples/micron_q2_fy25_sankey.html`: Interactive output example
- `examples/micron_q2_fy25_sankey.png`: Static image example

## Data Format

CSV with three required columns:

```csv
source,target,value
Total Revenue,DRAM,6.75
Total Revenue,NAND,2.20
DRAM,AI/Datacenter,3.50
DRAM,Mobile,1.80
...
```

| Column | Required | Description |
|--------|----------|-------------|
| source | Yes | Source node name |
| target | Yes | Target node name |
| value | Yes | Flow value (billions USD) |
| color | No | Custom hex color |
| label | No | Custom hover label |

### ⚠️ Data Verification

**When using automatic extraction:**
- Data is sourced from latest earnings reports, transcripts, and presentations
- **Always verify values** against official 10-Q/10-K filings or earnings releases
- If you find discrepancies, **edit the CSV directly** before generating the diagram
- Common issues: allocation estimates for end markets, "Other" category breakdowns

**Where to make corrections:** Edit the generated CSV file (e.g., `micron_q2_fy25_data.csv`) with accurate values, then re-run the generator.

## Output Formats

| Format | Use Case | Command |
|--------|----------|---------|
| HTML | Interactive exploration | `--format html` (default) |
| PNG | Presentations | `--format png` |
| SVG | Graphic editing | `--format svg` |

## Usage Examples

### Typical Workflow (with Claude)
```bash
# 1. Ask Claude to extract and create diagram
# Claude will automatically:
#   - Extract revenue data from earnings materials
#   - Create CSV file (e.g., micron_q2_fy25_data.csv)
#   - Generate the Sankey diagram

# 2. If you need to make corrections, edit the CSV:
# Open micron_q2_fy25_data.csv, fix any values

# 3. Regenerate with corrected data:
python scripts/sankey_generator.py --data micron_q2_fy25_data.csv \
  --company "Micron" --quarter "Q2 FY25"
```

### Direct Generation
```bash
# With company branding
python scripts/sankey_generator.py --data revenue_data.csv \
  --company "Micron" --quarter "Q2 FY25"

# Export as PNG for presentations
python scripts/sankey_generator.py --data revenue_data.csv \
  --format png --output micron_sankey.png
```

### Compare Two Companies Side-by-Side
```bash
# Compare Micron vs SK Hynix
python scripts/compare_companies.py \
  --company1 micron_data.csv --company2 skhynix_data.csv

# Normalize to percentages for easier comparison
python scripts/compare_companies.py \
  --company1 micron_data.csv --company2 skhynix_data.csv --normalize
```

### Compare Same Company Across Quarters
```bash
# Requires CSV with 'quarter' column
python scripts/compare_companies.py \
  --data micron_quarterly.csv --quarters "Q1 FY25,Q2 FY25"
```

### Manual Data Entry Options
```bash
# Interactive CLI entry
python scripts/extract_revenue_data.py --interactive --company "Micron" --output micron_q2.csv

# Try PDF extraction (experimental, requires manual verification)
python scripts/extract_revenue_data.py --pdf earnings.pdf --company "Micron" --output revenue_data.csv
```

## Invoking with Claude

Simply ask:
```
"Create a Sankey diagram showing Micron's revenue flow"
"Visualize how revenue breaks down from segments to end markets"
"Generate revenue flow diagram for SK Hynix Q3 2025"
"Compare Micron vs SK Hynix revenue composition side-by-side"
```

**What Claude will do automatically:**
1. Extract revenue data from earnings reports, transcripts, or web sources
2. Create a properly formatted CSV file
3. Generate the interactive Sankey diagram
4. Provide the output with a verification reminder

**⚠️ Important:** Claude will include a note reminding you to verify the extracted data against official sources. If you find discrepancies, simply edit the generated CSV and ask Claude to regenerate the diagram.

For comparisons, the skill will generate side-by-side diagrams.

## Color Schemes

### Companies
- **Micron**: Blue (#0066B3)
- **SK Hynix**: Red (#ED1C24)
- **Samsung**: Samsung Blue (#1428A0)

### Segments
- **DRAM**: Purple-red (#A23B72)
- **NAND**: Orange (#F18F01)
- **Emerging**: Gray (#C2C5BB)

### End Markets
- **AI/Datacenter**: Teal (#2E86AB)
- **Mobile**: Green (#06A77D)
- **Enterprise**: Red (#D62839)
- **PC**: Gray-green (#717568)
- **Automotive**: Orange (#F26419)

## Data Sources

1. **Quarterly earnings** (10-Q/10-K): Segment revenue
2. **Earnings presentations**: Visual breakdowns
3. **Earnings calls**: End market commentary
4. **Industry reports**: TrendForce, Gartner estimates

## Troubleshooting

**"Module not found"**
```bash
pip install -r requirements.txt --break-system-packages
```

**"kaleido not found" (for PNG/SVG)**
```bash
pip install kaleido --break-system-packages
```

**"No data file provided"**
```bash
# Create template first
python scripts/sankey_generator.py --create-template
```

## Integration

Works well with:
- **earnings-analysis-skill**: Include in financial performance section
- **competitor-battle-card-skill**: Revenue composition comparisons

## Version History

- **v1.0.0** (2025-01): Initial release
  - Multi-layer Sankey support
  - Company color schemes
  - HTML/PNG/SVG output
  - Comparison mode

## License

This skill is provided as a reference implementation. Customize for your organization's needs.

---

**Created for**: Competitive intelligence and financial analysis in memory semiconductors
**Typical use**: Visualizing revenue composition for earnings analysis and competitor comparisons
