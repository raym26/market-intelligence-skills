#!/usr/bin/env python3
"""
Extract revenue breakdown data from memory semiconductor earnings materials.

Supports:
- Parsing earnings presentation PDFs (tabula-py)
- Manual CSV template creation
- SEC filing extraction (10-Q, 10-K)

Usage:
    python extract_revenue_data.py --pdf earnings.pdf --output revenue_data.csv
    python extract_revenue_data.py --create-template --company "Micron"
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd

# Try to import optional PDF parsing libraries
try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


# Company-specific patterns for extracting revenue data
COMPANY_PATTERNS = {
    'micron': {
        'segments': ['DRAM', 'NAND', 'Other'],
        'end_markets': ['Data Center', 'Mobile', 'Client', 'Consumer', 'Auto/Industrial', 'Embedded'],
        'revenue_keywords': ['revenue', 'net sales', 'total revenue'],
        'segment_keywords': ['by product', 'by technology', 'revenue mix'],
    },
    'sk hynix': {
        'segments': ['DRAM', 'NAND Flash', 'Others'],
        'end_markets': ['Server', 'Mobile', 'PC', 'Consumer', 'Automotive'],
        'revenue_keywords': ['revenue', 'sales', 'total revenue'],
        'segment_keywords': ['by product', 'product mix', 'business segment'],
    },
    'samsung': {
        'segments': ['Memory', 'System LSI', 'Foundry'],
        'memory_segments': ['DRAM', 'NAND Flash', 'MCP'],
        'end_markets': ['Server', 'Mobile', 'PC', 'Consumer', 'SSD'],
        'revenue_keywords': ['revenue', 'sales'],
        'segment_keywords': ['by product', 'business area'],
    },
}

# Mapping for normalizing end market names
END_MARKET_MAPPING = {
    'data center': 'AI/Datacenter',
    'datacenter': 'AI/Datacenter',
    'server': 'AI/Datacenter',
    'cloud': 'AI/Datacenter',
    'ai': 'AI/Datacenter',
    'mobile': 'Mobile',
    'smartphone': 'Mobile',
    'handset': 'Mobile',
    'client': 'PC',
    'pc': 'PC',
    'notebook': 'PC',
    'desktop': 'PC',
    'consumer': 'Consumer',
    'consumer electronics': 'Consumer',
    'auto': 'Automotive',
    'automotive': 'Automotive',
    'auto/industrial': 'Automotive',
    'industrial': 'Industrial',
    'iot': 'Industrial',
    'embedded': 'Enterprise',
    'enterprise': 'Enterprise',
    'graphics': 'PC',
}


def normalize_end_market(market_name: str) -> str:
    """Normalize end market name to standard categories."""
    lower_name = market_name.lower().strip()
    for pattern, normalized in END_MARKET_MAPPING.items():
        if pattern in lower_name:
            return normalized
    return market_name.title()


def extract_tables_from_pdf(pdf_path: str) -> list:
    """Extract tables from PDF using tabula-py."""
    if not TABULA_AVAILABLE:
        print("Error: tabula-py not installed. Run: pip install tabula-py")
        return []

    try:
        # Extract all tables from PDF
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        print(f"Found {len(tables)} tables in PDF")
        return tables
    except Exception as e:
        print(f"Error extracting tables: {e}")
        return []


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF using PyPDF2."""
    if not PYPDF2_AVAILABLE:
        print("Error: PyPDF2 not installed. Run: pip install PyPDF2")
        return ""

    try:
        text = ""
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""


