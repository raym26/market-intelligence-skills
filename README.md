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

## Installation
```bash
# Install the skill
cp -r skills/earnings-analysis-skill ~/.claude/skills/earnings-analysis-memory-semiconductors

# Install dependencies
pip install -r skills/earnings-analysis-skill/requirements.txt --break-system-packages
```

## Usage
```
claude
"Analyze Micron earnings"
```

## Vision

Building toward autonomous market intelligence - starting with proven methodologies, scaling to full "hireable" MI analyst capability.
