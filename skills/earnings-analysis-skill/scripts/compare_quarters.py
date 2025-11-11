"""
Compare quarterly financial performance and generate trend tables.

Usage:
    python compare_quarters.py --company "Micron" --data historical_data.csv
"""

import argparse
import pandas as pd
import numpy as np
from datetime import datetime


def load_historical_data(file_path):
    """Load historical quarterly data from CSV."""
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Loaded {len(df)} quarters of data")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        return None


def create_sample_data():
    """Create sample template for historical data."""
    columns = [
        'Quarter', 'Fiscal_Year', 'Date',
        'Revenue_Total_B', 'Revenue_DRAM_B', 'Revenue_NAND_B',
        'Gross_Margin_Pct', 'Operating_Margin_Pct',
        'DRAM_Bit_Growth_QoQ', 'DRAM_ASP_Change_QoQ',
        'NAND_Bit_Growth_QoQ', 'NAND_ASP_Change_QoQ',
        'CapEx_B', 'Guidance_Revenue_Low_B', 'Guidance_Revenue_High_B'
    ]
    
    # Sample data for Micron (illustrative)
    data = {
        'Quarter': ['Q4', 'Q1', 'Q2', 'Q3'],
        'Fiscal_Year': [2024, 2025, 2025, 2025],
        'Date': ['2024-08-31', '2024-11-30', '2025-02-28', '2025-05-31'],
        'Revenue_Total_B': [7.75, 8.71, 9.08, None],
        'Revenue_DRAM_B': [5.58, 6.32, 6.75, None],
        'Revenue_NAND_B': [2.05, 2.26, 2.20, None],
        'Gross_Margin_Pct': [34.8, 39.6, 42.1, None],
        'Operating_Margin_Pct': [19.2, 24.5, 27.8, None],
        'DRAM_Bit_Growth_QoQ': [2, 5, 4, None],
        'DRAM_ASP_Change_QoQ': [15, 8, 3, None],
        'NAND_Bit_Growth_QoQ': [-2, 7, 2, None],
        'NAND_ASP_Change_QoQ': [12, 5, -1, None],
        'CapEx_B': [2.4, 2.6, 2.8, None],
        'Guidance_Revenue_Low_B': [8.5, 8.9, 9.2, None],
        'Guidance_Revenue_High_B': [8.9, 9.3, 9.6, None]
    }
    
    return pd.DataFrame(data)


def calculate_changes(df):
    """Calculate QoQ and YoY changes."""
    df = df.copy()
    
    # Sort by date
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    # QoQ changes
    for col in ['Revenue_Total_B', 'Revenue_DRAM_B', 'Revenue_NAND_B', 
                'Gross_Margin_Pct', 'Operating_Margin_Pct']:
        if col in df.columns:
            df[f'{col}_QoQ_Pct'] = df[col].pct_change() * 100
    
    # YoY changes (4 quarters back)
    for col in ['Revenue_Total_B', 'Revenue_DRAM_B', 'Revenue_NAND_B']:
        if col in df.columns:
            df[f'{col}_YoY_Pct'] = df[col].pct_change(periods=4) * 100
    
    return df


def generate_comparison_table(df, num_quarters=4):
    """Generate formatted comparison table for most recent quarters."""
    df_recent = df.tail(num_quarters).copy()
    
    # Create display table
    display_cols = {
        'Quarter': 'Quarter',
        'Revenue_Total_B': 'Revenue ($B)',
        'Revenue_Total_B_QoQ_Pct': 'QoQ %',
        'Revenue_Total_B_YoY_Pct': 'YoY %',
        'Gross_Margin_Pct': 'GM %',
        'Operating_Margin_Pct': 'OM %',
        'CapEx_B': 'CapEx ($B)'
    }
    
    comparison = pd.DataFrame()
    for orig_col, display_col in display_cols.items():
        if orig_col in df_recent.columns:
            comparison[display_col] = df_recent[orig_col]
    
    return comparison


def generate_segment_table(df, num_quarters=4):
    """Generate segment revenue breakdown table."""
    df_recent = df.tail(num_quarters).copy()
    
    segment_cols = {
        'Quarter': 'Quarter',
        'Revenue_DRAM_B': 'DRAM ($B)',
        'Revenue_NAND_B': 'NAND ($B)',
        'DRAM_Bit_Growth_QoQ': 'DRAM Bits (QoQ%)',
        'DRAM_ASP_Change_QoQ': 'DRAM ASP (QoQ%)',
        'NAND_Bit_Growth_QoQ': 'NAND Bits (QoQ%)',
        'NAND_ASP_Change_QoQ': 'NAND ASP (QoQ%)'
    }
    
    segment_table = pd.DataFrame()
    for orig_col, display_col in segment_cols.items():
        if orig_col in df_recent.columns:
            segment_table[display_col] = df_recent[orig_col]
    
    # Calculate segment mix
    if 'Revenue_DRAM_B' in df_recent.columns and 'Revenue_Total_B' in df_recent.columns:
        segment_table['DRAM %'] = (df_recent['Revenue_DRAM_B'] / df_recent['Revenue_Total_B'] * 100).round(1)
    if 'Revenue_NAND_B' in df_recent.columns and 'Revenue_Total_B' in df_recent.columns:
        segment_table['NAND %'] = (df_recent['Revenue_NAND_B'] / df_recent['Revenue_Total_B'] * 100).round(1)
    
    return segment_table


