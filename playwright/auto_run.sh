#!/bin/bash
# Autoresearch Playwright - 10 Cycles, 6-Hour Gaps
# Runs on M4 Mac automatically

cd "$(dirname "$0")"
REPO_DIR="$(pwd)"

echo "========================================"
echo "Autoresearch Playwright - Starting"
echo "Time: $(date)"
echo "Directory: $REPO_DIR"
echo "========================================"

# Check dependencies
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found"
    exit 1
fi

# Install/check dependencies
echo "Checking dependencies..."
pip3 install -q playwright trafilatura requests 2>/dev/null || echo "Note: pip install may require user action"

# Check if playwright browsers are installed
if ! python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    echo "Installing Playwright browsers (one-time)..."
    python3 -m playwright install chromium
fi

# Run 10 cycles
for i in {1..10}; do
    echo ""
    echo "========================================"
    echo "CYCLE $i/10"
    echo "Started: $(date)"
    echo "========================================"
    
    # Pull latest code (in case Kimi pushed new config)
    echo "Pulling latest code..."
    git pull origin main
    
    # Run experiment
    echo "Running scraper.py..."
    python3 scraper.py
    
    # Push results
    echo "Pushing results..."
    git add results/ results.tsv scraper.py
    git commit -m "Cycle-$i results: $(date +%Y%m%d-%H%M%S)"
    git push origin main
    
    echo "Cycle $i complete!"
    
    # If not last cycle, sleep 6 hours
    if [ $i -lt 10 ]; then
        echo ""
        echo "Sleeping 15 minutes until next cycle..."
        echo "Next cycle starts at: $(date -v+15M)"
        sleep 900  # 6 hours = 21600 seconds
    fi
done

echo ""
echo "========================================"
echo "ALL 10 CYCLES COMPLETE!"
echo "Finished: $(date)"
echo "========================================"
echo ""
echo "Final results in: results.tsv"
echo "Individual cycles in: results/"
