# Earnings Analysis Skill for Memory Semiconductors

A comprehensive Claude Code Skill for generating executive-ready post-earnings competitive intelligence reports for memory semiconductor companies.

## Overview

This skill enables automated, consistent earnings analysis following a proven methodology used at Intel for competitive intelligence. It's designed for analyzing Micron, SK Hynix, Samsung Memory, and other memory chip manufacturers.

**Typical output**: 2-page executive communique with financial analysis, strategic insights, and competitive implications.

## Installation

### For Claude Code (Recommended)

1. Copy this entire `earnings-analysis-skill` folder to one of these locations:

   **Project-specific** (shared via git):
   ```bash
   your-project/.claude/skills/earnings-analysis-memory-semiconductors/
   ```

   **User-wide** (available across all projects):
   ```bash
   ~/.claude/skills/earnings-analysis-memory-semiconductors/
   ```

2. Install Python dependencies:
   ```bash
   pip install pandas matplotlib plotly requests beautifulsoup4 tabula-py PyPDF2 --break-system-packages
   ```

### For Claude.ai

Upload the skill folder as a project resource, or manually copy the SKILL.md content into your conversation context when needed.

## Quick Start

### Step 1: Trigger the Skill

Simply ask Claude Code:
```
"Analyze Micron's Q2 FY25 earnings and create a report for SK Hynix leadership"
```

Claude will automatically invoke this skill and follow the methodology.

### Step 2: Provide Data Sources

You'll need:
- Earnings call transcript (AlphaSense, Seeking Alpha, or company IR site)
- Earnings presentation PDF
- Historical quarterly data (optional, for trends)

### Step 3: Review and Send

Claude generates the report following the proven structure. Review and send to stakeholders.

## Skill Components

### SKILL.md
Main instruction file that Claude reads to understand:
- When to use the skill
- Report structure and format
- Analysis methodology
- Financial metrics to track
- Competitive framing approach

### Python Scripts

Located in `/scripts/` directory:

1. **scrape_transcript.py**: Scrape earnings transcripts from free sources
   ```bash
   python scripts/scrape_transcript.py --company "Micron" --ticker "MU" --quarter "Q2" --year "2025"
   ```

2. **extract_financials.py**: Extract tables from earnings PDF
   ```bash
   python scripts/extract_financials.py --pdf "Micron_Q2FY25.pdf"
   ```

3. **compare_quarters.py**: Generate quarterly comparison tables
   ```bash
   python scripts/compare_quarters.py --company "Micron" --data historical_data.csv
   ```

4. **visualize_trends.py**: Create charts (revenue, margins, etc.)
   ```bash
   python scripts/visualize_trends.py --data historical_data.csv --charts all
   ```

5. **sankey_revenue.py**: Generate revenue flow Sankey diagram
   ```bash
   python scripts/sankey_revenue.py --data revenue_flow_data.csv
   ```

### Templates

Generate data templates:
```bash
# Historical quarterly data template
python scripts/compare_quarters.py --create-template

# Revenue flow data template
python scripts/sankey_revenue.py --create-template
```

## Report Structure

The skill generates reports with these sections:

1. **Subject Line**: `[Company] Q[X] FY[YY] Earnings Analysis - [Date]`
2. **Executive Summary**: 2-3 sentence bottom line
3. **Key Highlights**: 4-6 critical bullets
4. **Financial Performance**: Tables with trends (4+ quarters)
5. **Strategic Insights from Q&A**: Qualitative analysis with signal detection
6. **So What for SK Hynix**: Competitive implications
7. **Recommended Actions**: Next steps (if applicable)
8. **Appendix**: Full transcript

**Length**: Max 2 pages (excluding transcript)

## Key Features

### Financial Metrics Tracked
- Revenue (total, DRAM, NAND, emerging)
- Gross margin & operating margin
- Bit shipments & ASP trends
- CapEx & capacity plans
- Guidance vs. actuals

