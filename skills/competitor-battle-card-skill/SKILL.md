---
name: competitor-battle-card-memory-semiconductors
description: Generate comprehensive competitor battle cards for memory semiconductor companies (Micron, Samsung, SK Hynix, etc.). Creates 1-2 page profiles with company snapshot, product portfolio, competitive positioning, strengths/weaknesses, and win/loss patterns. Use for sales enablement, exec briefings, or competitive strategy planning.
version: 1.0.0
---

# Competitor Battle Card for Memory Semiconductors

## Overview

This skill enables Claude to generate executive-ready competitor battle cards for memory semiconductor companies. Originally designed for Intel competitive intelligence, adapted for SK Hynix competitive analysis of key rivals (Micron, Samsung, and emerging players).

The output is a concise (1-2 pages) battle card profile designed for sales teams, executive briefings, and strategic planning. Battle cards are living documents updated quarterly or when significant competitive developments occur.

## When to Use This Skill

Invoke this skill when:
- Creating or refreshing competitor profiles for sales enablement
- Preparing executive briefings on key competitors
- User requests "battle card", "competitor profile", or "competitive analysis"
- New competitive intelligence requires updating existing battle cards
- Strategic planning requires deep competitor assessment
- Win/loss analysis reveals need for competitive positioning updates

## Core Deliverable Structure

The battle card follows this exact structure (max 2 pages):

### 1. Header
```
COMPETITOR BATTLE CARD: [Company Name]
Last Updated: [Date] | Prepared for: SK Hynix [Team/Function]
Analyst: [Name] | Next Review: [Quarterly Date]
```

### 2. Company Snapshot (Quick Reference)
Present key facts in a scannable format:

**Company Basics:**
- **Headquarters**: Location
- **Founded**: Year
- **CEO/Leadership**: Key executives (CEO, CFO, relevant BU leaders)
- **Public/Private**: Ticker symbol if public
- **Employees**: Headcount (approximate)

**Financial Overview (Latest Fiscal Year):**
- **Total Revenue**: $ in billions, YoY% growth
- **Memory Revenue**: DRAM vs. NAND split ($ and %)
- **Gross Margin**: % (trend: improving/declining/stable)
- **Operating Margin**: %
- **R&D Spending**: $ and % of revenue
- **CapEx**: $ in billions
- **Market Cap**: $ (if public)

**Strategic Focus:**
- 1-2 sentence summary of company's current strategic priorities
- Example: "Doubling down on HBM for AI datacenter; reducing NAND exposure"

### 3. Product Portfolio
Organize by memory type and market segment:

**DRAM Products:**
- **DDR4/DDR5 (PC/Server)**: Nodes, competitive position, key customers
- **LPDDR (Mobile)**: Generations, density range, design wins
- **HBM (AI/Datacenter)**: HBM2e/HBM3/HBM3E status, capacity, customers (NVIDIA, AMD, etc.)
- **Automotive**: AEC-Q100 qualified products, partnerships

**NAND Products:**
- **Enterprise SSD**: PCIe Gen4/Gen5, capacities, customers
- **Client SSD**: Performance/mainstream segments
- **Mobile NAND**: UFS generations, eMMC
- **3D NAND Technology**: Layer count (e.g., 232L), node roadmap

**Emerging/Other:**
- CXL memory, MRAM, PCM, or other next-gen technologies
- Note: Only include if material to competitive positioning

### 4. Competitive Positioning Matrix

Present relative positioning vs. SK Hynix across key dimensions:

| Dimension | Micron Position | SK Hynix Position | Gap Analysis |
|-----------|----------------|-------------------|--------------|
| **HBM Technology** | HBM3 ramping, HBM3E in dev | HBM3E in production | SK Hynix leads by 1 gen |
| **HBM Capacity** | Limited, ramping 2025-26 | High, NVIDIA primary supplier | SK Hynix 60% share vs. 10% |
| **DDR5 Adoption** | Strong in server | Strong in server/mobile | Parity |
| **NAND Layers** | 232L in production | 238L in production | Near parity |
| **Manufacturing Cost** | Higher (older fabs) | Lower (newer Korea fabs) | SK Hynix advantage |
| **Customer Concentration** | Diversified | NVIDIA-heavy in HBM | Risk/opportunity trade-off |

### 5. Strengths (What Makes Them Dangerous)

List 4-6 key competitive strengths from SK Hynix's perspective:

