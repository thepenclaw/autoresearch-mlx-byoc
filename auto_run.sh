#!/bin/bash
cd /Users/mmadmin/Documents/GitHub/autoresearch-byoc/autoresearch-mlx-byoc

for i in {1..10}; do
    echo "========================================"
    echo "Cycle $i/10 - $(date)"
    echo "========================================"
    git pull origin main
    uv run train.py
    git add results.tsv train.py
    git commit -m "cycle-$i: $(date +%s)"
    git push origin main
    [ $i -lt 10 ] && echo "Sleeping 6 hours..." && sleep 21600
done

echo "All 10 cycles complete!"