### Qualitative Analysis
- Management tone & confidence
- Customer demand signals
- Technology roadmap updates
- Pricing environment
- Inventory & channel health
- Competitive positioning

### Signal Detection
- 🟢 Positive signals (accelerating demand, pricing power, tech leadership)
- 🔴 Negative signals (softening demand, pricing pressure, delays)
- ⚠️ Watch signals (cautious guidance, risks, uncertainties)

### Competitive Intelligence
Frames findings in context of:
- Market conditions for SK Hynix
- Competitive threats & opportunities
- Technology positioning
- Strategic implications
- Pricing/demand trends

## Workflow Example

1. **Prepare** (10 min)
   - Download earnings transcript & presentation
   - Update historical data CSV

2. **Invoke Skill** in Claude Code
   ```
   "Generate post-earnings analysis for Micron Q2 FY25 with SK Hynix competitive framing"
   ```

3. **Claude Executes**:
   - Reads SKILL.md for methodology
   - Analyzes transcript & financials
   - Runs Python scripts for tables/charts
   - Generates structured report

4. **Review & Refine** (15 min)
   - Verify numbers
   - Add insider context
   - Polish "So What" section

5. **Distribute**
   - Email to exec team, BU leaders, peer analysts
   - File in competitive intelligence database

**Total time**: ~30-45 minutes (vs. 2-3 hours manual)

## Customization

### For Different Companies
Edit SKILL.md to change:
- Competitive context (SK Hynix → your company)
- Key competitors to track
- Strategic priorities
- Internal stakeholders

### For Different Industries
Fork the skill and modify:
- Financial metrics tracked
- Segment structure
- Technology landscape
- Competitive dynamics

### Add Your Insights
Include company-specific knowledge:
- Internal roadmaps
- Customer relationships
- Technology advantages
- Pricing strategies

## Best Practices

1. **Attend live calls** when possible (management tone matters)
2. **Update historical data** immediately after each quarter
3. **Deliver within 24 hours** of earnings call (speed = value)
4. **Fact-check everything** (executives act on this)
5. **Focus on forward signals** (not just past performance)
6. **Be concise** (every sentence adds value)
7. **Quantify claims** (use numbers to support arguments)
8. **Watch omissions** (what's NOT discussed reveals much)

## Memory Semiconductor Context

### Technology
- **DRAM**: DDR4, DDR5, DDR6, HBM2e, HBM3, HBM3E
- **NAND**: TLC, QLC, PLC, 3D NAND (176L-300L+)
- **Nodes**: 1α, 1β, 1γ (DRAM generations)

### Markets
- AI/Datacenter (highest growth, HBM-driven)
- Mobile (largest volume, price-sensitive)
- Enterprise (server DRAM/SSD)
- PC (cyclical, DDR transition)
- Automotive (growing, reliability-critical)

### Competitors
- **Big 3**: Samsung (leader), SK Hynix, Micron
- **NAND**: +Kioxia, Western Digital, YMTC

## Troubleshooting

**Skill not loading?**
- Verify folder is in correct location
- Check SKILL.md has valid YAML frontmatter
- Restart Claude Code

**Scripts failing?**
- Install dependencies: `pip install -r requirements.txt --break-system-packages`
- Check Python version (3.8+)
- Verify file paths

**Data extraction issues?**
- PDF structure varies by company
- May require manual data entry
- Use templates as guide

## Support

For questions or issues:
1. Check SKILL.md for methodology details
2. Review script documentation (run with `--help`)
3. Consult Claude Code documentation

## Version History

- **v1.0.0** (2025-10-30): Initial release
  - Full earnings analysis methodology
  - 5 automation scripts
  - Templates and examples

## License

This skill is provided as a reference implementation. Customize for your organization's needs.

---

**Created for**: Competitive intelligence professionals in memory semiconductors  
**Based on**: Intel CI methodology adapted for SK Hynix context  
**Typical use**: Quarterly earnings analysis of Micron (and other competitors)
