#!/usr/bin/env python3
"""
Generate interactive Sankey diagrams for memory semiconductor revenue flows.

Supports multi-layer flows:
- Total Revenue → Segments (DRAM, NAND, Emerging)
- Segments → End Markets (AI/Datacenter, Mobile, Enterprise, PC, Automotive)
- Optional: End Markets → Profitability (Gross Profit, COGS)

Usage:
    python sankey_generator.py --data revenue_data.csv
    python sankey_generator.py --data revenue_data.csv --company "Micron" --quarter "Q2 FY25"
    python sankey_generator.py --create-template
"""

import argparse
import os
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


# Company color schemes
COMPANY_COLORS = {
    'micron': {
        'primary': '#0066B3',
        'DRAM': '#A23B72',
        'NAND': '#F18F01',
        'Emerging': '#C2C5BB',
        'Other': '#C2C5BB',
    },
    'sk hynix': {
        'primary': '#ED1C24',
        'DRAM': '#E74C3C',
        'NAND': '#F39C12',
        'Emerging': '#95A5A6',
        'Other': '#95A5A6',
    },
    'samsung': {
        'primary': '#1428A0',
        'DRAM': '#3498DB',
        'NAND': '#9B59B6',
        'Emerging': '#BDC3C7',
        'Other': '#BDC3C7',
    },
    'western digital': {
        'primary': '#005EB8',
        'DRAM': '#3498DB',
        'NAND': '#E67E22',
        'Emerging': '#95A5A6',
        'Other': '#95A5A6',
    },
    'kioxia': {
        'primary': '#E60012',
        'DRAM': '#E74C3C',
        'NAND': '#C0392B',
        'Emerging': '#7F8C8D',
        'Other': '#7F8C8D',
    },
}

# End market colors (consistent across all companies)
END_MARKET_COLORS = {
    'AI/Datacenter': '#2E86AB',
    'Datacenter': '#2E86AB',
    'AI': '#2E86AB',
    'Mobile': '#06A77D',
    'Enterprise': '#D62839',
    'PC': '#717568',
    'PC/Client': '#717568',
    'Client': '#717568',
    'Automotive': '#F26419',
    'Auto': '#F26419',
    'Industrial': '#8338EC',
    'Industrial/IoT': '#8338EC',
    'IoT': '#8338EC',
    'Consumer': '#3A86FF',
    'Embedded': '#9B59B6',
    'Gross Profit': '#27AE60',
    'COGS': '#E74C3C',
    'Operating Income': '#2ECC71',
    'Total Revenue': '#34495E',
}

DEFAULT_COLOR = '#CCCCCC'


def get_node_color(node_name: str, company: str = None) -> str:
    """Get color for a node based on name and company."""
    # Check end market colors first
    if node_name in END_MARKET_COLORS:
        return END_MARKET_COLORS[node_name]

    # Check company-specific colors
    if company:
        company_lower = company.lower()
        for key, colors in COMPANY_COLORS.items():
            if key in company_lower:
                if node_name in colors:
                    return colors[node_name]

    # Default segment colors (Micron scheme)
    default_segment_colors = COMPANY_COLORS['micron']
    if node_name in default_segment_colors:
        return default_segment_colors[node_name]

    return DEFAULT_COLOR


def create_sample_data() -> pd.DataFrame:
    """Create sample multi-layer revenue flow data for Micron Q2 FY25."""
    data = {
        'source': [
            # Layer 1: Total → Segments
            'Total Revenue', 'Total Revenue', 'Total Revenue',
            # Layer 2: DRAM → End Markets
            'DRAM', 'DRAM', 'DRAM', 'DRAM', 'DRAM',
            # Layer 2: NAND → End Markets
            'NAND', 'NAND', 'NAND', 'NAND', 'NAND',
            # Layer 2: Emerging → End Markets
            'Emerging', 'Emerging',
        ],
        'target': [
            # Layer 1
            'DRAM', 'NAND', 'Emerging',
            # Layer 2: DRAM
            'AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive',
            # Layer 2: NAND
            'AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive',
            # Layer 2: Emerging
            'AI/Datacenter', 'Industrial',
        ],
        'value': [
            # Layer 1: Total Revenue breakdown (~$8.7B)
            6.75, 1.85, 0.10,
            # Layer 2: DRAM to End Markets
            3.50, 1.60, 0.85, 0.65, 0.15,
            # Layer 2: NAND to End Markets
            0.70, 0.50, 0.35, 0.25, 0.05,
            # Layer 2: Emerging
            0.08, 0.02,
        ]
    }
    return pd.DataFrame(data)


