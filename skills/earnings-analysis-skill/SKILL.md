---
name: earnings-analysis-memory-semiconductors
description: Generate comprehensive post-earnings competitive analysis for memory semiconductor companies (Micron, SK Hynix, Samsung, etc.). Analyzes financial performance, strategic insights from earnings calls, and competitive implications. Use when tasked with earnings analysis, competitive intelligence reports, or quarterly performance assessments for memory chip manufacturers.
version: 1.0.0
---

# Post-Earnings Competitive Analysis for Memory Semiconductors

## Overview

This skill enables Claude to generate comprehensive, executive-ready post-earnings analysis reports for memory semiconductor companies. Originally designed for Intel competitive intelligence tracking of Qualcomm, adapted for SK Hynix competitive analysis of Micron (and other memory competitors).

The output is a concise (max 2 pages), insights-driven email communique distributed to executives, business unit leaders, and peer analysts across the organization.

## When to Use This Skill

Invoke this skill when:
- Analyzing earnings calls for Micron, SK Hynix, Samsung Memory, Western Digital, Kioxia
- Creating quarterly competitive intelligence reports
- Synthesizing financial performance and strategic implications
- User requests "earnings analysis", "post-earnings report", or "quarterly performance review"

## Core Deliverable Structure

The analysis follows this exact structure (max 2 pages excluding transcript):

### 1. Subject Line
Format: `[Company] Q[X] FY[YY] Earnings Analysis - [Date]`
Example: `Micron Q2 FY25 Earnings Analysis - March 27, 2025`

### 2. Executive Summary
- 2-3 sentence bottom-line assessment
- Focus on: headline numbers, surprise vs. expectations, strategic direction

### 3. Key Highlights
- 4-6 critical bullet points
- Mix of financial and strategic highlights
- Flag both positive and negative developments

### 4. Financial Performance (Tabular Format)
Present key metrics in tables showing trends over time (minimum 4 quarters):

**Required Metrics:**
- Total Revenue ($ in billions, YoY%, QoQ%)
- Segment Revenue (DRAM, NAND, Emerging Memory)
- Gross Margin %
- Operating Margin %
- Bit Shipments (if disclosed)
- Average Selling Price (ASP)
- CapEx ($ in billions)
- Capacity Plans (wafer starts, fab investments)
- Guidance (revenue range, margin outlook)

**Bonus Visualization:**
- Sankey diagram showing revenue flow from segments to end markets (AI/Datacenter, Mobile, Enterprise, PC, Automotive)

### 5. Strategic Insights from Analyst Q&A
Extract and synthesize qualitative signals:

**Look for:**
- Management tone and confidence level
- Customer demand signals (hyperscaler orders, enterprise buying patterns, mobile demand)
- Technology roadmap updates (process node transitions, HBM generations, DDR5/DDR6, etc.)
- Pricing environment commentary (ASP trends, contract negotiations, spot market)
- Inventory levels and channel health (weeks of inventory, destocking/restocking)
- Competitive positioning (vs. Samsung, SK Hynix; technology leadership claims)
- Forward-looking statements about AI/HBM demand, data center buildout, etc.

**Signal Detection:**
- 🟢 Positive signals: Accelerating demand, pricing power, technology leadership, capacity expansion
- 🔴 Negative signals: Softening demand, pricing pressure, technology delays, inventory buildup
- ⚠️ Mixed/Watch signals: Cautious guidance, geopolitical concerns, customer concentration

### 6. So What for SK Hynix (Competitive Implications)
Translate findings into strategic implications:

**Framework:**
- **Market Conditions**: What does Micron's performance signal about overall memory market health?
- **Competitive Threats**: Where is Micron gaining advantage? (e.g., HBM market share, DRAM technology, customer wins)
- **Competitive Opportunities**: Where is Micron vulnerable? (margins, capacity constraints, technology gaps)
- **Technology Positioning**: Relative technology advancement (process nodes, product portfolio)
- **Strategic Implications**: What should SK Hynix consider for roadmap/strategy?
- **Pricing & Demand Trends**: How do pricing/demand dynamics affect SK Hynix outlook?

### 7. Recommended Actions (If Applicable)
- Concrete next steps for stakeholders
- Areas requiring deeper investigation
- Strategic decisions to revisit

### 8. Appendix: Full Transcript
- Attach complete earnings call transcript
- Note: This is excluded from 2-page limit

## Data Collection Process

### Primary Sources
1. **AlphaSense**: Preferred source for transcripts and financial data
   - Search: "[Company] earnings call Q[X] FY[YY]"
   - Download transcript and earnings presentation

2. **Free Fallback Sources**:
   - Company Investor Relations website
   - Seeking Alpha (free transcripts, often available immediately post-call)
   - SEC EDGAR (10-Q, 10-K for detailed financials)

