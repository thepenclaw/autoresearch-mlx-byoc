#!/usr/bin/env python3
"""
OpenClaw Memory & Context - TRUE AUTORESEARCH (REAL URLs)
Karpathy Method: Cycle → Evaluate → Improve → Next Cycle
"""

import json
import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

# REAL OPENCLAW URLs - From github.com/openclaw/openclaw
EXPERIMENT_STATE = {
    "version": "1.0.0",
    "topic": "OpenClaw Memory & Context Issues",
    "hypothesis": "OpenClaw context compression and session management are the main pain points",
    "cycles_completed": 0,
    "total_cycles": 10,
    "findings": {"memory_issues": [], "context_issues": [], "solutions": [], "patterns": []},
    "scraper_performance": {"success_rate": [], "failed_sites": []},
    "current_strategy": {"site_priority": [], "failed_sites": []}
}

# REAL URLs from github.com/openclaw/openclaw
BATCHES = {
    1: {
        "name": "official-docs",
        "focus": "OpenClaw official documentation",
        "sites": [
            ("docs-main", "https://docs.openclaw.ai"),
            ("docs-getting-started", "https://docs.openclaw.ai/start/getting-started"),
            ("docs-faq", "https://docs.openclaw.ai/start/faq"),
            ("docs-showcase", "https://docs.openclaw.ai/start/showcase"),
            ("docs-wizard", "https://docs.openclaw.ai/start/wizard"),
            ("docs-install", "https://docs.openclaw.ai/install"),
            ("docs-updating", "https://docs.openclaw.ai/install/updating"),
            ("docs-docker", "https://docs.openclaw.ai/install/docker"),
            ("docs-channels", "https://docs.openclaw.ai/channels"),
            ("docs-skills", "https://docs.openclaw.ai/skills"),
        ]
    },
    2: {
        "name": "github-main",
        "focus": "OpenClaw GitHub repository main pages",
        "sites": [
            ("gh-repo", "https://github.com/openclaw/openclaw"),
            ("gh-readme", "https://github.com/openclaw/openclaw/blob/main/README.md"),
            ("gh-changelog", "https://github.com/openclaw/openclaw/blob/main/CHANGELOG.md"),
            ("gh-license", "https://github.com/openclaw/openclaw/blob/main/LICENSE"),
            ("gh-issues", "https://github.com/openclaw/openclaw/issues"),
            ("gh-pulls", "https://github.com/openclaw/openclaw/pulls"),
            ("gh-discussions", "https://github.com/openclaw/openclaw/discussions"),
            ("gh-releases", "https://github.com/openclaw/openclaw/releases"),
            ("gh-wiki", "https://github.com/openclaw/openclaw/wiki"),
            ("gh-actions", "https://github.com/openclaw/openclaw/actions"),
        ]
    },
    3: {
        "name": "github-issues-memory",
        "focus": "GitHub issues related to memory/context",
        "sites": [
            ("gh-issues-memory", "https://github.com/openclaw/openclaw/issues?q=memory"),
            ("gh-issues-context", "https://github.com/openclaw/openclaw/issues?q=context"),
            ("gh-issues-session", "https://github.com/openclaw/openclaw/issues?q=session"),
            ("gh-issues-compression", "https://github.com/openclaw/openclaw/issues?q=compression"),
            ("gh-issues-tokens", "https://github.com/openclaw/openclaw/issues?q=tokens"),
            ("gh-issues-history", "https://github.com/openclaw/openclaw/issues?q=history"),
            ("gh-issues-limit", "https://github.com/openclaw/openclaw/issues?q=limit"),
            ("gh-issues-window", "https://github.com/openclaw/openclaw/issues?q=window"),
            ("gh-issues-optimize", "https://github.com/openclaw/openclaw/issues?q=optimize"),
            ("gh-issues-performance", "https://github.com/openclaw/openclaw/issues?q=performance"),
        ]
    },
    4: {
        "name": "github-discussions",
        "focus": "GitHub discussions for solutions",
        "sites": [
            ("gh-discuss-general", "https://github.com/openclaw/openclaw/discussions/categories/general"),
            ("gh-discuss-q-a", "https://github.com/openclaw/openclaw/discussions/categories/q-a"),
            ("gh-discuss-ideas", "https://github.com/openclaw/openclaw/discussions/categories/ideas"),
            ("gh-discuss-show-tell", "https://github.com/openclaw/openclaw/discussions/categories/show-and-tell"),
            ("gh-discuss-memory", "https://github.com/openclaw/openclaw/discussions?discussions_q=memory"),
            ("gh-discuss-context", "https://github.com/openclaw/openclaw/discussions?discussions_q=context"),
            ("gh-discuss-session", "https://github.com/openclaw/openclaw/discussions?discussions_q=session"),
            ("gh-discuss-config", "https://github.com/openclaw/openclaw/discussions?discussions_q=config"),
            ("gh-discuss-help", "https://github.com/openclaw/openclaw/discussions?discussions_q=help"),
            ("gh-discuss-error", "https://github.com/openclaw/openclaw/discussions?discussions_q=error"),
        ]
    },
    5: {
        "name": "docs-advanced",
        "focus": "Advanced OpenClaw documentation",
        "sites": [
            ("docs-agents", "https://docs.openclaw.ai/agents"),
            ("docs-sessions", "https://docs.openclaw.ai/sessions"),
            ("docs-channels-main", "https://docs.openclaw.ai/channels"),
            ("docs-skills-main", "https://docs.openclaw.ai/skills"),
            ("docs-tools", "https://docs.openclaw.ai/tools"),
            ("docs-gateway", "https://docs.openclaw.ai/gateway"),
            ("docs-workspace", "https://docs.openclaw.ai/workspace"),
            ("docs-security", "https://docs.openclaw.ai/security"),
            ("docs-config", "https://docs.openclaw.ai/config"),
            ("docs-environment", "https://docs.openclaw.ai/config/environment"),
        ]
    },
    6: {
        "name": "community-discord",
        "focus": "Community resources and Discord",
        "sites": [
            ("openclaw-website", "https://openclaw.ai"),
            ("discord-invite", "https://discord.gg/clawd"),
            ("deepwiki", "https://deepwiki.com/openclaw/openclaw"),
            ("docs-nix", "https://github.com/openclaw/nix-openclaw"),
            ("gh-examples", "https://github.com/openclaw/examples"),
            ("gh-showcase", "https://github.com/openclaw/awesome-openclaw"),
            ("gh-templates", "https://github.com/openclaw/templates"),
            ("gh-extensions", "https://github.com/openclaw/extensions"),
            ("gh-docs", "https://github.com/openclaw/docs"),
            ("gh-community", "https://github.com/openclaw/community"),
        ]
    },
    7: {
        "name": "pull-requests",
        "focus": "GitHub PRs for code solutions",
        "sites": [
            ("gh-prs-memory", "https://github.com/openclaw/openclaw/pulls?q=memory"),
            ("gh-prs-context", "https://github.com/openclaw/openclaw/pulls?q=context"),
            ("gh-prs-session", "https://github.com/openclaw/openclaw/pulls?q=session"),
            ("gh-prs-compression", "https://github.com/openclaw/openclaw/pulls?q=compression"),
            ("gh-prs-fix", "https://github.com/openclaw/openclaw/pulls?q=fix"),
            ("gh-prs-optimize", "https://github.com/openclaw/openclaw/pulls?q=optimize"),
            ("gh-prs-improve", "https://github.com/openclaw/openclaw/pulls?q=improve"),
            ("gh-prs-refactor", "https://github.com/openclaw/openclaw/pulls?q=refactor"),
            ("gh-prs-feature", "https://github.com/openclaw/openclaw/pulls?q=feature"),
            ("gh-prs-bugfix", "https://github.com/openclaw/openclaw/pulls?q=bugfix"),
        ]
    },
    8: {
        "name": "releases-changelog",
        "focus": "Releases and changelog for updates",
        "sites": [
            ("gh-releases-all", "https://github.com/openclaw/openclaw/releases"),
            ("gh-release-latest", "https://github.com/openclaw/openclaw/releases/latest"),
            ("gh-tags", "https://github.com/openclaw/openclaw/tags"),
            ("gh-commits-main", "https://github.com/openclaw/openclaw/commits/main"),
            ("gh-commits-history", "https://github.com/openclaw/openclaw/commits/main/CHANGELOG.md"),
            ("gh-blame-readme", "https://github.com/openclaw/openclaw/blame/main/README.md"),
            ("gh-blame-changelog", "https://github.com/openclaw/openclaw/blame/main/CHANGELOG.md"),
            ("gh-network", "https://github.com/openclaw/openclaw/network"),
            ("gh-contributors", "https://github.com/openclaw/openclaw/graphs/contributors"),
            ("gh-insights", "https://github.com/openclaw/openclaw/pulse"),
        ]
    },
    9: {
        "name": "pattern-validation",
        "focus": "Validate findings (ADAPTIVE)",
        "sites": []  # Will be populated based on cycles 1-8
    },
    10: {
        "name": "synthesis",
        "focus": "Final synthesis (ADAPTIVE)",
        "sites": []  # Will be populated based on all cycles
    }
}

