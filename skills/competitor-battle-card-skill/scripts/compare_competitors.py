#!/usr/bin/env python3
"""
Compare Competitors Script
Generates side-by-side comparison tables for competitor battle cards.

Usage:
    python compare_competitors.py --competitors "Micron,Samsung,SKHynix" --metrics "revenue,margin,capex"
    python compare_competitors.py --create-template
"""

import argparse
import csv
import json
import sys
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: pandas not installed.", file=sys.stderr)
    print("Install with: pip install pandas", file=sys.stderr)
    sys.exit(1)


def load_competitor_data(competitor_name: str) -> dict:
    """
    Load competitor data from JSON file.

    Args:
        competitor_name: Name of competitor

    Returns:
        dict: Competitor data
    """
    # Look for data file
    filename = f"{competitor_name.lower().replace(' ', '_')}_data.json"

    if not Path(filename).exists():
        print(f"Warning: Data file not found: {filename}", file=sys.stderr)
        return {}

    with open(filename, "r") as f:
        return json.load(f)


def create_financial_comparison(competitors: list) -> pd.DataFrame:
    """
    Create financial comparison table across competitors.

    Args:
        competitors: List of competitor names

    Returns:
        pd.DataFrame: Comparison table
    """
    data = {
        "Metric": [
            "Total Revenue ($B)",
            "Memory Revenue ($B)",
            "DRAM Revenue ($B)",
            "NAND Revenue ($B)",
            "Gross Margin (%)",
            "Operating Margin (%)",
            "R&D Spending ($B)",
            "R&D % of Revenue",
            "CapEx ($B)",
            "Market Cap ($B)"
        ]
    }

    # Add columns for each competitor
    for competitor in competitors:
        comp_data = load_competitor_data(competitor)

        # Extract financial metrics (customize based on your data structure)
        financials = comp_data.get("financials", {})

        data[competitor] = [
            financials.get("total_revenue_billions", "N/A"),
            financials.get("memory_revenue_billions", "N/A"),
            financials.get("dram_revenue_billions", "N/A"),
            financials.get("nand_revenue_billions", "N/A"),
            financials.get("gross_margin_percent", "N/A"),
            financials.get("operating_margin_percent", "N/A"),
            financials.get("rd_spending_billions", "N/A"),
            financials.get("rd_percent_revenue", "N/A"),
            financials.get("capex_billions", "N/A"),
            financials.get("market_cap_billions", "N/A")
        ]

    return pd.DataFrame(data)


def create_technology_comparison(competitors: list) -> pd.DataFrame:
    """
    Create technology positioning comparison.

    Args:
        competitors: List of competitor names

    Returns:
        pd.DataFrame: Technology comparison table
    """
    data = {
        "Technology": [
            "DRAM Node (Leading Edge)",
            "HBM Generation (Production)",
            "HBM Generation (Development)",
            "DDR5 Status",
            "LPDDR Generation",
            "NAND Layers (Production)",
            "NAND Layers (Development)",
            "CXL Memory"
        ]
    }

    # Add columns for each competitor
    for competitor in competitors:
        comp_data = load_competitor_data(competitor)

        # Extract technology data (customize based on your structure)
        tech = comp_data.get("technology", {})

        data[competitor] = [
            tech.get("dram_node", "N/A"),
            tech.get("hbm_production", "N/A"),
            tech.get("hbm_development", "N/A"),
            tech.get("ddr5_status", "N/A"),
            tech.get("lpddr_gen", "N/A"),
            tech.get("nand_layers_production", "N/A"),
            tech.get("nand_layers_development", "N/A"),
            tech.get("cxl_status", "N/A")
        ]

    return pd.DataFrame(data)


def create_market_position_comparison(competitors: list) -> pd.DataFrame:
    """
    Create market position comparison.

    Args:
        competitors: List of competitor names

    Returns:
        pd.DataFrame: Market position table
    """
    data = {
        "Segment": [
            "DRAM Market Share (%)",
            "NAND Market Share (%)",
            "HBM Market Share (%)",
            "AI/Datacenter Position",
            "Mobile DRAM Position",
            "Enterprise SSD Position",
            "Automotive Memory Position"
        ]
    }

    # Add columns for each competitor
    for competitor in competitors:
        comp_data = load_competitor_data(competitor)

        market = comp_data.get("market_position", {})

        data[competitor] = [
            market.get("dram_share", "N/A"),
            market.get("nand_share", "N/A"),
            market.get("hbm_share", "N/A"),
            market.get("ai_datacenter", "N/A"),
            market.get("mobile_dram", "N/A"),
            market.get("enterprise_ssd", "N/A"),
            market.get("automotive", "N/A")
        ]

    return pd.DataFrame(data)