**Example Structure:**
- 🟢 **Geographic Diversification**: Only Big 3 memory company with significant US manufacturing (Idaho). Reduces geopolitical risk and qualifies for US CHIPS Act subsidies.
- 🟢 **Integrated Portfolio**: Both DRAM and NAND at scale. Can offer bundled solutions to hyperscalers (Amazon, Google, Microsoft).
- 🟢 **Technology Execution**: Successfully transitioned to 1β DRAM and 232L NAND on schedule. No major delays in recent roadmap.
- 🟢 **Management Stability**: CEO Sanjay Mehrotra (since 2017) with consistent strategy. Low exec turnover.

**Categories to Consider:**
- Technology leadership or fast-follower execution
- Manufacturing footprint and cost structure
- Customer relationships and design wins
- Financial resources and investment capacity
- Management team and strategic clarity
- Product portfolio breadth
- Supply chain resilience

### 6. Weaknesses (Where They're Vulnerable)

List 4-6 key vulnerabilities SK Hynix can exploit:

**Example Structure:**
- 🔴 **HBM Lag**: Late to HBM market. HBM3 only ramping in 2025 while SK Hynix ships HBM3E at volume. Missed NVIDIA AI boom initial wave.
- 🔴 **Margin Pressure**: Gross margins 5-10 points below Samsung/SK Hynix due to older fab base. Limits pricing flexibility.
- 🔴 **Technology Transition Risk**: Historically slower to new nodes vs. Samsung. 1α DRAM transition lagged by 2-3 quarters.
- 🔴 **NAND Competition**: Faces intense competition from 5+ NAND suppliers. Weaker pricing power than DRAM duopoly.

**Categories to Consider:**
- Technology gaps or delays
- Cost structure disadvantages
- Customer concentration risks
- Product portfolio gaps
- Financial constraints
- Management/execution issues
- Manufacturing limitations

### 7. Key Differentiators (SK Hynix vs. Competitor)

What makes SK Hynix better positioned? (3-5 points)

**Example:**
1. **HBM Leadership**: SK Hynix pioneered HBM and holds 60%+ market share. NVIDIA's primary supplier for H100/H200/B100 GPUs. Micron playing catch-up.
2. **Technology Cadence**: SK Hynix ships new HBM generations 6-12 months ahead of Micron. HBM3E already in production vs. Micron's development phase.
3. **AI Positioning**: SK Hynix seen as "AI memory leader" by customers. Brand association with NVIDIA Blackwell platform.
4. **Manufacturing Efficiency**: Newer fabs in Korea (M16 in Yongin) deliver 15-20% cost advantage vs. Micron's Idaho operations.

### 8. How to Compete (Sales Messaging & Objection Handling)

Provide actionable guidance for sales teams:

**When Micron Says...** (Common Objections)
1. **"We offer both DRAM and NAND - one-stop shop"**
   - **Counter**: "SK Hynix also offers complete memory solutions, but with technology leadership in HBM where it matters most for AI workloads. Our HBM3E is shipping today while theirs is still ramping."

2. **"We have US manufacturing for supply security"**
   - **Counter**: "SK Hynix is investing $15B in Indiana for HBM packaging (announced 2024). We combine Korean fab efficiency with US final assembly. Best of both worlds."

3. **"Our NAND pricing is more competitive"**
   - **Counter**: "True for commodity NAND, but for high-performance PCIe Gen5 enterprise SSDs, SK Hynix's 238L technology offers better performance-per-watt. Total cost of ownership favors SK Hynix in datacenter."

**Our Winning Messages:**
- Lead with HBM leadership and AI positioning
- Emphasize technology generation advantage
- Highlight NVIDIA partnership and AI credibility
- Focus on performance leadership, not price
- Leverage speed-to-market on new nodes

### 9. Win/Loss Patterns

Analyze where SK Hynix typically wins or loses against this competitor:

**Where SK Hynix Wins:**
- ✅ **AI/Datacenter HBM deals**: 80%+ win rate. SK Hynix HBM leadership is decisive.
- ✅ **Performance-critical server DRAM**: Strong win rate in high-density DDR5 RDIMMs for enterprise.
- ✅ **Early adopter customers**: Customers prioritizing latest technology choose SK Hynix.

**Where SK Hynix Loses:**
- ❌ **Commodity NAND**: Micron often wins on price in client SSD and mobile NAND.
- ❌ **US government/defense**: Micron's US manufacturing is preferred for security-sensitive applications.
- ❌ **Price-sensitive mobile LPDDR**: Micron sometimes undercuts on LPDDR4/5 for smartphones.

**Key Decision Factors:**
- Technology generation (favors SK Hynix in DRAM/HBM)
- Price (often favors Micron in NAND)
- Supply security (Micron emphasizes US manufacturing)
- Customer relationship history
- Total solution bundling (both can play)