def find_revenue_tables(tables: list, company: str = None) -> list:
    """Find tables that likely contain revenue data."""
    revenue_tables = []

    patterns = COMPANY_PATTERNS.get(company.lower() if company else 'micron', COMPANY_PATTERNS['micron'])

    for i, table in enumerate(tables):
        if table is None or table.empty:
            continue

        # Convert to string for pattern matching
        table_str = table.to_string().lower()

        # Check for revenue keywords
        has_revenue = any(kw in table_str for kw in patterns['revenue_keywords'])
        has_segments = any(seg.lower() in table_str for seg in patterns['segments'])

        if has_revenue or has_segments:
            revenue_tables.append({
                'index': i,
                'table': table,
                'has_revenue': has_revenue,
                'has_segments': has_segments,
            })

    return revenue_tables


def parse_revenue_values(text: str) -> dict:
    """Parse revenue values from text using regex patterns."""
    values = {}

    # Pattern for dollar amounts (e.g., $6.75B, $6,750M, 6.75 billion)
    dollar_pattern = r'\$?([\d,]+\.?\d*)\s*(B|billion|M|million)?'

    # Pattern for percentages
    percent_pattern = r'(\d+\.?\d*)\s*%'

    # Try to extract segment revenues
    segments = ['DRAM', 'NAND', 'Other', 'Emerging']
    for segment in segments:
        # Look for patterns like "DRAM: $6.75B" or "DRAM revenue of $6.75 billion"
        pattern = rf'{segment}[:\s]+.*?\$?([\d,]+\.?\d*)\s*(B|billion|M|million)?'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1).replace(',', ''))
            unit = match.group(2)
            if unit and unit.upper() in ['M', 'MILLION']:
                value /= 1000  # Convert to billions
            values[segment] = value

    return values


def create_company_template(company: str, output_path: str = None):
    """Create a revenue data template for a specific company."""
    company_lower = company.lower()
    patterns = COMPANY_PATTERNS.get(company_lower, COMPANY_PATTERNS['micron'])

    if output_path is None:
        output_path = f"{company_lower.replace(' ', '_')}_revenue_template.csv"

    segments = patterns['segments']
    end_markets = ['AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive']

    # Create template data
    with open(output_path, 'w') as f:
        f.write(f"# {company} Revenue Flow Template\n")
        f.write("# Fill in revenue values in billions USD\n")
        f.write("#\n")
        f.write("source,target,value\n")
        f.write("#\n")
        f.write("# Layer 1: Total Revenue to Segments\n")
        for seg in segments:
            f.write(f"Total Revenue,{seg},0.0\n")
        f.write("#\n")
        for seg in segments:
            if seg.lower() in ['other', 'others']:
                continue
            f.write(f"# Layer 2: {seg} to End Markets\n")
            for market in end_markets:
                f.write(f"{seg},{market},0.0\n")
            f.write("#\n")

    print(f"Created template: {output_path}")
    print(f"\nTemplate for {company}:")
    print(f"  Segments: {', '.join(segments)}")
    print(f"  End Markets: {', '.join(end_markets)}")
    print("\nEdit the file with actual revenue values from earnings materials.")

    return output_path


def interactive_data_entry(company: str = None) -> pd.DataFrame:
    """Interactive mode for entering revenue data."""
    print("\n" + "="*60)
    print("INTERACTIVE REVENUE DATA ENTRY")
    print("="*60)

    if company:
        print(f"\nEntering data for: {company}")

    # Get total revenue
    try:
        total_revenue = float(input("\nTotal Revenue (in billions, e.g., 8.7): $"))
    except ValueError:
        print("Invalid input. Using 0.")
        total_revenue = 0

    # Get segment breakdown
    print("\n--- Segment Revenue Breakdown ---")
    segments = {}
    for seg in ['DRAM', 'NAND', 'Emerging/Other']:
        try:
            value = float(input(f"  {seg} revenue (billions, or 0 to skip): $"))
            if value > 0:
                segments[seg.replace('/Other', '')] = value
        except ValueError:
            pass

    # Get end market breakdown for each segment
    print("\n--- End Market Revenue Breakdown ---")
    print("(Enter revenue in billions for each segment→market flow)")

    flows = []
    end_markets = ['AI/Datacenter', 'Mobile', 'Enterprise', 'PC', 'Automotive', 'Other']

    for seg, seg_total in segments.items():
        print(f"\n{seg} (total: ${seg_total:.2f}B):")
        remaining = seg_total
        for market in end_markets:
            if remaining <= 0:
                break
            try:
                value = float(input(f"  → {market} (remaining: ${remaining:.2f}B): $"))
                if value > 0:
                    flows.append({'source': seg, 'target': market, 'value': value})
                    remaining -= value
            except ValueError:
                pass

    # Create DataFrame
    df_data = []

    # Add layer 1 flows (Total → Segments)
    for seg, value in segments.items():
        df_data.append({'source': 'Total Revenue', 'target': seg, 'value': value})

    # Add layer 2 flows (Segments → Markets)
    df_data.extend(flows)

    return pd.DataFrame(df_data)


