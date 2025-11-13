#!/usr/bin/env python3
"""
Extract Financials Script
Extracts financial data from 10-K/10-Q PDFs for competitor battle cards.

Usage:
    python extract_financials.py --filing "MU-10K-2024.pdf"
    python extract_financials.py --ticker "MU" --year 2024 --type "10-K"
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import pdfplumber
    import PyPDF2
except ImportError:
    print("Error: Required packages not installed.", file=sys.stderr)
    print("Install with: pip install pdfplumber PyPDF2", file=sys.stderr)
    sys.exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from PDF.

    Args:
        pdf_path: Path to PDF file

    Returns:
        str: Extracted text
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting PDF text: {e}", file=sys.stderr)

    return text


def extract_financial_metrics(text: str) -> dict:
    """
    Extract key financial metrics from 10-K/10-Q text.

    Args:
        text: Extracted text from PDF

    Returns:
        dict: Financial metrics
    """
    metrics = {
        "total_revenue": None,
        "memory_revenue": None,
        "dram_revenue": None,
        "nand_revenue": None,
        "gross_margin": None,
        "operating_margin": None,
        "rd_spending": None,
        "capex": None,
        "net_income": None
    }

    # Patterns to search for (customize based on company formats)
    patterns = {
        "total_revenue": r"Total revenue[\s:]+\$?([\d,]+)",
        "gross_margin": r"Gross margin[\s:]+(\d+\.?\d*)%",
        "operating_margin": r"Operating margin[\s:]+(\d+\.?\d*)%",
        "rd_spending": r"Research and development[\s:]+\$?([\d,]+)",
        "capex": r"Capital expenditures?[\s:]+\$?([\d,]+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1).replace(",", "")
            metrics[key] = value

    return metrics


def extract_segment_revenue(text: str) -> dict:
    """
    Extract revenue by segment (DRAM, NAND, etc.) from filing.

    Args:
        text: Extracted text from PDF

    Returns:
        dict: Segment revenue breakdown
    """
    segments = {
        "dram": None,
        "nand": None,
        "emerging": None
    }

    # Memory semiconductor companies often have segment tables
    # Customize patterns based on how specific companies report segments

    # Example patterns (adjust for each company)
    dram_patterns = [
        r"DRAM[\s:]+\$?([\d,]+)",
        r"Compute and Networking[\s:]+\$?([\d,]+)",  # Micron terminology
        r"Memory[\s:]+\$?([\d,]+)"
    ]

    for pattern in dram_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            segments["dram"] = match.group(1).replace(",", "")
            break

    # Similar for NAND
    nand_patterns = [
        r"NAND[\s:]+\$?([\d,]+)",
        r"Storage[\s:]+\$?([\d,]+)"
    ]

    for pattern in nand_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            segments["nand"] = match.group(1).replace(",", "")
            break

    return segments


def extract_tables_from_pdf(pdf_path: str) -> list:
    """
    Extract tables from PDF (useful for structured financial data).

    Args:
        pdf_path: Path to PDF file

    Returns:
        list: List of extracted tables
    """
    tables = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:  # Skip empty tables
                        tables.append({
                            "page": page_num + 1,
                            "data": table
                        })
    except Exception as e:
        print(f"Error extracting tables: {e}", file=sys.stderr)

    return tables


def find_financial_statement_tables(tables: list) -> dict:
    """
    Identify and parse key financial statement tables.

    Args:
        tables: List of extracted tables

    Returns:
        dict: Parsed financial statements
    """
    statements = {
        "income_statement": None,
        "balance_sheet": None,
        "cash_flow": None
    }

    # Look for tables containing financial statement keywords
    for table_info in tables:
        table = table_info["data"]
        if not table or len(table) < 2:
            continue

        # Check first few rows for statement type indicators
        header_text = " ".join([str(cell) for row in table[:3] for cell in row if cell]).lower()

        if "income" in header_text or "operations" in header_text:
            statements["income_statement"] = table
        elif "balance sheet" in header_text or "assets" in header_text:
            statements["balance_sheet"] = table
        elif "cash flow" in header_text:
            statements["cash_flow"] = table

    return statements


def main():
    parser = argparse.ArgumentParser(
        description="Extract financial data from 10-K/10-Q PDFs"
    )
    parser.add_argument(
        "--filing",
        type=str,
        help="Path to 10-K or 10-Q PDF file"
    )
    parser.add_argument(
        "--ticker",
        type=str,
        help="Stock ticker (for auto-downloading from SEC EDGAR)"
    )
    parser.add_argument(
        "--year",
        type=int,
        help="Fiscal year"
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["10-K", "10-Q"],
        help="Filing type"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="financials.json",
        help="Output JSON file (default: financials.json)"
    )

    args = parser.parse_args()

    if not args.filing and not (args.ticker and args.year and args.type):
        parser.print_help()
        print("\nError: Provide either --filing or (--ticker, --year, --type)", file=sys.stderr)
        sys.exit(1)

    # If ticker provided, user would need to download from SEC EDGAR first
    # (or implement auto-download functionality)
    if args.ticker:
        print(f"Note: Auto-download from SEC EDGAR not yet implemented.", file=sys.stderr)
        print(f"Please download {args.type} for {args.ticker} manually and use --filing", file=sys.stderr)
        sys.exit(1)

    pdf_path = args.filing
    if not Path(pdf_path).exists():
        print(f"Error: File not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Extracting Financials from: {pdf_path}")
    print(f"{'='*60}\n")

    # Extract text
    print("📄 Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    if not text:
        print("Error: No text extracted from PDF", file=sys.stderr)
        sys.exit(1)

    print(f"   Extracted {len(text)} characters")

    # Extract financial metrics
    print("\n💰 Extracting financial metrics...")
    metrics = extract_financial_metrics(text)

    # Extract segment revenue
    print("📊 Extracting segment revenue...")
    segments = extract_segment_revenue(text)

    # Extract tables
    print("📋 Extracting tables...")
    tables = extract_tables_from_pdf(pdf_path)
    print(f"   Found {len(tables)} tables")

    # Find financial statements
    print("🔍 Identifying financial statement tables...")
    statements = find_financial_statement_tables(tables)

    # Combine results
    output = {
        "source_file": pdf_path,
        "metrics": metrics,
        "segments": segments,
        "tables_found": len(tables),
        "statements": {
            "income_statement_found": statements["income_statement"] is not None,
            "balance_sheet_found": statements["balance_sheet"] is not None,
            "cash_flow_found": statements["cash_flow"] is not None
        }
    }

    # Save to JSON
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Financial data extracted to: {args.output}")

    # Print summary
    print("\n📈 Summary:")
    for key, value in metrics.items():
        if value:
            print(f"   {key}: {value}")

    print("\n💡 Note: Extraction patterns may need customization for specific companies")
    print("   Review the output file and adjust regex patterns as needed.")


if __name__ == "__main__":
    main()
