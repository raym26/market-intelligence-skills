# Market Intelligence Skills

Claude Code Skills for automating market intelligence and competitive analysis workflows.

## Available Skills

### earnings-analysis-skill

Automates post-earnings competitive intelligence for memory semiconductor companies.

**Features:**
- Financial performance analysis with historical trends
- Strategic insights from analyst Q&A with signal detection
- Competitive implications framework
- Python automation scripts

**Time Saved:** 2-3 hours → 30 minutes per analysis

See [skills/earnings-analysis-skill/](skills/earnings-analysis-skill/) for details.

### competitor-battle-card-skill

Generates comprehensive competitor battle cards for memory semiconductor companies.

**Features:**
- Company snapshot with financials and leadership
- Product portfolio analysis (DRAM, NAND, HBM)
- Competitive positioning matrix
- Strengths/weaknesses assessment
- Sales messaging and objection handling
- Win/loss patterns and strategic recommendations
- Python automation scripts

**Time Saved:** 4-6 hours → 1 hour per battle card

See [skills/competitor-battle-card-skill/](skills/competitor-battle-card-skill/) for details.

## Installation

```bash
# Clone the repo
git clone https://github.com/raym26/market-intelligence-skills.git
cd market-intelligence-skills

# Install earnings-analysis-skill
cp -r skills/earnings-analysis-skill ~/.claude/skills/earnings-analysis-memory-semiconductors
pip install -r skills/earnings-analysis-skill/requirements.txt --break-system-packages

# Install competitor-battle-card-skill
cp -r skills/competitor-battle-card-skill ~/.claude/skills/competitor-battle-card-memory-semiconductors
pip install -r skills/competitor-battle-card-skill/requirements.txt --break-system-packages
```

## Usage

**Earnings Analysis:**
```
claude
"Analyze Micron Q2 FY25 earnings"
```

**Battle Cards:**
```
claude
"Create a battle card for Micron from SK Hynix's perspective"
```
## Prerequisites

- Claude Code installed ([download here](https://www.anthropic.com/claude-code))
- Claude Pro, Team, or Enterprise subscription (Skills not available on free tier)
- Python 3.8+ (for automation scripts)

## Security

These skills include Python scripts for automation. Always review code before running:
- **earnings-analysis-skill**: `scrape_transcript.py`, `extract_financials.py`, etc.
- **competitor-battle-card-skill**: `scrape_company_data.py`, `extract_financials.py`, etc.

## Vision

Building toward autonomous market intelligence - starting with proven methodologies, scaling to full "hireable" MI analyst capability.
