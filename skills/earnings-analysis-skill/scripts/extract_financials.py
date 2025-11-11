"""
Extract financial data tables from earnings presentation PDFs.

Usage:
    python extract_financials.py --pdf "Micron_Q2FY25_Earnings.pdf"
"""

import argparse
import pandas as pd
import re
try:
    import tabula
except ImportError:
    print("⚠️  tabula-py not installed. Install with: pip install tabula-py")
    tabula = None

try:
    import PyPDF2
except ImportError:
    print("⚠️  PyPDF2 not installed. Install with: pip install PyPDF2")
    PyPDF2 = None


def extract_tables_with_tabula(pdf_path):
    """
    Extract tables from PDF using tabula-py.
    
    Returns:
        List of DataFrames containing extracted tables
    """
    if not tabula:
        return None
    
    try:
        # Extract all tables from PDF
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        print(f"✓ Extracted {len(tables)} tables from PDF")
        return tables
    except Exception as e:
        print(f"✗ Error extracting tables: {str(e)}")
        return None


def identify_financial_tables(tables):
    """
    Identify which tables contain key financial metrics.
    
    Returns:
        dict with categorized tables
    """
    categorized = {
        'income_statement': None,
        'segment_revenue': None,
        'guidance': None,
        'balance_sheet': None,
        'cash_flow': None
    }
    
    if not tables:
        return categorized
    
    # Keywords to identify table types
    keywords = {
        'income_statement': ['revenue', 'gross margin', 'operating income', 'net income'],
        'segment_revenue': ['dram', 'nand', 'segment'],
        'guidance': ['guidance', 'outlook', 'forecast'],
        'balance_sheet': ['assets', 'liabilities', 'equity', 'cash'],
        'cash_flow': ['operating activities', 'investing', 'financing', 'capex']
    }
    
    for i, table in enumerate(tables):
        # Convert table to string for keyword matching
        table_text = str(table).lower()
        
        for category, words in keywords.items():
            if any(word in table_text for word in words):
                if categorized[category] is None:  # Take first match
                    categorized[category] = table
                    print(f"  ✓ Identified {category} (table {i+1})")
    
    return categorized


def extract_key_metrics(financial_tables):
    """
    Extract specific metrics from identified tables.
    
    Returns:
        dict with standardized financial metrics
    """
    metrics = {
        'revenue_total': None,
        'revenue_dram': None,
        'revenue_nand': None,
        'gross_margin': None,
        'operating_margin': None,
        'capex': None,
        'guidance_revenue': None,
        'guidance_margin': None
    }
    
    # This is a simplified example - actual implementation would need
    # robust parsing logic for different PDF formats
    
    if financial_tables['income_statement'] is not None:
        df = financial_tables['income_statement']
        # Look for revenue row
        revenue_rows = df[df.apply(lambda row: row.astype(str).str.contains('revenue|net sales', case=False).any(), axis=1)]
        if not revenue_rows.empty:
            # Extract most recent quarter value (typically first numeric column)
            try:
                metrics['revenue_total'] = extract_first_number(revenue_rows.iloc[0])
            except:
                pass
    
    # Similar logic for other metrics...
    
    return metrics


def extract_first_number(row):
    """Extract the first meaningful number from a pandas Series."""
    for val in row:
        if isinstance(val, (int, float)) and not pd.isna(val):
            return val
        # Try to extract number from string
        if isinstance(val, str):
            numbers = re.findall(r'[\d,]+\.?\d*', val.replace(',', ''))
            if numbers:
                try:
                    return float(numbers[0])
                except:
                    pass
    return None


def manual_pdf_text_extraction(pdf_path):
    """
    Fall back to text extraction if tabula fails.
    """
    if not PyPDF2:
        return None
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
        print(f"✓ Extracted text from {len(reader.pages)} pages")
        return text
    except Exception as e:
        print(f"✗ Error extracting text: {str(e)}")
        return None


def parse_text_for_metrics(text):
    """
    Use regex to find key metrics in extracted text.
    """
    metrics = {}
    
    # Pattern examples (would need refinement for actual PDFs)
    patterns = {
        'revenue': r'revenue.*?[\$]?\s*([\d,]+\.?\d*)\s*(?:million|billion)',
        'gross_margin': r'gross\s+margin.*?([\d]+\.?\d*)%',
        'operating_margin': r'operating\s+margin.*?([\d]+\.?\d*)%',
    }
    
    for metric, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics[metric] = match.group(1)
    
    return metrics


def save_extracted_data(data, output_file):
    """Save extracted financial data to CSV."""
    if isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        df = data
    
    df.to_csv(output_file, index=False)
    print(f"✓ Saved extracted data to {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Extract financial tables from earnings PDF')
    parser.add_argument('--pdf', required=True, help='Path to earnings presentation PDF')
    parser.add_argument('--output', default='financial_data.csv', help='Output CSV file')
    parser.add_argument('--method', choices=['tabula', 'text', 'both'], default='both',
                       help='Extraction method')
    
    args = parser.parse_args()
    
    print(f"Processing {args.pdf}...\n")
    
    tables = None
    text = None
    
    if args.method in ['tabula', 'both']:
        print("Attempting table extraction with tabula...")
        tables = extract_tables_with_tabula(args.pdf)
        
        if tables:
            categorized = identify_financial_tables(tables)
            metrics = extract_key_metrics(categorized)
            
            print("\n📊 Extracted Metrics:")
            for key, value in metrics.items():
                if value is not None:
                    print(f"   {key}: {value}")
            
            # Save the first few tables for manual review
            for i, table in enumerate(tables[:5]):
                table.to_csv(f"table_{i+1}.csv", index=False)
            print(f"\n✓ Saved first {min(5, len(tables))} tables as CSV files")
    
    if args.method in ['text', 'both'] or (args.method == 'both' and not tables):
        print("\nAttempting text extraction...")
        text = manual_pdf_text_extraction(args.pdf)
        
        if text:
            metrics = parse_text_for_metrics(text)
            print("\n📊 Metrics from text:")
            for key, value in metrics.items():
                print(f"   {key}: {value}")
            
            # Save full text for manual review
            with open('extracted_text.txt', 'w', encoding='utf-8') as f:
                f.write(text)
            print("✓ Saved full text to extracted_text.txt")
    
    print("\n💡 Note: Automatic extraction may require manual verification.")
    print("   Review the extracted tables and compare with the original PDF.")


if __name__ == "__main__":
    main()
