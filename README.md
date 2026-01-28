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

### sankey-revenue-flow-skill

Creates interactive Sankey diagrams visualizing revenue flows for memory semiconductor companies.

**Features:**
- Revenue flow visualization (Total → Segments → End Markets)
- Side-by-side company comparisons
- Normalized percentage views for easy comparison
- Company-branded color schemes (Micron, SK Hynix, Samsung, WD, Kioxia)
- Interactive HTML + static PNG/SVG export
- Automatic data extraction from earnings materials

**Time Saved:** 1-2 hours → 15 minutes per diagram

See [skills/sankey-revenue-flow-skill/](skills/sankey-revenue-flow-skill/) for details.

### last30days-skill

Researches topics from the past 30 days across Reddit, X, and the web to stay current between earnings cycles.

**Third-party skill by [@mvanhorn](https://github.com/mvanhorn)** | [Original repo](https://github.com/mvanhorn/last30days-skill)

**Features:**
- Reddit and X (Twitter) research with engagement metrics
- Web search fallback (works without API keys)
- Quick mode (8-12 sources) or Deep mode (50-70 sources)
- Synthesizes community discussions and news
- Custom examples for memory semiconductor intelligence

**Use Cases:** Track company news, technology trends, market dynamics, competitive moves between earnings

See [skills/last30days-skill/](skills/last30days-skill/) and [MEMORY_SEMICONDUCTOR_EXAMPLES.md](skills/last30days-skill/MEMORY_SEMICONDUCTOR_EXAMPLES.md) for details.

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

# Install sankey-revenue-flow-skill
cp -r skills/sankey-revenue-flow-skill ~/.claude/skills/sankey-revenue-flow-memory-semiconductors
pip install -r skills/sankey-revenue-flow-skill/requirements.txt --break-system-packages

# Install last30days-skill
cp -r skills/last30days-skill ~/.claude/skills/last30days
# Optional: Configure API keys for full functionality
mkdir -p ~/.config/last30days
# Add OPENAI_API_KEY and XAI_API_KEY to ~/.config/last30days/.env
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

**Revenue Flow Visualization:**
```
claude
"Create a Sankey diagram showing Micron's revenue flow"
"Compare Micron vs SK Hynix revenue composition side-by-side"
```

**Market Intelligence Updates:**
```
claude
"/last30days Micron HBM developments"
"/last30days memory chip pricing trends --deep"
```
## Prerequisites

- Claude Code installed ([download here](https://www.anthropic.com/claude-code))
- Claude Pro, Team, or Enterprise subscription (Skills not available on free tier)
- Python 3.8+ (for automation scripts)

## Security

These skills include Python scripts for automation. Always review code before running:
- **earnings-analysis-skill**: `scrape_transcript.py`, `extract_financials.py`, etc.
- **competitor-battle-card-skill**: `scrape_company_data.py`, `extract_financials.py`, etc.
- **sankey-revenue-flow-skill**: `sankey_generator.py`, `compare_companies.py`, `extract_revenue_data.py`
- **last30days-skill**: `last30days.py` and lib modules (third-party skill from [@mvanhorn](https://github.com/mvanhorn/last30days-skill))

## Vision

Building toward autonomous market intelligence - starting with proven methodologies, scaling to full "hireable" MI analyst capability.