### 10. Recent Developments (Last 6 Months)

Track significant competitive events:

**Strategic Announcements:**
- [Date]: Micron announced $15B Idaho fab expansion for 1γ DRAM
- [Date]: Secured $6.1B in US CHIPS Act funding
- [Date]: Launched HBM3E samples to customers (SK Hynix note: 12 months behind us)

**Product Launches:**
- [Date]: 232L NAND in mass production
- [Date]: DDR5 RDIMM for Intel Xeon 6
- [Date]: HBM3 shipping to customer (rumored AMD MI300)

**Financial/Business:**
- Q[X] FY25: Revenue up 25% YoY on memory recovery
- [Date]: Announced 10% workforce reduction
- [Date]: Increased CapEx guidance to $8B for 2025

**Customer Wins/Losses:**
- [Date]: Won server DRAM socket at AWS (source: industry rumor)
- [Date]: Lost HBM qualification at NVIDIA Blackwell (confirmed SK Hynix win)

### 11. Key Strategic Questions for Senior Management

Frame critical questions for SK Hynix leadership:

1. **HBM Capacity**: Micron ramping HBM production 2025-26. Will they pressure HBM pricing? Should we accelerate M16 capacity expansion?

2. **US Manufacturing**: Micron's US fab advantage secures CHIPS Act funding and defense/gov deals. Should SK Hynix accelerate Indiana packaging facility?

3. **NAND Strategy**: Micron remains committed to NAND despite low margins. Do we continue NAND investment or focus exclusively on DRAM/HBM?

4. **Technology Roadmap**: Can we maintain 6-12 month HBM technology lead through HBM4 generation? What investments are required?

5. **Customer Concentration**: SK Hynix heavily exposed to NVIDIA HBM. Micron's diversified customer base is less risky. Should we diversify?

6. **China Exposure**: Both companies face China risks. Micron banned from some Chinese customers. Does this create opportunity or precedent for retaliation against SK Hynix?

### 12. Recommended Actions (For SK Hynix Teams)

Concrete next steps organized by function:

**For Sales:**
- Lead all customer engagements with HBM leadership story
- Pre-empt Micron's "US manufacturing" message with Indiana packaging announcement
- Focus on AI/datacenter accounts where technology matters more than price

**For Product/Engineering:**
- Accelerate HBM4 roadmap to maintain 12-month lead
- Benchmark Micron's 1γ DRAM and 232L NAND; identify technology gaps
- Monitor Micron's HBM3E specs vs. our HBM3E to ensure performance leadership

**For Strategy:**
- Quarterly review of Micron capacity additions (DRAM/NAND/HBM)
- Track US CHIPS Act funding to Micron; model impact on their cost structure
- Win/loss analysis: Why did we lose recent NAND deals? Acceptable or needs response?

**For Competitive Intelligence:**
- Monitor Micron earnings calls for HBM roadmap updates
- Track Micron customer announcements (especially NVIDIA, AMD, Intel)
- Update this battle card within 48 hours of major Micron announcements

## Data Collection Process

### Primary Sources

1. **Company Investor Relations**:
   - Most recent 10-K/10-Q filings (SEC EDGAR)
   - Latest earnings call transcript and presentation
   - Investor day presentations (annually or bi-annually)

2. **Public Filings & Disclosures**:
   - SEC Form 8-K for material events
   - Patent filings (USPTO, WIPO) for technology roadmap
   - Government subsidy announcements (CHIPS Act, etc.)

3. **Industry Sources**:
   - TrendForce, Gartner, IDC reports on memory market
   - AnandTech, Tom's Hardware product reviews and teardowns
   - EE Times, Semiconductor Engineering for technology news

4. **Customer Announcements**:
   - NVIDIA, AMD, Intel product launches mentioning memory suppliers
   - Cloud provider (AWS, Azure, GCP) infrastructure announcements
   - OEM (Dell, HP, Lenovo) server/PC product specs

5. **Win/Loss Intelligence**:
   - Internal SK Hynix sales team feedback
   - Customer debriefs on competitive evaluations
   - Channel partner intelligence

### Python Automation Scripts

Use scripts in `scripts/` folder:

1. **`scrape_company_data.py`**: Scrape company website, IR site, press releases
2. **`extract_financials.py`**: Pull financials from 10-K/10-Q PDFs
3. **`compare_competitors.py`**: Generate side-by-side comparison tables
4. **`visualize_positioning.py`**: Create competitive positioning charts
5. **`track_news.py`**: Monitor news feeds for competitor updates

## Analysis Methodology

