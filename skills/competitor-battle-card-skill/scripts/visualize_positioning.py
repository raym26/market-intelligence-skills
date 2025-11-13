#!/usr/bin/env python3
"""
Visualize Competitive Positioning Script
Creates charts and visualizations for competitor battle cards.

Usage:
    python visualize_positioning.py --dimensions "technology,cost,hbm_share"
    python visualize_positioning.py --type "scatter" --x-axis "technology" --y-axis "cost"
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
except ImportError:
    print("Error: Required packages not installed.", file=sys.stderr)
    print("Install with: pip install matplotlib pandas plotly", file=sys.stderr)
    sys.exit(1)


def load_positioning_data(data_file: str = "positioning_data.json") -> dict:
    """
    Load competitive positioning data from JSON file.

    Args:
        data_file: Path to JSON data file

    Returns:
        dict: Positioning data
    """
    if not Path(data_file).exists():
        print(f"Warning: Data file not found: {data_file}", file=sys.stderr)
        return create_sample_data()

    with open(data_file, "r") as f:
        return json.load(f)


def create_sample_data() -> dict:
    """Create sample positioning data for demonstration."""
    return {
        "competitors": ["Micron", "Samsung", "SK Hynix"],
        "dimensions": {
            "technology_leadership": [7, 9, 8.5],  # 1-10 scale
            "manufacturing_cost": [6, 9, 8],  # Lower is better (inverted for plotting)
            "hbm_market_share": [10, 25, 60],  # Percentage
            "dram_market_share": [23, 42, 29],  # Percentage
            "financial_strength": [7, 9, 8],  # 1-10 scale
            "customer_relationships": [8, 8, 9],  # 1-10 scale
            "innovation_speed": [7, 8, 9]  # 1-10 scale
        }
    }


def create_radar_chart(data: dict, output: str = "radar_chart.html"):
    """
    Create radar chart for multi-dimensional competitive positioning.

    Args:
        data: Positioning data
        output: Output HTML file path
    """
    competitors = data["competitors"]
    dimensions = data["dimensions"]

    # Create plotly radar chart
    fig = go.Figure()

    categories = list(dimensions.keys())

    for i, competitor in enumerate(competitors):
        values = [dimensions[cat][i] for cat in categories]
        # Close the radar chart by repeating first value
        values = values + [values[0]]
        categories_closed = categories + [categories[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories_closed,
            fill='toself',
            name=competitor
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=True,
        title="Competitive Positioning: Multi-Dimensional Analysis"
    )

    fig.write_html(output)
    print(f"✅ Radar chart saved: {output}")


def create_scatter_plot(data: dict, x_axis: str, y_axis: str, output: str = "scatter_plot.html"):
    """
    Create 2D scatter plot comparing competitors on two dimensions.

    Args:
        data: Positioning data
        x_axis: Dimension for X axis
        y_axis: Dimension for Y axis
        output: Output HTML file path
    """
    competitors = data["competitors"]
    dimensions = data["dimensions"]

    if x_axis not in dimensions or y_axis not in dimensions:
        print(f"Error: Dimensions {x_axis} or {y_axis} not found in data", file=sys.stderr)
        return

    x_values = dimensions[x_axis]
    y_values = dimensions[y_axis]

    # Create scatter plot
    fig = go.Figure()

    for i, competitor in enumerate(competitors):
        fig.add_trace(go.Scatter(
            x=[x_values[i]],
            y=[y_values[i]],
            mode='markers+text',
            name=competitor,
            text=[competitor],
            textposition="top center",
            marker=dict(size=20)
        ))

    fig.update_layout(
        title=f"Competitive Positioning: {x_axis} vs {y_axis}",
        xaxis_title=x_axis.replace("_", " ").title(),
        yaxis_title=y_axis.replace("_", " ").title(),
        showlegend=True
    )

    fig.write_html(output)
    print(f"✅ Scatter plot saved: {output}")


def create_market_share_chart(data: dict, output: str = "market_share.html"):
    """
    Create market share visualization.

    Args:
        data: Positioning data
        output: Output HTML file path
    """
    competitors = data["competitors"]
    dimensions = data["dimensions"]

    # Create grouped bar chart for different market segments
    segments = ["hbm_market_share", "dram_market_share"]

    fig = go.Figure()

    for segment in segments:
        if segment in dimensions:
            fig.add_trace(go.Bar(
                name=segment.replace("_", " ").title(),
                x=competitors,
                y=dimensions[segment]
            ))

    fig.update_layout(
        title="Market Share Comparison by Segment",
        xaxis_title="Competitor",
        yaxis_title="Market Share (%)",
        barmode='group'
    )

    fig.write_html(output)
    print(f"✅ Market share chart saved: {output}")


def create_positioning_matrix(data: dict, output: str = "positioning_matrix.png"):
    """
    Create 2x2 positioning matrix (Technology vs Cost).

    Args:
        data: Positioning data
        output: Output PNG file path
    """
    competitors = data["competitors"]
    dimensions = data["dimensions"]

    tech_scores = dimensions.get("technology_leadership", [5, 5, 5])
    cost_scores = dimensions.get("manufacturing_cost", [5, 5, 5])

    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot competitors
    for i, competitor in enumerate(competitors):
        ax.scatter(tech_scores[i], cost_scores[i], s=500, alpha=0.6)
        ax.annotate(competitor, (tech_scores[i], cost_scores[i]),
                   ha='center', va='center', fontsize=12, fontweight='bold')

    # Draw quadrant lines
    ax.axhline(y=5, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=5, color='gray', linestyle='--', alpha=0.5)

    # Label quadrants
    ax.text(7.5, 7.5, 'Leaders', fontsize=14, ha='center', alpha=0.3)
    ax.text(2.5, 7.5, 'Cost Leaders', fontsize=14, ha='center', alpha=0.3)
    ax.text(7.5, 2.5, 'Tech Leaders', fontsize=14, ha='center', alpha=0.3)
    ax.text(2.5, 2.5, 'Challenged', fontsize=14, ha='center', alpha=0.3)

    ax.set_xlabel('Technology Leadership →', fontsize=12)
    ax.set_ylabel('Manufacturing Cost Efficiency →', fontsize=12)
    ax.set_title('Competitive Positioning Matrix', fontsize=16, fontweight='bold')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"✅ Positioning matrix saved: {output}")


def create_all_visualizations(data: dict):
    """Create all standard visualizations."""
    print("\n🎨 Creating visualizations...\n")

    create_radar_chart(data, "positioning_radar.html")
    create_scatter_plot(data, "technology_leadership", "manufacturing_cost",
                       "tech_vs_cost.html")
    create_market_share_chart(data, "market_share.html")
    create_positioning_matrix(data, "positioning_matrix.png")

    print("\n✅ All visualizations created!")


def main():
    parser = argparse.ArgumentParser(
        description="Visualize competitive positioning for battle cards"
    )
    parser.add_argument(
        "--data",
        type=str,
        default="positioning_data.json",
        help="Path to positioning data JSON file"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["radar", "scatter", "market_share", "matrix", "all"],
        default="all",
        help="Type of visualization to create"
    )
    parser.add_argument(
        "--x-axis",
        type=str,
        help="X-axis dimension for scatter plot"
    )
    parser.add_argument(
        "--y-axis",
        type=str,
        help="Y-axis dimension for scatter plot"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path"
    )

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"Visualizing Competitive Positioning")
    print(f"{'='*60}\n")

    # Load data
    data = load_positioning_data(args.data)

    if not data:
        print("Error: No data available", file=sys.stderr)
        sys.exit(1)

    # Create visualizations based on type
    if args.type == "all":
        create_all_visualizations(data)
    elif args.type == "radar":
        output = args.output or "positioning_radar.html"
        create_radar_chart(data, output)
    elif args.type == "scatter":
        if not args.x_axis or not args.y_axis:
            print("Error: --x-axis and --y-axis required for scatter plot", file=sys.stderr)
            sys.exit(1)
        output = args.output or "scatter_plot.html"
        create_scatter_plot(data, args.x_axis, args.y_axis, output)
    elif args.type == "market_share":
        output = args.output or "market_share.html"
        create_market_share_chart(data, output)
    elif args.type == "matrix":
        output = args.output or "positioning_matrix.png"
        create_positioning_matrix(data, output)

    print("\n💡 Note: Using sample data. Create positioning_data.json with actual data.")


if __name__ == "__main__":
    main()
