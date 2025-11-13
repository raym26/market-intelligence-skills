#!/usr/bin/env python3
"""
Track Competitor News Script
Monitors news feeds for competitor updates to keep battle cards current.

Usage:
    python track_news.py --company "Micron" --days 180
    python track_news.py --ticker "MU" --keywords "HBM,AI,datacenter"
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests package not installed.", file=sys.stderr)
    print("Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


def search_company_news(company: str, ticker: str, days: int = 180) -> list:
    """
    Search for recent company news from various sources.

    Args:
        company: Company name
        ticker: Stock ticker
        days: Number of days to look back

    Returns:
        list: News articles
    """
    articles = []

    # In production, you would use news APIs like:
    # - NewsAPI (https://newsapi.org/)
    # - Alpha Vantage News
    # - Yahoo Finance API
    # - Google News RSS
    # - Company RSS feeds

    print(f"Searching news for {company} ({ticker}) - last {days} days...")
    print("\n💡 Note: Implement news API integration for production use")
    print("   Suggested APIs: NewsAPI, Alpha Vantage, Yahoo Finance, Google News RSS")

    # Placeholder structure for what articles would look like
    sample_article = {
        "title": "Example: Micron Announces HBM3E Production Ramp",
        "date": datetime.now().isoformat(),
        "source": "Example Source",
        "url": "https://example.com",
        "summary": "Summary of the news article...",
        "category": "product_launch",  # product_launch, financial, strategic, leadership, etc.
        "relevance_score": 8  # 1-10 scale
    }

    return articles


def categorize_news(articles: list) -> dict:
    """
    Categorize news articles by type.

    Args:
        articles: List of news articles

    Returns:
        dict: Articles organized by category
    """
    categories = {
        "strategic": [],
        "product_launches": [],
        "financial": [],
        "leadership": [],
        "partnerships": [],
        "manufacturing": [],
        "customers": [],
        "technology": [],
        "other": []
    }

    # Keywords for categorization
    category_keywords = {
        "strategic": ["acquisition", "merger", "strategy", "investment", "expansion"],
        "product_launches": ["launch", "announce", "unveil", "introduce", "new product"],
        "financial": ["earnings", "revenue", "margin", "profit", "guidance"],
        "leadership": ["ceo", "cfo", "executive", "appoint", "hire", "resignation"],
        "partnerships": ["partnership", "collaboration", "agreement", "deal"],
        "manufacturing": ["fab", "factory", "capacity", "production", "yield"],
        "customers": ["customer", "win", "contract", "design win", "nvidia", "amd"],
        "technology": ["hbm", "dram", "nand", "node", "process", "technology"]
    }

    for article in articles:
        title_lower = article.get("title", "").lower()
        summary_lower = article.get("summary", "").lower()
        text = f"{title_lower} {summary_lower}"

        categorized = False
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                categories[category].append(article)
                categorized = True
                break

        if not categorized:
            categories["other"].append(article)

    return categories


def filter_by_keywords(articles: list, keywords: list) -> list:
    """
    Filter articles by specific keywords.

    Args:
        articles: List of articles
        keywords: Keywords to filter by

    Returns:
        list: Filtered articles
    """
    filtered = []

    for article in articles:
        title = article.get("title", "").lower()
        summary = article.get("summary", "").lower()
        text = f"{title} {summary}"

        if any(keyword.lower() in text for keyword in keywords):
            filtered.append(article)

    return filtered


def generate_recent_developments_section(articles: list, limit: int = 10) -> str:
    """
    Generate "Recent Developments" section for battle card.

    Args:
        articles: List of news articles
        limit: Maximum number of items to include

    Returns:
        str: Formatted section in markdown
    """
    if not articles:
        return "No recent developments found.\n"

    # Sort by date (most recent first)
    sorted_articles = sorted(
        articles,
        key=lambda x: x.get("date", ""),
        reverse=True
    )[:limit]

    output = ["## Recent Developments (Last 6 Months)\n"]

    # Group by category
    categorized = categorize_news(sorted_articles)

    for category, items in categorized.items():
        if items:
            output.append(f"\n**{category.replace('_', ' ').title()}:**")
            for article in items:
                date = article.get("date", "")[:10]  # YYYY-MM-DD
                title = article.get("title", "")
                summary = article.get("summary", "")

                if summary:
                    output.append(f"- [{date}]: {title} - {summary[:100]}...")
                else:
                    output.append(f"- [{date}]: {title}")

    return "\n".join(output)


def create_sample_news_data():
    """Create sample news data for demonstration."""
    sample_news = [
        {
            "date": (datetime.now() - timedelta(days=30)).isoformat(),
            "title": "Micron Announces HBM3E Volume Production",
            "source": "Company Press Release",
            "category": "product_launch",
            "summary": "Micron announces mass production of HBM3E for AI datacenter applications",
            "relevance": 9
        },
        {
            "date": (datetime.now() - timedelta(days=60)).isoformat(),
            "title": "Micron Receives $6.1B CHIPS Act Funding",
            "source": "Government Announcement",
            "category": "strategic",
            "summary": "US government awards Micron $6.1B to expand domestic manufacturing",
            "relevance": 8
        },
        {
            "date": (datetime.now() - timedelta(days=90)).isoformat(),
            "title": "Micron Reports Q4 FY24 Results - Revenue Up 25% YoY",
            "source": "Earnings Release",
            "category": "financial",
            "summary": "Strong quarter driven by memory market recovery and AI demand",
            "relevance": 7
        }
    ]

    return sample_news


def main():
    parser = argparse.ArgumentParser(
        description="Track competitor news for battle cards"
    )
    parser.add_argument(
        "--company",
        type=str,
        help="Company name (e.g., 'Micron')"
    )
    parser.add_argument(
        "--ticker",
        type=str,
        help="Stock ticker (e.g., 'MU')"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=180,
        help="Number of days to look back (default: 180)"
    )
    parser.add_argument(
        "--keywords",
        type=str,
        help="Comma-separated keywords to filter (e.g., 'HBM,AI,datacenter')"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="recent_developments.json",
        help="Output JSON file (default: recent_developments.json)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "markdown"],
        default="json",
        help="Output format: json or markdown"
    )

    args = parser.parse_args()

    if not args.company or not args.ticker:
        parser.print_help()
        print("\n💡 Running with sample data for demonstration...\n")
        articles = create_sample_news_data()
        company = "Micron"
        ticker = "MU"
    else:
        company = args.company
        ticker = args.ticker
        # Search for news (would use real API in production)
        articles = search_company_news(company, ticker, args.days)

        # If no articles found, use sample data
        if not articles:
            print("\n⚠️  No articles found. Using sample data.\n")
            articles = create_sample_news_data()

    print(f"\n{'='*60}")
    print(f"Tracking News: {company} ({ticker})")
    print(f"Period: Last {args.days} days")
    print(f"{'='*60}\n")

    # Filter by keywords if provided
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
        print(f"Filtering by keywords: {', '.join(keywords)}")
        articles = filter_by_keywords(articles, keywords)

    print(f"Found {len(articles)} relevant articles\n")

    # Categorize articles
    categorized = categorize_news(articles)

    print("📰 Articles by category:")
    for category, items in categorized.items():
        if items:
            print(f"   {category}: {len(items)} articles")

    # Output results
    if args.format == "json":
        output_data = {
            "company": company,
            "ticker": ticker,
            "period_days": args.days,
            "total_articles": len(articles),
            "categorized": {k: len(v) for k, v in categorized.items()},
            "articles": articles
        }

        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✅ News data saved to: {args.output}")

    elif args.format == "markdown":
        markdown_output = generate_recent_developments_section(articles)
        output_file = args.output.replace(".json", ".md")

        with open(output_file, "w") as f:
            f.write(markdown_output)

        print(f"\n✅ Markdown section saved to: {output_file}")
        print("\nCopy this section into your battle card 'Recent Developments' section.")

    print("\n💡 Integration Tips:")
    print("   - Set up NewsAPI account for automated news tracking")
    print("   - Configure RSS feeds from company IR sites")
    print("   - Run this script weekly to update battle cards")
    print("   - Use keywords to focus on relevant topics (HBM, AI, etc.)")


if __name__ == "__main__":
    main()