def extract_from_pdf(pdf_path: str, company: str = None, output_path: str = None) -> pd.DataFrame:
    """Main function to extract revenue data from PDF."""
    print(f"\nExtracting revenue data from: {pdf_path}")

    if not os.path.exists(pdf_path):
        print(f"Error: File not found: {pdf_path}")
        return None

    # Extract tables
    tables = extract_tables_from_pdf(pdf_path)

    if not tables:
        print("No tables found. Trying text extraction...")
        text = extract_text_from_pdf(pdf_path)
        if text:
            values = parse_revenue_values(text)
            if values:
                print(f"Found revenue values in text: {values}")
            else:
                print("Could not automatically extract revenue data.")
                print("Please use --create-template to create a manual entry template.")
        return None

    # Find revenue tables
    revenue_tables = find_revenue_tables(tables, company)

    if not revenue_tables:
        print("No revenue tables identified. Tables found:")
        for i, table in enumerate(tables):
            if table is not None and not table.empty:
                print(f"\nTable {i}:")
                print(table.head())
        print("\nPlease manually review tables and create CSV from template.")
        return None

    print(f"\nFound {len(revenue_tables)} potential revenue tables:")
    for rt in revenue_tables:
        print(f"\nTable {rt['index']}:")
        print(rt['table'])

    print("\nNote: Automatic parsing may require manual verification.")
    print("Consider using --create-template for manual data entry.")

    return None


def main():
    parser = argparse.ArgumentParser(
        description='Extract revenue data from memory semiconductor earnings materials',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --pdf earnings.pdf --company "Micron"
  %(prog)s --create-template --company "SK Hynix"
  %(prog)s --interactive --company "Micron" --output micron_q2.csv
        """
    )
    parser.add_argument('--pdf', '-p', help='Path to earnings PDF')
    parser.add_argument('--company', '-c', help='Company name (Micron, SK Hynix, Samsung)')
    parser.add_argument('--output', '-o', help='Output CSV file path')
    parser.add_argument('--create-template', action='store_true',
                        help='Create template CSV for manual data entry')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Interactive data entry mode')
    parser.add_argument('--list-tables', action='store_true',
                        help='List all tables found in PDF')

    args = parser.parse_args()

    # Create template
    if args.create_template:
        company = args.company or 'Micron'
        create_company_template(company, args.output)
        return 0

    # Interactive mode
    if args.interactive:
        df = interactive_data_entry(args.company)
        if df is not None and not df.empty:
            output = args.output or 'revenue_data.csv'
            df.to_csv(output, index=False)
            print(f"\nSaved to: {output}")
            print(df)
        return 0

    # Extract from PDF
    if args.pdf:
        df = extract_from_pdf(args.pdf, args.company, args.output)
        if df is not None and not df.empty:
            output = args.output or 'revenue_data.csv'
            df.to_csv(output, index=False)
            print(f"\nSaved to: {output}")
        return 0

    # No action specified
    print("Usage: Specify --pdf, --create-template, or --interactive")
    print("Run with --help for more information.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
