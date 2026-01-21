#!/usr/bin/env python3
"""
Generate side-by-side Sankey comparisons for memory semiconductor companies.

Supports:
- Company vs. company comparison
- Same company across quarters (temporal comparison)
- Normalized (percentage) or absolute value views

Usage:
    python compare_companies.py --company1 micron.csv --company2 skhynix.csv
    python compare_companies.py --data company.csv --quarters "Q1 FY25,Q2 FY25"
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_data(file_path: str) -> pd.DataFrame:
    """Load revenue flow data from CSV."""
    try:
        df = pd.read_csv(file_path, comment='#')
        df = df.dropna()
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna()
        df = df[df['value'] > 0]
        return df
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None


def get_node_color(node_name: str, company: str = None) -> str:
    """Get color for a node."""
    # End market colors
    end_market_colors = {
        'AI/Datacenter': '#2E86AB',
        'Mobile': '#06A77D',
        'Enterprise': '#D62839',
        'PC': '#717568',
        'Automotive': '#F26419',
        'Industrial': '#8338EC',
        'Consumer': '#3A86FF',
        'Total Revenue': '#34495E',
        'Gross Profit': '#27AE60',
        'COGS': '#E74C3C',
    }

    # Segment colors by company
    company_segment_colors = {
        'micron': {'DRAM': '#A23B72', 'NAND': '#F18F01', 'Emerging': '#C2C5BB'},
        'sk hynix': {'DRAM': '#E74C3C', 'NAND': '#F39C12', 'Emerging': '#95A5A6'},
        'samsung': {'DRAM': '#3498DB', 'NAND': '#9B59B6', 'Emerging': '#BDC3C7'},
    }

    if node_name in end_market_colors:
        return end_market_colors[node_name]

    if company:
        company_lower = company.lower()
        for key, colors in company_segment_colors.items():
            if key in company_lower:
                if node_name in colors:
                    return colors[node_name]

    # Default segment colors
    default_colors = {'DRAM': '#A23B72', 'NAND': '#F18F01', 'Emerging': '#C2C5BB', 'Other': '#C2C5BB'}
    if node_name in default_colors:
        return default_colors[node_name]

    return '#CCCCCC'


def prepare_sankey_data(df: pd.DataFrame, company: str = None, normalize: bool = False) -> dict:
    """Prepare data for Sankey diagram."""
    if normalize:
        # Convert to percentages based on Total Revenue (not sum of all flows)
        # Find the root node's total value (typically "Total Revenue")
        root_nodes = ['Total Revenue', 'Revenue', 'Total']
        total_revenue = 0
        for root in root_nodes:
            total_revenue = df[df['source'] == root]['value'].sum()
            if total_revenue > 0:
                break

        if total_revenue == 0:
            # Fallback: use the largest outflow as the base
            total_revenue = df.groupby('source')['value'].sum().max()

        df = df.copy()
        df['value'] = df['value'] / total_revenue * 100

    all_nodes = list(pd.concat([df['source'], df['target']]).unique())
    node_dict = {node: idx for idx, node in enumerate(all_nodes)}

    # Calculate node totals
    node_totals = {}
    for node in all_nodes:
        outflow = df[df['source'] == node]['value'].sum()
        inflow = df[df['target'] == node]['value'].sum()
        node_totals[node] = max(outflow, inflow)

    node_colors = [get_node_color(node, company) for node in all_nodes]

    if normalize:
        node_labels = [f"{node}<br>{node_totals[node]:.1f}%" for node in all_nodes]
    else:
        node_labels = [f"{node}<br>${node_totals[node]:.2f}B" for node in all_nodes]

    source_indices = df['source'].map(node_dict).tolist()
    target_indices = df['target'].map(node_dict).tolist()
    values = df['value'].tolist()

    # Calculate percentages for each flow (as % of source node total)
    percentages = []
    source_names = []
    target_names = []
    for idx, row in df.iterrows():
        source_total = node_totals[row['source']]
        pct = (row['value'] / source_total * 100) if source_total > 0 else 0
        percentages.append(f"{pct:.1f}%")
        source_names.append(row['source'])
        target_names.append(row['target'])

    # Link colors
    link_colors = []
    for src in df['source']:
        color = get_node_color(src, company)
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            link_colors.append(f'rgba({r},{g},{b},0.4)')
        else:
            link_colors.append('rgba(0,0,0,0.2)')

    return {
        'nodes': all_nodes,
        'node_labels': node_labels,
        'node_colors': node_colors,
        'source': source_indices,
        'target': target_indices,
        'value': values,
        'link_colors': link_colors,
        'percentages': percentages,
        'source_names': source_names,
        'target_names': target_names,
    }


def create_comparison_sankey(
    data1: dict, data2: dict,
    title1: str, title2: str,
    main_title: str = 'Revenue Flow Comparison',
    output_file: str = 'comparison_sankey.html',
    normalize: bool = False,
):
    """Create side-by-side Sankey comparison."""

    # Create subplots
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(title1, title2),
        horizontal_spacing=0.1,
        specs=[[{"type": "sankey"}, {"type": "sankey"}]]
    )

    # Prepare customdata for tooltips
    link_customdata1 = list(zip(
        data1['source_names'],
        data1['target_names'],
        data1['percentages']
    ))
    link_customdata2 = list(zip(
        data2['source_names'],
        data2['target_names'],
        data2['percentages']
    ))

    # Determine tooltip format based on normalize flag
    if normalize:
        hover_template = '<b>%{customdata[0]} → %{customdata[1]}</b><br>%{value:.1f}% (%{customdata[2]})<extra></extra>'
    else:
        hover_template = '<b>%{customdata[0]} → %{customdata[1]}</b><br>$%{value:.2f}B (%{customdata[2]})<extra></extra>'

    # Add first Sankey
    fig.add_trace(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=data1['node_labels'],
                color=data1['node_colors'],
                hovertemplate='%{label}<extra></extra>',
            ),
            link=dict(
                source=data1['source'],
                target=data1['target'],
                value=data1['value'],
                color=data1['link_colors'],
                customdata=link_customdata1,
                hovertemplate=hover_template,
            ),
            domain=dict(x=[0, 0.45], y=[0, 1]),
        ),
        row=1, col=1
    )

    # Add second Sankey
    fig.add_trace(
        go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color='black', width=0.5),
                label=data2['node_labels'],
                color=data2['node_colors'],
                hovertemplate='%{label}<extra></extra>',
            ),
            link=dict(
                source=data2['source'],
                target=data2['target'],
                value=data2['value'],
                color=data2['link_colors'],
                customdata=link_customdata2,
                hovertemplate=hover_template,
            ),
            domain=dict(x=[0.55, 1], y=[0, 1]),
        ),
        row=1, col=2
    )

    # Update layout
    unit = "%" if normalize else "$B"
    fig.update_layout(
        title=dict(
            text=f"{main_title} ({unit})",
            font=dict(size=20, family='Arial Black'),
            x=0.5,
            xanchor='center',
        ),
        font=dict(size=11, family='Arial'),
        height=700,
        width=1400,
        margin=dict(l=30, r=30, t=100, b=30),
        paper_bgcolor='white',
    )

    # Save
    fig.write_html(output_file)
    print(f"Saved comparison: {output_file}")

    # Try to save PNG
    try:
        png_path = output_file.replace('.html', '.png')
        fig.write_image(png_path, width=1400, height=700, scale=2)
        print(f"Saved PNG: {png_path}")
    except Exception as e:
        print(f"Could not save PNG (install kaleido): {e}")

    return fig


def compare_companies(
    file1: str, file2: str,
    company1: str = None, company2: str = None,
    output_file: str = 'comparison_sankey.html',
    normalize: bool = False,
):
    """Compare two companies side-by-side."""

    # Load data
    df1 = load_data(file1)
    df2 = load_data(file2)

    if df1 is None or df2 is None:
        return None

    # Infer company names from file if not provided
    if not company1:
        company1 = Path(file1).stem.replace('_', ' ').title()
    if not company2:
        company2 = Path(file2).stem.replace('_', ' ').title()

    print(f"\nComparing {company1} vs {company2}")
    print(f"  {company1}: {len(df1)} flows, ${df1['value'].sum():.2f}B total")
    print(f"  {company2}: {len(df2)} flows, ${df2['value'].sum():.2f}B total")

    # Prepare Sankey data
    data1 = prepare_sankey_data(df1, company1, normalize)
    data2 = prepare_sankey_data(df2, company2, normalize)

    # Create comparison
    return create_comparison_sankey(
        data1, data2,
        title1=company1,
        title2=company2,
        main_title='Revenue Flow Comparison',
        output_file=output_file,
        normalize=normalize,
    )


def compare_quarters(
    data_file: str,
    quarters: list,
    company: str = None,
    output_file: str = 'quarterly_comparison.html',
    normalize: bool = False,
):
    """Compare same company across quarters (requires multi-quarter CSV)."""

    df = load_data(data_file)
    if df is None:
        return None

    if 'quarter' not in df.columns:
        print("Error: CSV must have 'quarter' column for quarterly comparison")
        print("Expected columns: source, target, value, quarter")
        return None

    # Get data for each quarter
    q1_data = df[df['quarter'] == quarters[0]]
    q2_data = df[df['quarter'] == quarters[1]]

    if q1_data.empty or q2_data.empty:
        print(f"Error: Could not find data for quarters: {quarters}")
        print(f"Available quarters: {df['quarter'].unique().tolist()}")
        return None

    print(f"\nComparing {quarters[0]} vs {quarters[1]}")

    # Prepare Sankey data
    data1 = prepare_sankey_data(q1_data, company, normalize)
    data2 = prepare_sankey_data(q2_data, company, normalize)

    title = f"{company} " if company else ""

    return create_comparison_sankey(
        data1, data2,
        title1=f"{title}{quarters[0]}",
        title2=f"{title}{quarters[1]}",
        main_title=f'{title}Quarterly Revenue Comparison',
        output_file=output_file,
        normalize=normalize,
    )


def create_summary_table(file1: str, file2: str, company1: str, company2: str) -> pd.DataFrame:
    """Create comparison summary table."""

    df1 = load_data(file1)
    df2 = load_data(file2)

    if df1 is None or df2 is None:
        return None

    # Get segment totals
    segments = ['DRAM', 'NAND', 'Emerging', 'Other']

    summary = []
    for seg in segments:
        seg1 = df1[df1['target'] == seg]['value'].sum()
        seg2 = df2[df2['target'] == seg]['value'].sum()
        if seg1 > 0 or seg2 > 0:
            summary.append({
                'Segment': seg,
                f'{company1} ($B)': seg1,
                f'{company2} ($B)': seg2,
                'Difference ($B)': seg1 - seg2,
            })

    # Get end market totals
    markets = ['AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive', 'Industrial']

    for market in markets:
        m1 = df1[df1['target'] == market]['value'].sum()
        m2 = df2[df2['target'] == market]['value'].sum()
        if m1 > 0 or m2 > 0:
            summary.append({
                'Segment': market,
                f'{company1} ($B)': m1,
                f'{company2} ($B)': m2,
                'Difference ($B)': m1 - m2,
            })

    return pd.DataFrame(summary)


def main():
    parser = argparse.ArgumentParser(
        description='Generate side-by-side Sankey comparisons',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --company1 micron.csv --company2 skhynix.csv
  %(prog)s --company1 micron.csv --company2 skhynix.csv --normalize
  %(prog)s --data company_quarterly.csv --quarters "Q1 FY25,Q2 FY25"
        """
    )
    parser.add_argument('--company1', '-c1', help='First company CSV file')
    parser.add_argument('--company2', '-c2', help='Second company CSV file')
    parser.add_argument('--name1', '-n1', help='First company name')
    parser.add_argument('--name2', '-n2', help='Second company name')
    parser.add_argument('--data', '-d', help='Single CSV with quarterly data')
    parser.add_argument('--quarters', '-q', help='Comma-separated quarters to compare')
    parser.add_argument('--output', '-o', default='comparison_sankey.html',
                        help='Output file path')
    parser.add_argument('--normalize', action='store_true',
                        help='Normalize to percentages for comparison')
    parser.add_argument('--summary', action='store_true',
                        help='Print summary comparison table')

    args = parser.parse_args()

    # Company comparison
    if args.company1 and args.company2:
        compare_companies(
            args.company1, args.company2,
            args.name1, args.name2,
            args.output,
            args.normalize,
        )

        if args.summary:
            summary = create_summary_table(
                args.company1, args.company2,
                args.name1 or 'Company 1',
                args.name2 or 'Company 2',
            )
            if summary is not None:
                print("\n" + "="*60)
                print("COMPARISON SUMMARY")
                print("="*60)
                print(summary.to_string(index=False))
        return 0

    # Quarterly comparison
    if args.data and args.quarters:
        quarters = [q.strip() for q in args.quarters.split(',')]
        if len(quarters) != 2:
            print("Error: Provide exactly 2 quarters to compare")
            return 1

        compare_quarters(
            args.data,
            quarters,
            args.name1,  # Use as company name
            args.output,
            args.normalize,
        )
        return 0

    print("Usage: Specify --company1 and --company2, or --data with --quarters")
    print("Run with --help for more information.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