3. **Live Call**:
   - Listen live when possible for management tone
   - Note emphasis, hesitation, confidence in voice
   - Take real-time notes on surprising statements

### Financial Data Extraction
Use Python scripts (see `scripts/` folder) to:
1. Extract tables from earnings presentation PDFs
2. Pull historical data from prior quarters for trend analysis
3. Compare actuals vs. guidance from prior quarter
4. Generate visualizations (revenue trends, margin analysis, Sankey diagram)

## Analysis Methodology

### Step 1: Quick First Pass (15 minutes)
- Scan earnings presentation for headline numbers
- Read prepared remarks summary
- Identify surprises vs. Street expectations

### Step 2: Deep Financial Analysis (30 minutes)
- Build comparison tables (actual vs. guidance, vs. prior quarter, YoY)
- Calculate key ratios and trends
- Identify inflection points in margins, ASPs, or volumes

### Step 3: Transcript Analysis (45 minutes)
- Read full Q&A section
- Tag comments by theme (demand, pricing, technology, competition, outlook)
- Extract direct quotes for key insights
- Note what was NOT discussed (often revealing)

### Step 4: Competitive Framing (30 minutes)
- Compare to SK Hynix's most recent results
- Identify relative strengths/weaknesses
- Frame strategic implications
- Draft "So What" section

### Step 5: Synthesis & Writing (30 minutes)
- Draft executive summary (start with conclusion)
- Organize insights by priority
- Ensure max 2 pages
- Proofread for clarity and impact

## Key Memory Semiconductor Context

### Technology Landscape
- **DRAM**: DDR4, DDR5 (mainstream), DDR6 (emerging), HBM2e, HBM3, HBM3E (AI/datacenter)
- **NAND**: TLC, QLC, PLC (emerging), 3D NAND layers (176L, 232L, 300L+)
- **Process Nodes**: 1α, 1β, 1γ (nm-class DRAM generations)
- **Emerging**: CXL memory, MRAM, PCM

### Market Segments
- **AI/Datacenter**: Highest growth, HBM-driven, premium pricing
- **Mobile**: Largest volume, price-sensitive, LPDDR standards
- **Enterprise**: Server DRAM/SSD, stable demand
- **PC**: Cyclical, DDR4→DDR5 transition
- **Automotive**: Growing, reliability-critical

### Competitive Dynamics
- **Big 3 Memory**: Samsung (leader), SK Hynix, Micron
- **HBM Leadership**: SK Hynix (first mover), Samsung (capacity), Micron (catching up)
- **NAND Competition**: +Kioxia, Western Digital, YMTC (China)

### Key Performance Indicators
- **Bit Growth**: Industry typically +20-40% annually (supply)
- **ASP Trends**: Cyclical, correlated with supply/demand balance
- **Margin Cycles**: Memory is highly cyclical (boom/bust)
- **CapEx Intensity**: 30-40% of revenue in growth phases

## Python Automation Scripts

The skill includes Python scripts in the `scripts/` directory:

1. **`scrape_transcript.py`**: Scrape earnings transcript from free sources
2. **`extract_financials.py`**: Extract tables from earnings PDF using PyPDF2/tabula
3. **`compare_quarters.py`**: Generate comparison tables with historical data
4. **`visualize_trends.py`**: Create revenue/margin trend charts
5. **`sankey_revenue.py`**: Generate Sankey diagram for revenue flow

Scripts use standard libraries: `requests`, `beautifulsoup4`, `pandas`, `matplotlib`, `plotly`, `PyPDF2`, `tabula-py`

## Tips for Excellence

1. **Lead with Insight**: Executives care about "so what", not just numbers
2. **Signal Detection**: Flag leading indicators (orders, backlog, customer commentary)
3. **Be Concise**: Every sentence should add value
4. **Quantify**: Use numbers to support qualitative claims
5. **Compare**: Always contextualize (vs. expectations, vs. prior quarter, vs. competition)
6. **Voice Matters**: Management tone reveals confidence/concern
7. **Watch for Omissions**: What they DON'T discuss is often revealing
8. **Speed Matters**: Deliver within 24 hours of earnings call
9. **Accuracy Critical**: Executives will act on this; fact-check everything
10. **Forward-Looking**: Focus on implications for future, not just past performance

## Example Analysis Triggers

When user says:
- "Analyze Micron's latest earnings"
- "Create post-earnings report for [memory company]"
- "What were the key takeaways from [company] earnings call?"
- "Generate competitive intelligence on [company] Q[X] results"
- "Summarize [company] earnings for executive team"

→ Invoke this skill and follow the structure above.

## Output Format

Generate the email report in Markdown format, with:
- Clear section headers
- Tables in markdown format
- Bullet points for highlights/insights
- Bold for emphasis on key numbers/insights
- Professional, concise business writing tone

The report should be ready to copy into an email and send immediately.
