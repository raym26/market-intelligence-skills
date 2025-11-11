"""
Generate Sankey diagram showing revenue flow from segments to end markets.

Usage:
    python sankey_revenue.py --data revenue_flow_data.csv
"""

import argparse
import pandas as pd
import plotly.graph_objects as go


def create_sample_revenue_flow():
    """Create sample revenue flow data structure."""
    # Example data structure for Micron Q2 FY25
    data = {
        # From segments to end markets
        'source': ['DRAM', 'DRAM', 'DRAM', 'DRAM', 'DRAM',
                   'NAND', 'NAND', 'NAND', 'NAND', 'NAND'],
        'target': ['AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive',
                   'AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive'],
        'value': [3.5, 1.8, 0.9, 0.45, 0.1,  # DRAM distribution
                  0.8, 0.6, 0.4, 0.3, 0.1]   # NAND distribution
    }
    return pd.DataFrame(data)


def load_revenue_flow_data(file_path):
    """Load revenue flow data from CSV."""
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Loaded revenue flow data")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        return None


def prepare_sankey_data(df):
    """
    Prepare data for Sankey diagram.
    
    Expected columns: source, target, value
    """
    # Get unique nodes
    all_nodes = list(pd.concat([df['source'], df['target']]).unique())
    
    # Create node indices
    node_dict = {node: idx for idx, node in enumerate(all_nodes)}
    
    # Map sources and targets to indices
    source_indices = df['source'].map(node_dict).tolist()
    target_indices = df['target'].map(node_dict).tolist()
    values = df['value'].tolist()
    
    return {
        'nodes': all_nodes,
        'source': source_indices,
        'target': target_indices,
        'value': values
    }


def create_sankey_diagram(sankey_data, title='Revenue Flow', output_file='sankey_revenue.html'):
    """Create interactive Sankey diagram using Plotly."""
    
    # Define colors for segments and end markets
    node_colors = {
        # Segments
        'DRAM': '#A23B72',
        'NAND': '#F18F01',
        'Emerging': '#C2C5BB',
        # End markets
        'AI/Datacenter': '#2E86AB',
        'Mobile': '#06A77D',
        'Enterprise': '#D62839',
        'PC': '#717568',
        'Automotive': '#F26419',
        'Industrial': '#8338EC',
        'Consumer': '#3A86FF'
    }
    
    # Assign colors to nodes
    colors = [node_colors.get(node, '#CCCCCC') for node in sankey_data['nodes']]
    
    # Create Sankey figure
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=sankey_data['nodes'],
            color=colors,
            customdata=[f"${v:.2f}B" if v else "" for v in 
                       [sum(val for s, val in zip(sankey_data['source'] + sankey_data['target'], 
                                                   sankey_data['value'] * 2) if s == i) or None
                        for i in range(len(sankey_data['nodes']))]],
            hovertemplate='%{label}<br>$%{value:.2f}B<extra></extra>'
        ),
        link=dict(
            source=sankey_data['source'],
            target=sankey_data['target'],
            value=sankey_data['value'],
            color='rgba(0,0,0,0.2)',
            hovertemplate='%{source.label} → %{target.label}<br>$%{value:.2f}B<extra></extra>'
        )
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, family='Arial Black')
        ),
        font=dict(size=12, family='Arial'),
        plot_bgcolor='white',
        height=600,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    # Save as HTML
    fig.write_html(output_file)
    print(f"✓ Saved Sankey diagram to {output_file}")
    
    # Also save as static image if kaleido is available
    try:
        fig.write_image(output_file.replace('.html', '.png'), width=1200, height=600)
        print(f"✓ Saved static image to {output_file.replace('.html', '.png')}")
    except:
        print("  (Install kaleido for static image export: pip install kaleido)")
    
    return fig


def generate_revenue_breakdown_table(df):
    """Generate summary table of revenue breakdown."""
    # Segment totals
    segment_totals = df.groupby('source')['value'].sum().reset_index()
    segment_totals.columns = ['Segment', 'Revenue ($B)']
    
    # End market totals
    market_totals = df.groupby('target')['value'].sum().reset_index()
    market_totals.columns = ['End Market', 'Revenue ($B)']
    
    # Calculate percentages
    total_revenue = df['value'].sum()
    segment_totals['% of Total'] = (segment_totals['Revenue ($B)'] / total_revenue * 100).round(1)
    market_totals['% of Total'] = (market_totals['Revenue ($B)'] / total_revenue * 100).round(1)
    
    print("\n📊 Revenue by Segment:")
    print(segment_totals.to_string(index=False))
    
    print("\n📊 Revenue by End Market:")
    print(market_totals.to_string(index=False))
    
    print(f"\n💰 Total Revenue: ${total_revenue:.2f}B")
    
    return segment_totals, market_totals


def main():
    parser = argparse.ArgumentParser(description='Generate Sankey revenue flow diagram')
    parser.add_argument('--data', help='Path to revenue flow CSV (optional)')
    parser.add_argument('--output', default='sankey_revenue.html', help='Output HTML file')
    parser.add_argument('--title', default='Revenue Flow: Segments to End Markets',
                       help='Chart title')
    parser.add_argument('--create-template', action='store_true',
                       help='Create sample data template')
    
    args = parser.parse_args()
    
    if args.create_template:
        print("Creating sample revenue flow template...")
        sample_df = create_sample_revenue_flow()
        sample_df.to_csv('revenue_flow_template.csv', index=False)
        print("✓ Created revenue_flow_template.csv")
        print("\n📋 Template structure:")
        print("   - source: Segment name (DRAM, NAND, Emerging)")
        print("   - target: End market (AI/Datacenter, Mobile, Enterprise, etc.)")
        print("   - value: Revenue in billions")
        print("\n💡 Edit this file with actual data, then run:")
        print(f"   python sankey_revenue.py --data revenue_flow_template.csv")
        return
    
    # Load data
    if args.data:
        df = load_revenue_flow_data(args.data)
    else:
        print("No data file provided. Using sample data for demonstration...\n")
        df = create_sample_revenue_flow()
    
    if df is None:
        return
    
    # Validate data
    required_cols = ['source', 'target', 'value']
    if not all(col in df.columns for col in required_cols):
        print(f"✗ Error: CSV must contain columns: {required_cols}")
        return
    
    # Generate breakdown table
    generate_revenue_breakdown_table(df)
    
    # Prepare Sankey data
    sankey_data = prepare_sankey_data(df)
    
    # Create diagram
    print(f"\nGenerating Sankey diagram...")
    create_sankey_diagram(sankey_data, title=args.title, output_file=args.output)
    
    print(f"\n✓ Open {args.output} in a web browser to view the interactive diagram")


if __name__ == "__main__":
    main()