def create_template_csv(output_path: str = 'revenue_template.csv'):
    """Create a template CSV file for data entry."""
    template_data = {
        'source': [
            '# Layer 1: Total Revenue to Segments',
            'Total Revenue', 'Total Revenue', 'Total Revenue',
            '# Layer 2: Segments to End Markets',
            'DRAM', 'DRAM', 'DRAM', 'DRAM', 'DRAM',
            'NAND', 'NAND', 'NAND', 'NAND', 'NAND',
            'Emerging', 'Emerging',
            '# Layer 3 (Optional): End Markets to Profitability',
            '# AI/Datacenter', '# AI/Datacenter',
        ],
        'target': [
            '',
            'DRAM', 'NAND', 'Emerging',
            '',
            'AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive',
            'AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive',
            'AI/Datacenter', 'Industrial',
            '',
            '# Gross Profit', '# COGS',
        ],
        'value': [
            '',
            0.0, 0.0, 0.0,
            '',
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0,
            '',
            '# 0.0', '# 0.0',
        ]
    }

    # Write as CSV with comments
    with open(output_path, 'w') as f:
        f.write("# Revenue Flow Template\n")
        f.write("# Fill in revenue values in billions USD\n")
        f.write("# Lines starting with # are comments and will be ignored\n")
        f.write("#\n")
        f.write("source,target,value\n")
        f.write("# Layer 1: Total Revenue to Segments\n")
        f.write("Total Revenue,DRAM,0.0\n")
        f.write("Total Revenue,NAND,0.0\n")
        f.write("Total Revenue,Emerging,0.0\n")
        f.write("#\n")
        f.write("# Layer 2: DRAM to End Markets\n")
        f.write("DRAM,AI/Datacenter,0.0\n")
        f.write("DRAM,Mobile,0.0\n")
        f.write("DRAM,Enterprise,0.0\n")
        f.write("DRAM,PC,0.0\n")
        f.write("DRAM,Automotive,0.0\n")
        f.write("#\n")
        f.write("# Layer 2: NAND to End Markets\n")
        f.write("NAND,AI/Datacenter,0.0\n")
        f.write("NAND,Mobile,0.0\n")
        f.write("NAND,Enterprise,0.0\n")
        f.write("NAND,PC,0.0\n")
        f.write("NAND,Automotive,0.0\n")
        f.write("#\n")
        f.write("# Layer 2: Emerging to End Markets (optional)\n")
        f.write("# Emerging,AI/Datacenter,0.0\n")
        f.write("# Emerging,Industrial,0.0\n")
        f.write("#\n")
        f.write("# Layer 3: End Markets to Profitability (optional)\n")
        f.write("# AI/Datacenter,Gross Profit,0.0\n")
        f.write("# AI/Datacenter,COGS,0.0\n")

    print(f"Created template: {output_path}")
    print("\nTemplate structure:")
    print("  - Layer 1: Total Revenue → Segments (DRAM, NAND, Emerging)")
    print("  - Layer 2: Segments → End Markets (AI/Datacenter, Mobile, etc.)")
    print("  - Layer 3: (Optional) End Markets → Profitability")
    print("\nEdit the file with actual revenue values (in billions USD)")


