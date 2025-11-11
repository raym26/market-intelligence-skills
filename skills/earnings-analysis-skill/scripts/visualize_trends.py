"""
Generate visualizations for earnings analysis.

Usage:
    python visualize_trends.py --data historical_data.csv
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def load_data(file_path):
    """Load historical data."""
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def plot_revenue_trend(df, output_file='revenue_trend.png'):
    """Plot revenue trend over time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot total revenue
    ax.plot(df['Date'], df['Revenue_Total_B'], marker='o', linewidth=2, 
            label='Total Revenue', color='#2E86AB')
    
    # Plot segments if available
    if 'Revenue_DRAM_B' in df.columns:
        ax.plot(df['Date'], df['Revenue_DRAM_B'], marker='s', linewidth=1.5,
                label='DRAM Revenue', color='#A23B72', linestyle='--')
    if 'Revenue_NAND_B' in df.columns:
        ax.plot(df['Date'], df['Revenue_NAND_B'], marker='^', linewidth=1.5,
                label='NAND Revenue', color='#F18F01', linestyle='--')
    
    ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
    ax.set_ylabel('Revenue ($B)', fontsize=12, fontweight='bold')
    ax.set_title('Quarterly Revenue Trend', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved revenue trend to {output_file}")
    plt.close()


def plot_margin_trend(df, output_file='margin_trend.png'):
    """Plot margin trends over time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot margins
    if 'Gross_Margin_Pct' in df.columns:
        ax.plot(df['Date'], df['Gross_Margin_Pct'], marker='o', linewidth=2,
                label='Gross Margin', color='#06A77D')
    if 'Operating_Margin_Pct' in df.columns:
        ax.plot(df['Date'], df['Operating_Margin_Pct'], marker='s', linewidth=2,
                label='Operating Margin', color='#D62839')
    
    ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
    ax.set_ylabel('Margin (%)', fontsize=12, fontweight='bold')
    ax.set_title('Quarterly Margin Trend', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))
    plt.xticks(rotation=45)
    
    # Add shaded region for industry average (example)
    # ax.axhspan(30, 40, alpha=0.1, color='gray', label='Industry Range')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved margin trend to {output_file}")
    plt.close()


def plot_segment_mix(df, output_file='segment_mix.png'):
    """Plot segment revenue mix as stacked area chart."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if 'Revenue_DRAM_B' in df.columns and 'Revenue_NAND_B' in df.columns:
        # Calculate other (if any)
        df_plot = df.copy()
        df_plot['Other'] = df_plot['Revenue_Total_B'] - df_plot['Revenue_DRAM_B'] - df_plot['Revenue_NAND_B']
        
        # Create stacked area plot
        ax.fill_between(df_plot['Date'], 0, df_plot['Revenue_DRAM_B'], 
                        label='DRAM', alpha=0.7, color='#A23B72')
        ax.fill_between(df_plot['Date'], df_plot['Revenue_DRAM_B'], 
                        df_plot['Revenue_DRAM_B'] + df_plot['Revenue_NAND_B'],
                        label='NAND', alpha=0.7, color='#F18F01')
        if df_plot['Other'].sum() > 0:
            ax.fill_between(df_plot['Date'], 
                           df_plot['Revenue_DRAM_B'] + df_plot['Revenue_NAND_B'],
                           df_plot['Revenue_Total_B'],
                           label='Other', alpha=0.7, color='#C2C5BB')
        
        ax.set_xlabel('Quarter', fontsize=12, fontweight='bold')
        ax.set_ylabel('Revenue ($B)', fontsize=12, fontweight='bold')
        ax.set_title('Segment Revenue Mix', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved segment mix to {output_file}")
        plt.close()


def plot_bit_asp_analysis(df, output_file='bit_asp_analysis.png'):
    """Plot bit growth vs ASP changes for DRAM and NAND."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # DRAM analysis
    if 'DRAM_Bit_Growth_QoQ' in df.columns and 'DRAM_ASP_Change_QoQ' in df.columns:
        quarters = [f"Q{row['Quarter']} FY{row['Fiscal_Year']}" for _, row in df.iterrows()]
        
        x = range(len(df))
        width = 0.35
        
        ax1.bar([i - width/2 for i in x], df['DRAM_Bit_Growth_QoQ'], width, 
                label='Bit Growth', color='#2E86AB', alpha=0.8)
        ax1.bar([i + width/2 for i in x], df['DRAM_ASP_Change_QoQ'], width,
                label='ASP Change', color='#F18F01', alpha=0.8)
        
        ax1.set_xlabel('Quarter', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Change (%)', fontsize=11, fontweight='bold')
        ax1.set_title('DRAM: Bit Growth vs ASP', fontsize=12, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(quarters, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # NAND analysis
    if 'NAND_Bit_Growth_QoQ' in df.columns and 'NAND_ASP_Change_QoQ' in df.columns:
        ax2.bar([i - width/2 for i in x], df['NAND_Bit_Growth_QoQ'], width,
                label='Bit Growth', color='#2E86AB', alpha=0.8)
        ax2.bar([i + width/2 for i in x], df['NAND_ASP_Change_QoQ'], width,
                label='ASP Change', color='#F18F01', alpha=0.8)
        
        ax2.set_xlabel('Quarter', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Change (%)', fontsize=11, fontweight='bold')
        ax2.set_title('NAND: Bit Growth vs ASP', fontsize=12, fontweight='bold')
        ax2.set_xticks(x)
        ax2.set_xticklabels(quarters, rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved bit/ASP analysis to {output_file}")
    plt.close()


def create_dashboard(df, output_file='earnings_dashboard.png'):
    """Create comprehensive dashboard with all key metrics."""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Revenue trend
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(df['Date'], df['Revenue_Total_B'], marker='o', linewidth=2.5,
            color='#2E86AB', markersize=8)
    ax1.set_ylabel('Revenue ($B)', fontsize=11, fontweight='bold')
    ax1.set_title('Quarterly Revenue', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))
    
    # Margins
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(df['Date'], df['Gross_Margin_Pct'], marker='o', linewidth=2,
            label='Gross', color='#06A77D')
    ax2.plot(df['Date'], df['Operating_Margin_Pct'], marker='s', linewidth=2,
            label='Operating', color='#D62839')
    ax2.set_ylabel('Margin (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Margin Trends', fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Segment mix
    ax3 = fig.add_subplot(gs[1, 1])
    latest = df.iloc[-1]
    segments = []
    values = []
    colors = ['#A23B72', '#F18F01', '#C2C5BB']
    
    if 'Revenue_DRAM_B' in df.columns:
        segments.append('DRAM')
        values.append(latest['Revenue_DRAM_B'])
    if 'Revenue_NAND_B' in df.columns:
        segments.append('NAND')
        values.append(latest['Revenue_NAND_B'])
    other = latest['Revenue_Total_B'] - sum(values)
    if other > 0:
        segments.append('Other')
        values.append(other)
    
    ax3.pie(values, labels=segments, autopct='%1.1f%%', startangle=90,
           colors=colors[:len(segments)])
    ax3.set_title(f'Latest Quarter Mix\n({latest["Quarter"]} FY{latest["Fiscal_Year"]})',
                 fontsize=13, fontweight='bold')
    
    # DRAM bit/ASP
    ax4 = fig.add_subplot(gs[2, 0])
    if 'DRAM_Bit_Growth_QoQ' in df.columns:
        quarters = [f"Q{row['Quarter']}" for _, row in df.iterrows()]
        x = range(len(df))
        width = 0.35
        ax4.bar([i - width/2 for i in x], df['DRAM_Bit_Growth_QoQ'], width,
               label='Bits', color='#2E86AB', alpha=0.8)
        ax4.bar([i + width/2 for i in x], df['DRAM_ASP_Change_QoQ'], width,
               label='ASP', color='#F18F01', alpha=0.8)
        ax4.set_ylabel('QoQ Change (%)', fontsize=10, fontweight='bold')
        ax4.set_title('DRAM Bit/ASP Growth', fontsize=12, fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels(quarters)
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')
        ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    # CapEx trend
    ax5 = fig.add_subplot(gs[2, 1])
    if 'CapEx_B' in df.columns:
        ax5.bar(df['Date'], df['CapEx_B'], color='#717568', alpha=0.7)
        ax5.set_ylabel('CapEx ($B)', fontsize=11, fontweight='bold')
        ax5.set_title('Capital Expenditure', fontsize=13, fontweight='bold')
        ax5.grid(True, alpha=0.3, axis='y')
        ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y-Q%q'))
    
    plt.suptitle('Earnings Analysis Dashboard', fontsize=16, fontweight='bold', y=0.995)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved dashboard to {output_file}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Generate earnings analysis visualizations')
    parser.add_argument('--data', required=True, help='Path to historical data CSV')
    parser.add_argument('--output-dir', default='.', help='Output directory for charts')
    parser.add_argument('--charts', nargs='+', 
                       choices=['revenue', 'margin', 'segment', 'bitasp', 'dashboard', 'all'],
                       default=['all'], help='Which charts to generate')
    
    args = parser.parse_args()
    
    print(f"Loading data from {args.data}...\n")
    df = load_data(args.data)
    
    import os
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    charts_to_generate = args.charts
    if 'all' in charts_to_generate:
        charts_to_generate = ['revenue', 'margin', 'segment', 'bitasp', 'dashboard']
    
    print("Generating visualizations...\n")
    
    if 'revenue' in charts_to_generate:
        plot_revenue_trend(df, os.path.join(output_dir, 'revenue_trend.png'))
    
    if 'margin' in charts_to_generate:
        plot_margin_trend(df, os.path.join(output_dir, 'margin_trend.png'))
    
    if 'segment' in charts_to_generate:
        plot_segment_mix(df, os.path.join(output_dir, 'segment_mix.png'))
    
    if 'bitasp' in charts_to_generate:
        plot_bit_asp_analysis(df, os.path.join(output_dir, 'bit_asp_analysis.png'))
    
    if 'dashboard' in charts_to_generate:
        create_dashboard(df, os.path.join(output_dir, 'earnings_dashboard.png'))
    
    print(f"\n✓ All visualizations saved to {output_dir}/")


if __name__ == "__main__":
    main()
