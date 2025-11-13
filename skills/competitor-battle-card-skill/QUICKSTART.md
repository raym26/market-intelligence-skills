# Quick Start: Competitor Battle Card Skill

Get your first battle card in under 5 minutes.

## Installation (2 minutes)

```bash
# 1. Copy skill to Claude Code
cp -r competitor-battle-card-skill ~/.claude/skills/competitor-battle-card-memory-semiconductors

# 2. Install dependencies
pip install pandas matplotlib plotly requests beautifulsoup4 yfinance PyPDF2 pdfplumber --break-system-packages

# 3. Verify installation
ls ~/.claude/skills/competitor-battle-card-memory-semiconductors/SKILL.md
```

## Generate Your First Battle Card (3 minutes)

### Option 1: Simple Prompt

Open Claude Code and type:
```
Create a competitor battle card for Micron from SK Hynix's perspective
```

Claude will:
1. Search for Micron's latest financial data
2. Analyze product portfolio and positioning
3. Generate comprehensive 1-2 page battle card
4. Include sales messaging and win/loss patterns

### Option 2: With Your Own Data

If you have specific documents:
```
Create a battle card for Micron using the attached 10-K and earnings transcript.
Frame it from SK Hynix's competitive perspective.
```

Then attach:
- Latest 10-K PDF
- Recent earnings call transcript
- Any internal win/loss data

## What You'll Get

A structured battle card with:

✅ Company snapshot (financials, leadership, strategy)
✅ Product portfolio (DRAM, NAND, HBM breakdown)
✅ Competitive positioning matrix
✅ Strengths & weaknesses vs. SK Hynix
✅ Sales messaging & objection handling
✅ Win/loss patterns
✅ Recent developments (last 6 months)
✅ Strategic questions for management
✅ Recommended actions by team

**Output format**: Markdown (ready for PDF export or PowerPoint)

## Common Use Cases

### For Sales Teams
```
"Update the Micron battle card with their latest HBM3E announcement"
```

### For Executives
```
"Create exec briefing on Samsung Memory's competitive position vs. SK Hynix"
```

### For Strategy
```
"Generate battle card for Micron focusing on AI/datacenter segment"
```

### For Win/Loss Analysis
```
"Update Micron battle card with recent win/loss data:
- Lost 3 HBM deals (price)
- Won 2 DDR5 server deals (performance)
- Lost 1 NAND deal (US manufacturing requirement)"
```

## Customization Examples

### Change Perspective
Default is SK Hynix → Competitor. To change:
```
"Create Micron battle card from Samsung's perspective"
```

### Focus on Specific Segment
```
"Create Micron battle card focused on HBM and AI/datacenter competition"
```

### Include More Financial Detail
```
"Create detailed Micron battle card with 5-year financial trends and margin analysis"
```

## Update Existing Battle Card

```
"Update the Micron battle card with:
- Q4 FY24 earnings results
- New HBM3E product announcement
- Win at AMD for MI300 series
- Refresh recent developments section"
```

## Automation with Python Scripts

### Scrape Latest Company Data
```bash
python scripts/scrape_company_data.py --company "Micron" --ticker "MU"
```

### Extract Financials from 10-K
```bash
python scripts/extract_financials.py --filing "MU-10K-2024.pdf"
```

### Generate Competitor Comparison
```bash
python scripts/compare_competitors.py --competitors "Micron,Samsung,SKHynix"
```

### Monitor News Updates
```bash
python scripts/track_news.py --company "Micron" --days 180
```

## Tips for Best Results

1. **Provide Context**: Mention your company perspective (e.g., "from SK Hynix's view")
2. **Include Recent Data**: Attach latest 10-K or earnings transcript if available
3. **Be Specific**: Focus on segments or topics if needed (HBM, NAND, etc.)
4. **Update Regularly**: Refresh quarterly after competitor earnings
5. **Add Internal Data**: Include win/loss feedback from sales teams
6. **Review & Refine**: Claude generates structure; you add insider context

## Troubleshooting

**"Skill not found"**
→ Check installation path: `~/.claude/skills/competitor-battle-card-memory-semiconductors/`

**"Missing dependencies"**
→ Run: `pip install -r requirements.txt --break-system-packages`

**"Outdated information"**
→ Attach latest 10-K/earnings docs or specify: "Use Micron's Q4 FY24 data"

**"Too generic"**
→ Add specifics: "Focus on HBM competition" or "Emphasize AI datacenter segment"

## Next Steps

- ✅ Generate your first battle card
- 📊 Review output and add internal insights
- 🔄 Set quarterly update reminders
- 📧 Distribute to sales/exec teams
- 📈 Track win rates before/after using battle cards

## Examples to Try

```
# Comprehensive battle card
"Create full competitor battle card for Samsung Memory vs. SK Hynix"

# Quick competitive snapshot
"Generate 1-page competitive overview of Micron for exec briefing"

# Sales-focused
"Create Micron battle card with heavy emphasis on objection handling and win/loss patterns"

# Technology-focused
"Analyze Micron's technology roadmap and positioning vs. SK Hynix in HBM and advanced DRAM"

# Market segment-focused
"Create Micron battle card focused on automotive memory segment"
```

## Learn More

- **Full Documentation**: See [README.md](README.md)
- **Methodology**: Review [SKILL.md](SKILL.md)
- **Examples**: Check [examples/](examples/) folder

---

**Time to first battle card**: ~3-5 minutes
**Time savings vs. manual**: 4-6 hours → 1 hour
**Update frequency**: Quarterly or after major events