def save_state():
    with open("experiment_state.json", "w") as f:
        json.dump(EXPERIMENT_STATE, f, indent=2)

def load_state():
    global EXPERIMENT_STATE
    if os.path.exists("experiment_state.json"):
        with open("experiment_state.json", "r") as f:
            EXPERIMENT_STATE = json.load(f)
        return True
    return False

def scrape_site(name, url):
    """Scrape single site"""
    try:
        import trafilatura
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            html = page.content()
            title = page.title()
            browser.close()
            
            markdown = trafilatura.extract(html, output_format="markdown") or ""
            
            return {"name": name, "url": url, "title": title, "chars": len(markdown), "success": True}
    except Exception as e:
        return {"name": name, "url": url, "error": str(e), "success": False}

def analyze_content(content):
    """Extract insights from content"""
    content = content.lower()
    insights = {"memory": [], "context": [], "session": [], "compression": []}
    
    patterns = {
        "memory": ["memory", "ram", "oom", "out of memory", "memory leak"],
        "context": ["context", "context window", "token limit", "truncat", "compress"],
        "session": ["session", "history", "conversation", "chat history"],
        "compression": ["compress", "compact", "reduce", "optimize", "efficient"]
    }
    
    for category, keywords in patterns.items():
        for keyword in keywords:
            if keyword in content:
                insights[category].append(keyword)
    
    return insights

