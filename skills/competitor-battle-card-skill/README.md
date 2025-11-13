# Competitor Battle Card Skill for Memory Semiconductors

A comprehensive Claude Code Skill for generating executive-ready competitor battle cards for memory semiconductor companies.

## Overview

This skill automates the creation of detailed competitor profiles following a proven methodology used at Intel for competitive intelligence. It's designed for analyzing Micron, Samsung Memory, SK Hynix, and other memory chip manufacturers.

**Typical output**: 1-2 page battle card with company snapshot, product portfolio, competitive positioning, strengths/weaknesses, win/loss patterns, and sales messaging.

## Installation

### For Claude Code (Recommended)

1. Copy this entire `competitor-battle-card-skill` folder to one of these locations:

   **Project-specific** (shared via git):
   ```bash
   your-project/.claude/skills/competitor-battle-card-memory-semiconductors/
   ```

   **User-wide** (available across all projects):
   ```bash
   ~/.claude/skills/competitor-battle-card-memory-semiconductors/
   ```

2. Install Python dependencies:
   ```bash
   pip install pandas matplotlib plotly requests beautifulsoup4 yfinance PyPDF2 pdfplumber --break-system-packages
   ```

### For Claude.ai

Upload the skill folder as a project resource, or manually copy the SKILL.md content into your conversation context when needed.

## Quick Start

### Step 1: Trigger the Skill

Simply ask Claude Code:
```
"Create a battle card for Micron from SK Hynix's perspective"
```

Claude will automatically invoke this skill and follow the methodology.

### Step 2: Provide Data Sources (Optional)

For best results, have these available:
- Latest 10-K or 10-Q filing
- Recent earnings call transcript
- Product portfolio information (from company website)
- Internal win/loss data (if available)

Claude can also search and gather this information autonomously.

### Step 3: Review and Distribute

Claude generates the battle card following the proven structure. Review, add insider context, and distribute to sales/exec teams.

## Skill Components

### SKILL.md
Main instruction file that Claude reads to understand:
- When to use the skill
- Battle card structure and format
- Analysis methodology
- Data sources and collection process
- Competitive framing approach

### Python Scripts

Located in `/scripts/` directory:

1. **scrape_company_data.py**: Scrape company IR sites, press releases
   ```bash
   python scripts/scrape_company_data.py --company "Micron" --ticker "MU"
   ```

2. **extract_financials.py**: Extract financials from 10-K/10-Q PDFs
   ```bash
   python scripts/extract_financials.py --filing "10-K" --ticker "MU"
   ```

3. **compare_competitors.py**: Generate side-by-side competitor comparison tables
   ```bash
   python scripts/compare_competitors.py --competitors "Micron,Samsung,SKHynix" --metrics "revenue,margin,capex"
   ```

4. **visualize_positioning.py**: Create competitive positioning charts
   ```bash
   python scripts/visualize_positioning.py --dimensions "technology,cost,hbm_share"
   ```

5. **track_news.py**: Monitor news feeds for competitor updates
   ```bash
   python scripts/track_news.py --company "Micron" --days 180
   ```

### Templates

Generate data templates:
```bash
# Competitor comparison template
python scripts/compare_competitors.py --create-template

# Product portfolio template
python scripts/scrape_company_data.py --create-template
```

## Battle Card Structure

The skill generates battle cards with these sections:

1. **Header**: Company name, date, prepared for, next review
2. **Company Snapshot**: HQ, leadership, financials, strategic focus
3. **Product Portfolio**: DRAM, NAND, HBM, emerging technologies
4. **Competitive Positioning Matrix**: Dimension-by-dimension vs. SK Hynix
5. **Strengths**: 4-6 competitive advantages
6. **Weaknesses**: 4-6 vulnerabilities to exploit
7. **Key Differentiators**: What makes SK Hynix better
8. **How to Compete**: Sales messaging & objection handling
9. **Win/Loss Patterns**: Where we win, where we lose, why
10. **Recent Developments**: Last 6 months of key events
11. **Key Strategic Questions**: For senior management
12. **Recommended Actions**: By function (sales, product, strategy, CI)

**Length**: 1-2 pages (dense but scannable)

## Key Features

### Comprehensive Company Analysis
- Financial metrics (revenue, margins, CapEx, R&D)
- Leadership team and organizational structure
- Strategic priorities and market positioning
- Product portfolio across DRAM, NAND, HBM

### Competitive Intelligence
- Strengths and weaknesses vs. SK Hynix
- Technology positioning (nodes, HBM generations, NAND layers)
- Market share and customer relationships
- Win/loss patterns and decision factors

### Sales Enablement
- Common objections and counter-messaging
- Winning messages for SK Hynix
- Competitive positioning guidance
- Where to compete vs. where to avoid

### Strategic Framing
- Key questions for senior management
- Recommended actions by function
- Competitive threats and opportunities
- Forward-looking implications

## Workflow Example