def create_template():
    """Create template CSV for competitor comparison data."""
    template_data = {
        "competitor": ["Micron", "Samsung", "SK Hynix"],
        "total_revenue_billions": [25.0, 35.0, 30.0],
        "memory_revenue_billions": [24.0, 33.0, 28.0],
        "dram_revenue_billions": [15.0, 20.0, 20.0],
        "nand_revenue_billions": [9.0, 13.0, 8.0],
        "gross_margin_percent": [28.5, 35.2, 32.1],
        "operating_margin_percent": [15.2, 22.1, 20.3],
        "rd_spending_billions": [2.5, 3.8, 3.2],
        "capex_billions": [7.5, 9.2, 8.1],
        "dram_market_share": [23, 42, 29],
        "nand_market_share": [14, 34, 20],
        "hbm_market_share": [10, 25, 60],
        "dram_node": ["1β", "1β", "1β"],
        "hbm_production": ["HBM3", "HBM3E", "HBM3E"],
        "nand_layers": [232, 236, 238]
    }

    df = pd.DataFrame(template_data)
    filename = "competitor_comparison_template.csv"
    df.to_csv(filename, index=False)

    print(f"✅ Template created: {filename}")
    print("Edit this file with actual competitor data, then use for comparisons.")


def generate_markdown_table(df: pd.DataFrame) -> str:
    """
    Convert DataFrame to markdown table format.

    Args:
        df: pandas DataFrame

    Returns:
        str: Markdown formatted table
    """
    # Get column names
    headers = "| " + " | ".join(df.columns) + " |"
    separator = "|" + "|".join(["---" for _ in df.columns]) + "|"

    rows = []
    for _, row in df.iterrows():
        row_str = "| " + " | ".join([str(val) for val in row]) + " |"
        rows.append(row_str)

    return "\n".join([headers, separator] + rows)


def main():
    parser = argparse.ArgumentParser(
        description="Compare competitors for battle cards"
    )
    parser.add_argument(
        "--competitors",
        type=str,
        help="Comma-separated list of competitors (e.g., 'Micron,Samsung,SKHynix')"
    )
    parser.add_argument(
        "--metrics",
        type=str,
        default="all",
        help="Metrics to compare: 'financial', 'technology', 'market', or 'all' (default: all)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="competitor_comparison.md",
        help="Output markdown file (default: competitor_comparison.md)"
    )
    parser.add_argument(
        "--create-template",
        action="store_true",
        help="Create template CSV for competitor data"
    )

    args = parser.parse_args()

    if args.create_template:
        create_template()
        return

    if not args.competitors:
        parser.print_help()
        sys.exit(1)

    competitors = [c.strip() for c in args.competitors.split(",")]

    print(f"\n{'='*60}")
    print(f"Comparing Competitors: {', '.join(competitors)}")
    print(f"{'='*60}\n")

    output_content = []

    # Generate requested comparisons
    if args.metrics in ["all", "financial"]:
        print("📊 Generating financial comparison...")
        financial_df = create_financial_comparison(competitors)
        output_content.append("## Financial Comparison\n")
        output_content.append(generate_markdown_table(financial_df))
        output_content.append("\n")

    if args.metrics in ["all", "technology"]:
        print("🔬 Generating technology comparison...")
        tech_df = create_technology_comparison(competitors)
        output_content.append("## Technology Comparison\n")
        output_content.append(generate_markdown_table(tech_df))
        output_content.append("\n")

    if args.metrics in ["all", "market"]:
        print("📈 Generating market position comparison...")
        market_df = create_market_position_comparison(competitors)
        output_content.append("## Market Position Comparison\n")
        output_content.append(generate_markdown_table(market_df))
        output_content.append("\n")

    # Write to file
    with open(args.output, "w") as f:
        f.write("\n".join(output_content))

    print(f"\n✅ Comparison saved to: {args.output}")
    print("\n💡 Note: Update competitor data JSON files for accurate comparisons")
    print("   Use --create-template to generate a template CSV")


if __name__ == "__main__":
    main()