def format_table_markdown(df, title):
    """Format DataFrame as markdown table."""
    output = f"\n### {title}\n\n"
    output += df.to_markdown(index=False, floatfmt='.1f')
    output += "\n"
    return output


def analyze_trends(df):
    """Generate insights from trend analysis."""
    insights = []
    
    latest = df.iloc[-1]
    prior = df.iloc[-2] if len(df) > 1 else None
    
    # Revenue trend
    if prior is not None and 'Revenue_Total_B' in df.columns:
        rev_change = ((latest['Revenue_Total_B'] - prior['Revenue_Total_B']) / prior['Revenue_Total_B'] * 100)
        if rev_change > 5:
            insights.append(f"✓ Strong revenue growth: +{rev_change:.1f}% QoQ")
        elif rev_change < -5:
            insights.append(f"⚠️ Revenue decline: {rev_change:.1f}% QoQ")
    
    # Margin expansion/contraction
    if prior is not None and 'Gross_Margin_Pct' in df.columns:
        margin_change = latest['Gross_Margin_Pct'] - prior['Gross_Margin_Pct']
        if margin_change > 2:
            insights.append(f"✓ Margin expansion: +{margin_change:.1f}pp to {latest['Gross_Margin_Pct']:.1f}%")
        elif margin_change < -2:
            insights.append(f"⚠️ Margin compression: {margin_change:.1f}pp to {latest['Gross_Margin_Pct']:.1f}%")
    
    # Segment mix shift
    if 'Revenue_DRAM_B' in df.columns and 'Revenue_NAND_B' in df.columns:
        dram_pct = latest['Revenue_DRAM_B'] / latest['Revenue_Total_B'] * 100
        insights.append(f"ℹ️ DRAM mix: {dram_pct:.1f}% of revenue")
    
    return insights


def main():
    parser = argparse.ArgumentParser(description='Compare quarterly financial performance')
    parser.add_argument('--company', required=True, help='Company name')
    parser.add_argument('--data', help='Path to historical data CSV (optional)')
    parser.add_argument('--quarters', type=int, default=4, help='Number of quarters to compare')
    parser.add_argument('--output', default='quarterly_comparison.md', help='Output markdown file')
    parser.add_argument('--create-template', action='store_true', 
                       help='Create sample data template')
    
    args = parser.parse_args()
    
    if args.create_template:
        print("Creating sample data template...")
        sample_df = create_sample_data()
        sample_df.to_csv('historical_data_template.csv', index=False)
        print("✓ Created historical_data_template.csv")
        print("\n💡 Edit this file with actual data, then run:")
        print(f"   python compare_quarters.py --company '{args.company}' --data historical_data_template.csv")
        return
    
    # Load data
    if args.data:
        df = load_historical_data(args.data)
    else:
        print("No data file provided. Using sample data for demonstration...\n")
        df = create_sample_data()
    
    if df is None:
        return
    
    # Calculate changes
    df = calculate_changes(df)
    
    # Generate comparison tables
    print(f"\n📊 Quarterly Comparison for {args.company}\n")
    print("="*60)
    
    comparison_table = generate_comparison_table(df, args.quarters)
    print(format_table_markdown(comparison_table, "Financial Performance Trend"))
    
    segment_table = generate_segment_table(df, args.quarters)
    print(format_table_markdown(segment_table, "Segment Performance"))
    
    # Trend insights
    insights = analyze_trends(df)
    if insights:
        print("\n### Key Trends\n")
        for insight in insights:
            print(f"- {insight}")
    
    # Save to markdown file
    with open(args.output, 'w') as f:
        f.write(f"# {args.company} Quarterly Comparison\n")
        f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        f.write(format_table_markdown(comparison_table, "Financial Performance Trend"))
        f.write(format_table_markdown(segment_table, "Segment Performance"))
        if insights:
            f.write("\n### Key Trends\n\n")
            for insight in insights:
                f.write(f"- {insight}\n")
    
    print(f"\n✓ Saved comparison to {args.output}")


if __name__ == "__main__":
    main()