1. **Prepare** (15 min)
   - Identify competitor to profile
   - Gather recent 10-K, earnings materials
   - Review any internal win/loss data

2. **Invoke Skill** in Claude Code
   ```
   "Generate competitor battle card for Micron with SK Hynix framing"
   ```

3. **Claude Executes**:
   - Reads SKILL.md for methodology
   - Searches/analyzes public filings and data
   - Runs Python scripts for comparisons
   - Generates structured battle card

4. **Review & Enhance** (30 min)
   - Verify financial numbers
   - Add insider knowledge (customer feedback, internal data)
   - Refine sales messaging based on recent deals
   - Polish strategic questions

5. **Distribute**
   - Sales teams (for customer engagements)
   - Executive briefings
   - Product/strategy teams
   - Quarterly updates

**Total time**: ~1 hour (vs. 4-6 hours manual)

## Customization

### For Different Companies
Edit SKILL.md to change:
- Your company perspective (SK Hynix → your company)
- Key competitors to track
- Strategic priorities and focus areas
- Internal stakeholders and distribution

### For Different Industries
Fork the skill and modify:
- Financial metrics tracked
- Product categories
- Technology landscape
- Competitive dynamics
- Market structure

### Add Your Insights
Include company-specific knowledge:
- Internal win/loss data
- Customer feedback and preferences
- Technology roadmap and advantages
- Strategic priorities and concerns

## Best Practices

1. **Update Quarterly**: Refresh after competitor earnings calls
2. **Be Honest**: Acknowledge competitor strengths; hiding gaps helps no one
3. **Make It Actionable**: Sales teams need "what to say" not just "what to know"
4. **Stay Current**: Add recent developments within 48 hours
5. **Quantify Claims**: Use specific numbers and data
6. **Focus Forward**: Emphasize future threats/opportunities
7. **Keep It Scannable**: Execs skim; make key points jump out
8. **Cite Sources**: Add footnotes for credibility
9. **Test Messaging**: Validate sales objection handling with field teams
10. **Track Effectiveness**: Monitor which battle cards drive wins

## Memory Semiconductor Context

### Technology
- **DRAM Nodes**: 1α, 1β, 1γ, 1δ (smaller = more advanced)
- **HBM**: HBM2e, HBM3, HBM3E, HBM4 (AI/datacenter memory)
- **DDR**: DDR4 (mature), DDR5 (ramping), DDR6 (development)
- **NAND**: 176L, 232L, 300L+ (3D stacking, more layers = more bits)

### Markets
- **AI/Datacenter**: HBM-driven, highest growth and margins
- **Mobile**: Largest volume (smartphones), LPDDR memory
- **Enterprise**: Server DRAM/SSD, stable demand
- **PC**: Cyclical, DDR transitions
- **Automotive**: Growing, reliability-critical

### Competitors
- **Big 3**: Samsung (leader ~35-40%), SK Hynix (~30% DRAM), Micron (~20-25%)
- **HBM Leaders**: SK Hynix (60%+), Samsung (30%+), Micron (entering)
- **NAND**: +Kioxia, Western Digital, YMTC

## Use Cases

### Sales Enablement
- Pre-call prep for customer meetings
- Objection handling training
- Win/loss analysis and improvement
- Competitive deal strategy

### Executive Briefings
- Board meetings
- Strategic planning sessions
- Quarterly business reviews
- Investor relations prep

### Product Strategy
- Roadmap competitive benchmarking
- Feature prioritization
- Technology investment decisions
- Pricing and positioning

### Competitive Intelligence
- Ongoing competitor monitoring
- Strategic threat assessment
- Market dynamics analysis
- Technology landscape tracking

## Troubleshooting

**Skill not loading?**
- Verify folder is in correct location (check path)
- Check SKILL.md has valid YAML frontmatter
- Restart Claude Code

**Scripts failing?**
- Install dependencies: `pip install -r requirements.txt --break-system-packages`
- Check Python version (3.8+)
- Verify file paths and permissions

**Data collection issues?**
- SEC EDGAR may rate-limit; add delays between requests
- Company websites vary; may need manual data entry
- Use templates as starting point

**Outdated information?**
- Battle cards need quarterly updates
- Track competitor earnings calendars
- Set reminders for major events (investor days, product launches)

## Version History

- **v1.0.0** (2025-01-13): Initial release
  - Full battle card methodology
  - 5 automation scripts
  - Templates and examples
  - SK Hynix perspective

## Support

For questions or issues:
1. Check SKILL.md for methodology details
2. Review script documentation (run with `--help`)
3. Consult Claude Code documentation
4. Open issue on GitHub repo

## License

This skill is provided as a reference implementation. Customize for your organization's needs.

---

**Created for**: Competitive intelligence professionals in memory semiconductors
**Based on**: Intel CI methodology adapted for SK Hynix context
**Typical use**: Ongoing competitor monitoring and sales enablement
