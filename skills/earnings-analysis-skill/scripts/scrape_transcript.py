"""
Scrape earnings call transcripts from free sources.

Usage:
    python scrape_transcript.py --company "Micron" --quarter "Q2" --year "2025"
"""

import requests
from bs4 import BeautifulSoup
import argparse
import re
from datetime import datetime


def scrape_seeking_alpha(company_ticker, quarter, fiscal_year):
    """
    Scrape earnings transcript from Seeking Alpha.
    
    Args:
        company_ticker: Stock ticker (e.g., 'MU' for Micron)
        quarter: Quarter (e.g., 'Q2')
        fiscal_year: Fiscal year (e.g., '2025')
    
    Returns:
        dict with transcript text and metadata
    """
    # Seeking Alpha URL pattern (approximate - may need adjustment)
    search_url = f"https://seekingalpha.com/symbol/{company_ticker}/earnings/transcripts"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a simplified example - actual implementation would need
            # to parse Seeking Alpha's specific HTML structure
            transcript_links = soup.find_all('a', href=re.compile(r'/article/\d+-.*-earnings-call-transcript'))
            
            # Find the most recent transcript matching the quarter
            for link in transcript_links:
                if quarter.lower() in link.text.lower() and fiscal_year in link.text:
                    transcript_url = "https://seekingalpha.com" + link['href']
                    return fetch_transcript_page(transcript_url)
            
            return {"error": f"No transcript found for {company_ticker} {quarter} FY{fiscal_year}"}
        else:
            return {"error": f"Failed to access Seeking Alpha: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"Exception during scraping: {str(e)}"}


def fetch_transcript_page(url):
    """Fetch the full transcript from a specific URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract transcript text (structure varies by site)
            article = soup.find('article') or soup.find('div', class_='article-content')
            
            if article:
                # Clean up the text
                transcript_text = article.get_text(separator='\n', strip=True)
                
                return {
                    "success": True,
                    "url": url,
                    "transcript": transcript_text,
                    "fetched_at": datetime.now().isoformat()
                }
        
        return {"error": f"Failed to fetch transcript: {response.status_code}"}
        
    except Exception as e:
        return {"error": f"Exception fetching transcript: {str(e)}"}


def scrape_company_ir_site(company_name, quarter, fiscal_year):
    """
    Attempt to find transcript on company's IR website.
    
    Note: This is a template - each company's IR site has different structure.
    """
    # Company IR site mappings
    ir_sites = {
        "Micron": "https://investors.micron.com",
        "SK Hynix": "https://www.skhynix.com/investor",
        "Samsung": "https://www.samsung.com/semiconductor/investor-relations/",
        "Western Digital": "https://investor.wdc.com"
    }
    
    base_url = ir_sites.get(company_name)
    if not base_url:
        return {"error": f"IR site not configured for {company_name}"}
    
    # This would need company-specific logic
    return {
        "message": f"Manual retrieval needed from {base_url}",
        "instructions": "Navigate to Financials > Quarterly Results > Earnings Calls"
    }


def save_transcript(transcript_data, output_file):
    """Save transcript to a text file."""
    if transcript_data.get("success"):
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Earnings Call Transcript\n")
            f.write(f"Source: {transcript_data['url']}\n")
            f.write(f"Fetched: {transcript_data['fetched_at']}\n\n")
            f.write(transcript_data['transcript'])
        print(f"✓ Transcript saved to {output_file}")
        return True
    else:
        print(f"✗ Failed to save transcript: {transcript_data.get('error')}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Scrape earnings call transcripts')
    parser.add_argument('--company', required=True, help='Company name or ticker')
    parser.add_argument('--ticker', help='Stock ticker (e.g., MU for Micron)')
    parser.add_argument('--quarter', required=True, help='Quarter (e.g., Q2)')
    parser.add_argument('--year', required=True, help='Fiscal year (e.g., 2025)')
    parser.add_argument('--output', default='transcript.txt', help='Output file name')
    
    args = parser.parse_args()
    
    print(f"Searching for {args.company} {args.quarter} FY{args.year} earnings transcript...\n")
    
    # Try Seeking Alpha first (if ticker provided)
    if args.ticker:
        print(f"Attempting Seeking Alpha ({args.ticker})...")
        result = scrape_seeking_alpha(args.ticker, args.quarter, args.year)
        if result.get("success"):
            save_transcript(result, args.output)
            return
        else:
            print(f"  {result.get('error')}\n")
    
    # Fall back to company IR site
    print(f"Checking company IR site...")
    result = scrape_company_ir_site(args.company, args.quarter, args.year)
    print(f"  {result.get('message', result.get('error'))}")
    
    if result.get('instructions'):
        print(f"\n📋 {result['instructions']}")
    
    print("\n💡 Alternative: Manually download from:")
    print(f"   - Seeking Alpha: https://seekingalpha.com/symbol/{args.ticker or '...'}/earnings")
    print(f"   - Company IR site")
    print(f"   - AlphaSense (subscription required)")


if __name__ == "__main__":
    main()
