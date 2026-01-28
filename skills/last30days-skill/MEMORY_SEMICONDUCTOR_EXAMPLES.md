# Memory Semiconductor Use Cases for /last30days

> **Note:** /last30days is a third-party skill created by [@mvanhorn](https://github.com/mvanhorn/last30days-skill). This document provides memory semiconductor-specific examples and integration guidance.

This skill is particularly useful for staying current on memory semiconductor market developments between earnings cycles.

## Typical Use Cases

### Company News & Developments
Track recent news and discussions about memory chip manufacturers:
```
/last30days Micron Technology news
/last30days SK Hynix HBM developments
/last30days Samsung memory business updates
/last30days Western Digital NAND news
```

### Technology & Product Trends
Monitor emerging technologies and product announcements:
```
/last30days HBM3E adoption
/last30days DDR5 market trends
/last30days CXL memory technology
/last30days NAND flash capacity increases
```

### Market Intelligence
Gather insights on industry dynamics and competitive positioning:
```
/last30days memory chip supply constraints
/last30days DRAM pricing trends
/last30days AI server memory demand
/last30days memory semiconductor capacity expansion
```

### Customer & End Market Trends
Understand demand drivers and customer behavior:
```
/last30days AI datacenter memory requirements
/last30days smartphone DRAM trends
/last30days automotive memory adoption
/last30days enterprise SSD demand
```

### Competitive Analysis
Track competitor moves and strategic shifts:
```
/last30days Micron vs SK Hynix HBM
/last30days memory manufacturer market share
/last30days NAND fab capacity announcements
/last30days memory chip manufacturing investments
```

## Integration with Other Skills

**Combine with earnings-analysis:**
1. Run earnings analysis for quarterly results
2. Use /last30days to catch up on developments since the quarter ended
3. Identify trends that may impact next quarter

**Combine with battle-cards:**
1. Generate competitor battle card
2. Use /last30days to add recent competitive moves
3. Update battle card with latest positioning

**Combine with sankey-revenue:**
1. Generate revenue flow diagram
2. Use /last30days to research market trends by segment
3. Validate or adjust end market allocations

## Command Options

**Quick research** (8-12 sources, faster):
```
/last30days Micron HBM news --quick
```

**Deep research** (50-70 sources, comprehensive):
```
/last30days memory chip industry trends --deep
```

**Reddit-only** (community discussions):
```
/last30days semiconductor stocks --sources=reddit
```

**X-only** (real-time updates):
```
/last30days Micron earnings --sources=x
```

## Setup Requirements

Configure API keys for full functionality:
```bash
mkdir -p ~/.config/last30days
cat > ~/.config/last30days/.env << 'EOF'
OPENAI_API_KEY=sk-...
XAI_API_KEY=xai-...
EOF
chmod 600 ~/.config/last30days/.env
```

**Note:** The skill works without API keys using web search fallback, but Reddit and X research require the respective API keys.

## Tips for Memory Semiconductor Research

1. **Be specific with company names**: Use full names (Micron Technology, SK Hynix Inc) for better results
2. **Include product codes**: Search for "HBM3E" or "DDR5" for technical discussions
3. **Use --deep for quarterly updates**: Between earnings, use deep research to catch comprehensive market shifts
4. **Combine with date context**: "Micron Q1 FY26 developments" helps focus on relevant time periods
5. **Track multiple dimensions**: Run separate searches for technology, pricing, capacity, and demand

---

**Created for**: Market intelligence and competitive analysis in memory semiconductors
**Best used**: Between earnings cycles or for real-time market pulse checks
