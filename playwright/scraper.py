#!/usr/bin/env python3
"""
Autoresearch Playwright - Scraping Experiment
Tests Playwright configurations for optimal speed/quality tradeoff
Modified by LLM agent each cycle
"""

import time
import json
import sys
from datetime import datetime

# =============================================================================
# CONFIG - MODIFY THIS SECTION (Agent edits here)
# =============================================================================

CONFIG = {
    "wait_until": "domcontentloaded",  # FINAL: Best wait strategy
    "timeout": 60000,                   # FINAL: 60s optimal
    "headless": True,                   # FINAL: Headless is faster
    "viewport": {"width": 1280, "height": 720},  # FINAL: Desktop viewport
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0",
}

# =============================================================================
# FIXED TEST URLS - DO NOT MODIFY
# =============================================================================

TEST_URLS = [
    ("static_doc", "https://docs.python.org/3/"),
    ("react_spa", "https://react.dev/learn/"),
    ("forum", "https://news.ycombinator.com/"),
    ("productivity", "https://www.notion.com/"),
    ("ecommerce", "https://www.shopify.com/"),
    ("vue_docs", "https://vuejs.org/guide/"),
    ("social", "https://www.reddit.com/r/MachineLearning/"),
    ("api_docs", "https://stripe.com/docs"),
    ("github", "https://github.com/torvalds/linux"),
    ("blog", "https://blog.mozilla.org/en/mozilla/"),
]

# =============================================================================
# SCRAPING FUNCTIONS
# =============================================================================

def scrape_with_playwright(url, config):
    """Scrape URL using Playwright with given config"""
    from playwright.sync_api import sync_playwright
    
    start_time = time.time()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=config["headless"])
            context = browser.new_context(
                viewport=config["viewport"],
                user_agent=config["user_agent"]
            )
            page = context.new_page()
            
            page.goto(url, wait_until=config["wait_until"], timeout=config["timeout"])
            
            # Get full HTML
            html = page.content()
            
            browser.close()
            
            elapsed = time.time() - start_time
            return {"success": True, "html": html, "time": elapsed}
    
    except Exception as e:
        elapsed = time.time() - start_time
        return {"success": False, "error": str(e), "time": elapsed}

def extract_content(html):
    """Extract clean content from HTML using trafilatura"""
    try:
        import trafilatura
        text = trafilatura.extract(html, output_format="txt") or ""
        return len(text)
    except:
        # Fallback: simple text extraction
        import re
        text = re.sub(r'<[^>]+>', '', html)
        return len(text)

def estimate_full_content_size(url):
    """Estimate what 'complete' content looks like for this URL type"""
    # Static fetch gives us baseline
    import requests
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": CONFIG["user_agent"]})
        static_text = extract_content(r.text)
        return static_text * 1.5  # Assume JS adds ~50% more content
    except:
        return 5000  # Default estimate

# =============================================================================
# MAIN EXPERIMENT
# =============================================================================

def run_experiment():
    """Run scraping experiment on all test URLs"""
    results = []
    total_start = time.time()
    
    print("=" * 70)
    print(f"Playwright Autoresearch - {datetime.now().isoformat()}")
    print("=" * 70)
    print(f"\nConfig: {json.dumps(CONFIG, indent=2)}")
    print("\n" + "-" * 70)
    
    for i, (category, url) in enumerate(TEST_URLS):
        print(f"\n[{i+1}/{len(TEST_URLS)}] {category}: {url}")
        
        # Scrape with Playwright
        scrape_result = scrape_with_playwright(url, CONFIG)
        
        if not scrape_result["success"]:
            print(f"  ERROR: {scrape_result.get('error', 'Unknown')}")
            results.append({
                "category": category,
                "url": url,
                "success": False,
                "error": scrape_result.get("error")
            })
            continue
        
        # Extract content
        extracted_chars = extract_content(scrape_result["html"])
        estimated_full = estimate_full_content_size(url)
        
        # Calculate completeness (capped at 1.0)
        completeness = min(extracted_chars / max(estimated_full, 1), 1.0)
        
        # Calculate score for this URL
        url_score = completeness / max(scrape_result["time"], 0.1)
        
        result = {
            "category": category,
            "url": url,
            "success": True,
            "time_seconds": round(scrape_result["time"], 2),
            "html_size": len(scrape_result["html"]),
            "extracted_chars": extracted_chars,
            "completeness": round(completeness, 3),
            "score": round(url_score, 3)
        }
        
        results.append(result)
        
        print(f"  Time: {result['time_seconds']:.2f}s | "
              f"Chars: {result['extracted_chars']:,} | "
              f"Complete: {result['completeness']:.1%} | "
              f"Score: {result['score']:.3f}")
    
    total_time = time.time() - total_start
    
    # Calculate aggregate metrics
    successful = [r for r in results if r.get("success")]
    
    if successful:
        avg_time = sum(r["time_seconds"] for r in successful) / len(successful)
        avg_completeness = sum(r["completeness"] for r in successful) / len(successful)
        total_score = avg_completeness / max(avg_time, 0.1)
    else:
        avg_time = 0
        avg_completeness = 0
        total_score = 0
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "config": CONFIG,
        "total_urls": len(TEST_URLS),
        "successful": len(successful),
        "total_time": round(total_time, 2),
        "avg_time": round(avg_time, 2),
        "avg_completeness": round(avg_completeness, 3),
        "total_score": round(total_score, 3),
        "results": results
    }
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Successful: {len(successful)}/{len(TEST_URLS)}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Avg time per URL: {avg_time:.2f}s")
    print(f"Avg completeness: {avg_completeness:.1%}")
    print(f"TOTAL SCORE: {total_score:.3f}")
    
    # Save results
    cycle_num = len([f for f in __import__('os').listdir('results') if f.startswith('cycle_')]) + 1
    
    with open(f"results/cycle_{cycle_num:02d}.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Append to TSV
    with open("results.tsv", "a") as f:
        if cycle_num == 1:
            f.write("cycle\ttimestamp\tscore\tavg_time\tcompleteness\tconfig\n")
        config_str = json.dumps(CONFIG)
        f.write(f"{cycle_num}\t{summary['timestamp']}\t{total_score:.3f}\t"
                f"{avg_time:.2f}\t{avg_completeness:.3f}\t{config_str}\n")
    
    print(f"\n✓ Results saved to results/cycle_{cycle_num:02d}.json")
    print(f"✓ Summary appended to results.tsv")
    
    return summary

if __name__ == "__main__":
    import os
    os.makedirs("results", exist_ok=True)
    run_experiment()
