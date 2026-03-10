#!/bin/bash
# Auto-Research Runner - 10 cycles, 6-hour gaps
# Karpathy BYOC Method on M4 Mac

cd /Users/mmadmin/Documents/GitHub/autoresearch-mlx-byoc

echo "=========================================="
echo "Starting Auto-Research: $(date)"
echo "=========================================="

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# Prepare data (one-time)
if [ ! -d "$HOME/.cache/autoresearch" ]; then
    echo "Preparing data (one-time setup)..."
    uv run prepare.py
fi

# Run 10 cycles
for i in {1..10}; do
    echo ""
    echo "=========================================="
    echo "CYCLE $i/10 - $(date)"
    echo "=========================================="
    
    # Pull latest code (in case you modified it)
    git pull origin main
    
    # Run experiment (~5 minutes)
    echo "Running train.py (5 min budget)..."
    uv run train.py
    
    # Push results
    git add results.tsv train.py
    git commit -m "Cycle-$i: $(date +%Y%m%d-%H%M%S)"
    git push origin main
    
    echo "Cycle $i complete. Results pushed."
    
    # Wait 6 hours (except after last cycle)
    if [ $i -lt 10 ]; then
        echo "Sleeping 6 hours until next cycle..."
        sleep 21600  # 6 hours = 21600 seconds
    fi
done

echo ""
echo "=========================================="
echo "ALL 10 CYCLES COMPLETE! $(date)"
echo "=========================================="