def load_data(file_path: str) -> pd.DataFrame:
    """Load revenue flow data from CSV, ignoring comment lines."""
    try:
        df = pd.read_csv(file_path, comment='#')
        # Remove any rows with NaN or empty values
        df = df.dropna()
        df = df[df['value'] != 0]
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna()
        print(f"Loaded {len(df)} flow records from {file_path}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def prepare_sankey_data(df: pd.DataFrame, company: str = None) -> dict:
    """Prepare data structure for Plotly Sankey diagram."""
    # Get all unique nodes
    all_nodes = list(pd.concat([df['source'], df['target']]).unique())

    # Create node index mapping
    node_dict = {node: idx for idx, node in enumerate(all_nodes)}

    # Calculate node totals for labels
    node_totals = {}
    for node in all_nodes:
        # Sum of outflows
        outflow = df[df['source'] == node]['value'].sum()
        # Sum of inflows
        inflow = df[df['target'] == node]['value'].sum()
        # Use the larger value (for intermediate nodes they should be equal)
        node_totals[node] = max(outflow, inflow)

    # Create node colors
    node_colors = [get_node_color(node, company) for node in all_nodes]

    # Create node labels with values
    node_labels = [f"{node}<br>${node_totals[node]:.2f}B" for node in all_nodes]

    # Map flows to indices
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

    # Create link colors (semi-transparent version of source node color)
    link_colors = []
    for src in df['source']:
        color = get_node_color(src, company)
        # Convert hex to rgba with 0.4 opacity
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
        'node_totals': node_totals,
        'source': source_indices,
        'target': target_indices,
        'value': values,
        'link_colors': link_colors,
        'percentages': percentages,
        'source_names': source_names,
        'target_names': target_names,
    }


def create_sankey_diagram(
    sankey_data: dict,
    title: str = 'Revenue Flow',
    company: str = None,
    quarter: str = None,
    output_file: str = 'sankey_revenue.html',
    output_format: str = 'html',
    width: int = 1200,
    height: int = 600,
) -> go.Figure:
    """Create interactive Sankey diagram using Plotly."""

    # Build title
    full_title = title
    if company and quarter:
        full_title = f"{company} {quarter} - {title}"
    elif company:
        full_title = f"{company} - {title}"
    elif quarter:
        full_title = f"{quarter} - {title}"

    # Prepare customdata for link tooltips: [source_name, target_name, percentage]
    link_customdata = list(zip(
        sankey_data['source_names'],
        sankey_data['target_names'],
        sankey_data['percentages']
    ))

    # Create figure
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=20,
            thickness=25,
            line=dict(color='black', width=0.5),
            label=sankey_data['node_labels'],
            color=sankey_data['node_colors'],
            hovertemplate='%{label}<extra></extra>',
        ),
        link=dict(
            source=sankey_data['source'],
            target=sankey_data['target'],
            value=sankey_data['value'],
            color=sankey_data['link_colors'],
            customdata=link_customdata,
            hovertemplate='<b>%{customdata[0]} → %{customdata[1]}</b><br>' +
                         '$%{value:.2f}B (%{customdata[2]})<extra></extra>',
        )
    )])

    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=22, family='Arial Black'),
            x=0.5,
            xanchor='center',
        ),
        font=dict(size=12, family='Arial'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=height,
        width=width,
        margin=dict(l=30, r=30, t=80, b=30),
    )

    # Save output
    output_path = Path(output_file)

    if output_format == 'html' or output_file.endswith('.html'):
        fig.write_html(str(output_path))
        print(f"Saved interactive Sankey: {output_path}")

    if output_format == 'png' or output_file.endswith('.png'):
        png_path = output_path.with_suffix('.png') if not output_file.endswith('.png') else output_path
        try:
            fig.write_image(str(png_path), width=width, height=height, scale=2)
            print(f"Saved PNG: {png_path}")
        except Exception as e:
            print(f"Could not save PNG (install kaleido: pip install kaleido): {e}")

    if output_format == 'svg' or output_file.endswith('.svg'):
        svg_path = output_path.with_suffix('.svg') if not output_file.endswith('.svg') else output_path
        try:
            fig.write_image(str(svg_path), format='svg', width=width, height=height)
            print(f"Saved SVG: {svg_path}")
        except Exception as e:
            print(f"Could not save SVG (install kaleido: pip install kaleido): {e}")

    # Also save HTML if format is png or svg (for interactive version)
    if output_format in ['png', 'svg']:
        html_path = output_path.with_suffix('.html')
        fig.write_html(str(html_path))
        print(f"Also saved interactive HTML: {html_path}")

    return fig