def evaluate_cycle(cycle_num, results):
    """Evaluate cycle and update strategy"""
    print(f"\n{'='*60}")
    print(f"CYCLE {cycle_num} EVALUATION")
    print(f"{'='*60}")
    
    successful = sum(1 for r in results if r.get("success"))
    total = len(results)
    
    print(f"Success: {successful}/{total} ({successful/total*100:.0f}%)")
    
    # Track findings
    for r in results:
        if r.get("success") and r.get("chars", 0) > 1000:
            EXPERIMENT_STATE["current_strategy"]["site_priority"].append({
                "name": r["name"], "url": r["url"], "chars": r["chars"], "cycle": cycle_num
            })
        elif not r.get("success"):
            EXPERIMENT_STATE["current_strategy"]["failed_sites"].append({
                "name": r["name"], "url": r["url"], "error": r.get("error", ""), "cycle": cycle_num
            })
    
    EXPERIMENT_STATE["cycles_completed"] = cycle_num
    save_state()
    
    # Recommendations
    if cycle_num < 9:
        print(f"\n💡 Next: {BATCHES[cycle_num+1]['name']} - {BATCHES[cycle_num+1]['focus']}")

def commit_cycle(cycle_num, batch_name):
    """Commit to git"""
    branch = f"cycle-{cycle_num:02d}-{batch_name}"
    subprocess.run(["git", "checkout", "-b", branch], capture_output=True)
    subprocess.run(["git", "add", "-A"], capture_output=True)
    subprocess.run(["git", "commit", "-m", f"Cycle {cycle_num}: {batch_name}"], capture_output=True)
    subprocess.run(["git", "push", "origin", branch], capture_output=True)
    subprocess.run(["git", "checkout", "main"], capture_output=True)
    print(f"✓ Committed: {branch}")

def run_cycle(cycle_num):
    """Run single cycle"""
    if cycle_num not in BATCHES:
        return
    
    batch = BATCHES[cycle_num]
    print(f"\n{'#'*60}")
    print(f"CYCLE {cycle_num}: {batch['name'].upper()}")
    print(f"{'#'*60}")
    
    results = []
    for i, (name, url) in enumerate(batch["sites"], 1):
        print(f"[{i}/{len(batch['sites'])}] {name}...", end=" ", flush=True)
        result = scrape_site(name, url)
        results.append(result)
        
        if result["success"]:
            print(f"✓ {result['chars']:,} chars")
        else:
            print(f"✗ {result.get('error', 'failed')[:30]}")
        
        time.sleep(2)
    
    evaluate_cycle(cycle_num, results)
    commit_cycle(cycle_num, batch["name"])

def main():
    if not load_state():
        print("🚀 Starting OpenClaw autoresearch")
        save_state()
    
    print(f"\n📋 Topic: {EXPERIMENT_STATE['topic']}")
    print(f"🎯 Hypothesis: {EXPERIMENT_STATE['hypothesis']}")
    
    start = EXPERIMENT_STATE["cycles_completed"] + 1
    
    for cycle in range(start, 11):
        run_cycle(cycle)
        if cycle < 10:
            time.sleep(5)
    
    print(f"\n🎉 Complete! {EXPERIMENT_STATE['cycles_completed']} cycles done.")

if __name__ == "__main__":
    main()
