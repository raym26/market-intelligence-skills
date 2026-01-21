# Quick Start Guide

Get up and running with Sankey revenue flow diagrams in 5 minutes.

## 1. Install Dependencies

```bash
pip install pandas plotly kaleido PyPDF2 tabula-py requests beautifulsoup4 --break-system-packages
```

Or use the requirements file:
```bash
pip install -r requirements.txt --break-system-packages
```

## 2. Create Template Data

```bash
python scripts/sankey_generator.py --create-template
```

This creates `revenue_template.csv` with the expected format.

## 3. Edit Your Data

Open the CSV and replace with actual revenue data:

```csv
source,target,value
Total Revenue,DRAM,6.75
Total Revenue,NAND,2.20
DRAM,AI/Datacenter,3.50
DRAM,Mobile,1.80
...
```

## 4. Generate Sankey Diagram

```bash
python scripts/sankey_generator.py --data revenue_template.csv \
  --company "Micron" --quarter "Q2 FY25"
```

## 5. View Output

Open `sankey_revenue.html` in your browser.

## Common Commands

**Generate from example data:**
```bash
python scripts/sankey_generator.py --data examples/example_data.csv
```

**Export PNG for presentations:**
```bash
python scripts/sankey_generator.py --data examples/example_data.csv --format png
```

**Compare two companies:**
```bash
python scripts/compare_companies.py --company1 micron.csv --company2 skhynix.csv
```

## File Structure

```
sankey-revenue-flow-skill/
├── SKILL.md              # Claude instructions
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
├── requirements.txt      # Python dependencies
├── scripts/
│   ├── sankey_generator.py      # Main script
│   ├── extract_revenue_data.py  # Data extraction
│   ├── compare_companies.py     # Comparison tool
│   └── templates/
│       └── revenue_template.csv # Input template
└── examples/
    ├── example_data.csv         # Sample input
    ├── micron_q2_fy25_sankey.html
    └── micron_q2_fy25_sankey.png
```

## Using with Claude

Ask Claude:
```
"Create a Sankey diagram for Micron's latest revenue breakdown"
```

Claude will invoke this skill and guide you through the process.

## Need Help?

- Full docs: See `README.md`
- Script help: `python scripts/sankey_generator.py --help`
- SKILL.md has detailed methodology

---

**Ready to visualize revenue flows!**