def generate_summary_tables(df: pd.DataFrame) -> tuple:
    """Generate summary tables for segments and end markets."""

    # Segment totals (sources in layer 1)
    layer1_sources = ['Total Revenue']
    segment_df = df[df['source'].isin(layer1_sources)]
    if not segment_df.empty:
        segment_totals = segment_df.groupby('target')['value'].sum().reset_index()
        segment_totals.columns = ['Segment', 'Revenue ($B)']
        total = segment_totals['Revenue ($B)'].sum()
        segment_totals['% of Total'] = (segment_totals['Revenue ($B)'] / total * 100).round(1)
        segment_totals = segment_totals.sort_values('Revenue ($B)', ascending=False)
    else:
        segment_totals = pd.DataFrame()

    # End market totals
    segments = ['DRAM', 'NAND', 'Emerging', 'Other']
    market_df = df[df['source'].isin(segments)]
    if not market_df.empty:
        market_totals = market_df.groupby('target')['value'].sum().reset_index()
        market_totals.columns = ['End Market', 'Revenue ($B)']
        total = market_totals['Revenue ($B)'].sum()
        market_totals['% of Total'] = (market_totals['Revenue ($B)'] / total * 100).round(1)
        market_totals = market_totals.sort_values('Revenue ($B)', ascending=False)
    else:
        market_totals = pd.DataFrame()

    return segment_totals, market_totals


def print_summary(df: pd.DataFrame):
    """Print revenue summary to console."""
    segment_totals, market_totals = generate_summary_tables(df)

    if not segment_totals.empty:
        print("\n" + "="*50)
        print("REVENUE BY SEGMENT")
        print("="*50)
        print(segment_totals.to_string(index=False))
        print(f"\nTotal: ${segment_totals['Revenue ($B)'].sum():.2f}B")

    if not market_totals.empty:
        print("\n" + "="*50)
        print("REVENUE BY END MARKET")
        print("="*50)
        print(market_totals.to_string(index=False))
        print(f"\nTotal: ${market_totals['Revenue ($B)'].sum():.2f}B")

    print("="*50)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Sankey revenue flow diagrams for memory semiconductors',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --data revenue_data.csv
  %(prog)s --data revenue_data.csv --company "Micron" --quarter "Q2 FY25"
  %(prog)s --data revenue_data.csv --format png --output revenue_flow.png
  %(prog)s --create-template
        """
    )
    parser.add_argument('--data', '-d', help='Path to revenue flow CSV file')
    parser.add_argument('--output', '-o', default='sankey_revenue.html',
                        help='Output file path (default: sankey_revenue.html)')
    parser.add_argument('--format', '-f', choices=['html', 'png', 'svg'], default='html',
                        help='Output format (default: html)')
    parser.add_argument('--company', '-c', help='Company name (Micron, SK Hynix, Samsung, etc.)')
    parser.add_argument('--quarter', '-q', help='Quarter label (e.g., Q2 FY25)')
    parser.add_argument('--title', '-t', default='Revenue Flow: Segments to End Markets',
                        help='Chart title')
    parser.add_argument('--width', type=int, default=1200, help='Output width in pixels')
    parser.add_argument('--height', type=int, default=600, help='Output height in pixels')
    parser.add_argument('--create-template', action='store_true',
                        help='Create template CSV file')
    parser.add_argument('--demo', action='store_true',
                        help='Run demo with sample data')

    args = parser.parse_args()

    # Create template if requested
    if args.create_template:
        create_template_csv('revenue_template.csv')
        return 0

    # Load or create data
    if args.data:
        df = load_data(args.data)
        if df is None:
            return 1
    elif args.demo:
        print("Running demo with sample Micron Q2 FY25 data...\n")
        df = create_sample_data()
        args.company = args.company or 'Micron'
        args.quarter = args.quarter or 'Q2 FY25'
    else:
        print("No data file provided. Use --data <file.csv> or --demo for sample data.")
        print("Use --create-template to create a template CSV file.")
        return 1

    # Validate data
    required_cols = ['source', 'target', 'value']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: CSV must contain columns: {required_cols}")
        return 1

    # Print summary
    print_summary(df)

    # Prepare and create Sankey diagram
    sankey_data = prepare_sankey_data(df, args.company)

    print(f"\nGenerating Sankey diagram...")
    create_sankey_diagram(
        sankey_data,
        title=args.title,
        company=args.company,
        quarter=args.quarter,
        output_file=args.output,
        output_format=args.format,
        width=args.width,
        height=args.height,
    )

    print(f"\nOpen {args.output} in a web browser to view the interactive diagram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
