# Quick Start Guide

Get up and running with the earnings analysis skill in 5 minutes.

## 1. Install the Skill

**Option A: Project-specific** (recommended for teams)
```bash
# In your project directory
mkdir -p .claude/skills
cp -r earnings-analysis-skill .claude/skills/earnings-analysis-memory-semiconductors
```

**Option B: User-wide** (available across all projects)
```bash
# System-wide installation
mkdir -p ~/.claude/skills
cp -r earnings-analysis-skill ~/.claude/skills/earnings-analysis-memory-semiconductors
```

## 2. Install Python Dependencies

```bash
pip install pandas matplotlib plotly requests beautifulsoup4 tabula-py PyPDF2 --break-system-packages
```

Or use the requirements file:
```bash
pip install -r earnings-analysis-skill/requirements.txt --break-system-packages
```

## 3. Test the Skill

Start Claude Code and ask:
```
"Help me create a Micron earnings analysis report"
```

Claude should automatically invoke the skill and ask you for:
- Earnings transcript
- Financial data
- Historical comparison data

## 4. Generate Template Data

Create sample data files to get started:

```bash
# Historical quarterly data template
python earnings-analysis-skill/scripts/compare_quarters.py --create-template

# Revenue flow data template  
python earnings-analysis-skill/scripts/sankey_revenue.py --create-template
```

Edit these CSV files with your actual data.

## 5. Run Your First Analysis

```
"Analyze Micron Q2 FY25 earnings. Here's the transcript: [paste or upload]
Use historical data from historical_data_template.csv"
```

Claude will:
1. Parse the transcript
2. Extract key financial metrics
3. Generate comparison tables
4. Create visualizations
5. Write the analysis report
6. Apply SK Hynix competitive framing

## Common Commands

**Generate full analysis:**
```
"Generate post-earnings analysis for [Company] [Quarter] with competitive implications for SK Hynix"
```

**Just financial tables:**
```
"Create quarterly comparison tables for the last 4 quarters"
```

**Just visualizations:**
```
"Generate revenue trend and margin analysis charts"
```

**Scrape transcript:**
```bash
python scripts/scrape_transcript.py --company "Micron" --ticker "MU" --quarter "Q2" --year "2025"
```

## File Structure

```
earnings-analysis-skill/
├── SKILL.md                          # Main skill instructions (Claude reads this)
├── README.md                         # Full documentation
├── QUICKSTART.md                     # This file
├── requirements.txt                  # Python dependencies
├── scripts/
│   ├── scrape_transcript.py          # Get earnings transcripts
│   ├── extract_financials.py         # Parse earnings PDFs
│   ├── compare_quarters.py           # Generate comparison tables
│   ├── visualize_trends.py           # Create charts
│   └── sankey_revenue.py             # Revenue flow diagrams
└── examples/
    └── example_report.md             # Sample output
```

## Troubleshooting

**"Skill not found"**
- Check folder name matches: `earnings-analysis-memory-semiconductors`
- Verify it's in `.claude/skills/` or `~/.claude/skills/`
- Restart Claude Code

**"Module not found"**
- Install dependencies: `pip install -r requirements.txt --break-system-packages`
- Check Python version: `python --version` (need 3.8+)

**"Can't find transcript"**
- Download manually from Seeking Alpha or company IR site
- Use `scripts/scrape_transcript.py` for automation
- Or paste transcript text directly to Claude

## Next Steps

1. Review `examples/example_report.md` to see expected output
2. Customize SKILL.md for your company's context (change SK Hynix references)
3. Build historical data CSV with past quarters
4. Run a test analysis on recent earnings

## Need Help?

- Full docs: See `README.md`
- Script help: Run any script with `--help` flag
- Example: `python scripts/compare_quarters.py --help`

---

**Ready to analyze earnings like a pro!** 🚀
