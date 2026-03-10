# Autoresearch Playwright - Agent Instructions

## Goal

Optimize Playwright configuration for web scraping on Apple Silicon M4. Find the best speed vs extraction quality tradeoff.

## Metric

**Score = extraction_completeness / time_seconds**

Higher is better. We want maximum content extraction in minimum time.

## What You CAN Modify

Edit **`scraper.py`** only. Specifically these sections:

### 1. CONFIG section (lines 15-30)
```python
CONFIG = {
    "wait_until": "networkidle",  # Change to: "load", "domcontentloaded", "networkidle"
    "timeout": 30000,             # Change to: 5000, 10000, 20000, 30000, 60000
    "headless": True,             # Change to: True or False
    "viewport": {"width": 1280, "height": 720},  # Change dimensions
    "user_agent": "Mozilla/5.0...",  # Change or use None for default
}
```

### 2. Extraction Logic (lines 80-100)
You can modify how content is extracted:
- Change trafilatura parameters
- Add custom extraction logic
- Modify preprocessing

## What You CANNOT Modify

- **`TEST_URLS`** - Fixed set of 10 URLs (static + JS-heavy mix)
- **Evaluation function** - How completeness is measured
- **`prepare.py`** - Data preparation (if exists)
- **Test URL list** - Must remain constant for fair comparison

## Experiment Rules

1. **One change per cycle** - Don't change 5 things at once
2. **Hypothesis-driven** - Have a reason for each change
3. **Document in commit** - Explain what you changed and why
4. **Revert if worse** - If score drops, try opposite direction

## Test URLs (Fixed)

```python
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
```

## Strategy Guidelines

### Early Cycles (1-3): Explore
- Test extremes: very fast timeouts vs very long
- Compare "load" vs "networkidle"
- Test headless vs headed

### Middle Cycles (4-7): Exploit
- Focus on promising configs
- Fine-tune timeout values
- Test viewport variations

### Late Cycles (8-10): Verify
- Confirm best config works across all URL types
- Test robustness
- Document findings

## Analysis Checklist

Before pushing new experiment, ask:
- [ ] What was the previous score?
- [ ] What change am I making?
- [ ] Why will this improve the score?
- [ ] What do I expect to happen?

## Success Criteria

After 10 cycles, we want:
1. **Best config identified** - Optimal wait_until, timeout, headless combo
2. **Tradeoff understood** - Speed vs quality curve
3. **Reproducible** - Anyone can run same config, get same results

## Output Format

Commit messages should follow:
```
Cycle-X: Brief description

Hypothesis: What I think will happen
Change: What I modified
Expected: Expected outcome
```