### Step 1: Financial & Strategic Baseline (45 min)
- Read most recent 10-K and earnings presentation
- Extract key financial metrics (revenue, margins, CapEx, R&D)
- Identify strategic priorities from CEO letter and earnings calls

### Step 2: Product Portfolio Assessment (1 hour)
- Catalog DRAM/NAND/HBM product lines
- Map products to market segments (AI, datacenter, mobile, PC, auto)
- Identify technology generations and roadmap
- Compare to SK Hynix portfolio for gaps/overlaps

### Step 3: Competitive Positioning Analysis (1 hour)
- Build dimension-by-dimension comparison vs. SK Hynix
- Identify relative strengths and weaknesses
- Determine key differentiators

### Step 4: Win/Loss & Customer Intelligence (45 min)
- Review internal sales feedback on recent deals
- Analyze customer announcements and design wins
- Identify patterns in wins vs. losses

### Step 5: Strategic Framing (30 min)
- Draft sales messaging and objection handling
- Formulate strategic questions for management
- Define recommended actions by team

### Step 6: Synthesis & Writing (1 hour)
- Organize into battle card structure
- Ensure 1-2 page length (dense but scannable)
- Add recent developments from last 6 months
- Proofread for accuracy and clarity

## Key Memory Semiconductor Context

### Technology Landscape
- **DRAM Nodes**: 1α (~18nm), 1β (~16nm), 1γ (~14nm), 1δ (future)
- **HBM Generations**: HBM2e (2020-22), HBM3 (2022-24), HBM3E (2024-25), HBM4 (2026+)
- **DDR Standards**: DDR4 (mature), DDR5 (ramping), DDR6 (development)
- **NAND Layers**: 128L (old), 176L (mature), 232L (current), 300L+ (future)

### Market Dynamics
- **Big 3 Oligopoly**: Samsung (35-40% DRAM/NAND), SK Hynix (30% DRAM, 20% NAND), Micron (20-25% DRAM, 15% NAND)
- **HBM Duopoly**: SK Hynix (60%+), Samsung (30%+), Micron (entering)
- **Pricing**: Cyclical, driven by supply/demand balance
- **CapEx**: Counter-cyclical (invest in downturns for next upcycle)

### Competitive Benchmarking Dimensions
- **Technology Leadership**: Who ships new nodes first
- **Manufacturing Cost**: $/bit, influenced by node, utilization, location
- **HBM Market Share**: Critical for AI era positioning
- **Customer Relationships**: Design-in cycles are 1-2 years
- **Financial Strength**: Balance sheet to survive downturns

## Output Format

Generate the battle card in Markdown format, with:
- Clear section headers (use ## and ###)
- Tables for financial data and competitive comparisons
- Bullet points for strengths, weaknesses, differentiators
- 🟢 🔴 ✅ ❌ emoji for visual scanning (strengths/weaknesses/wins/losses)
- Bold for key facts and numbers
- Professional but direct tone (sales/exec audience)

The battle card should be ready to print as PDF or copy into PowerPoint slides.

## Battle Card Lifecycle

**Creation**: When new competitor emerges or major strategic shift occurs

**Updates**:
- Quarterly refresh after competitor's earnings call
- Within 48 hours of major announcements (M&A, product launch, exec change)
- After win/loss reviews reveal new patterns

**Distribution**:
- Sales teams (for customer engagements)
- Executive briefings (board meetings, strategy reviews)
- Product teams (roadmap planning)
- Marketing (messaging and positioning)

**Archive**:
- Keep prior versions in git history
- Tag with date and version for reference

## Tips for Excellence

1. **Be Specific**: "HBM3E vs. HBM3" is better than "advanced memory"
2. **Quantify Everything**: Use numbers to support claims
3. **Avoid Bias**: Acknowledge competitor strengths honestly
4. **Focus on Actionability**: Sales teams need "what to say" not just "what to know"
5. **Update Regularly**: Stale battle cards are worse than none
6. **Cite Sources**: Add footnotes for key claims
7. **Keep It Scannable**: Execs will skim; make key points jump out
8. **Forward-Looking**: Focus on competitive threats/opportunities ahead
9. **Internal Honesty**: Call out where SK Hynix is behind; hiding gaps helps no one
10. **Customer Perspective**: Frame through "why would customer choose X over Y"

## Example Triggers

When user says:
- "Create battle card for Micron"
- "Update competitor profile for Samsung Memory"
- "Generate competitive analysis of [memory company]"
- "Prepare exec briefing on [competitor]"
- "Build sales enablement on [competitor]"

→ Invoke this skill and follow the structure above.
