# Using AI Code Metrics with Claude Code

This guide provides specific instructions for tracking and analyzing Claude Code usage within your development workflow.

## Identifying Claude Code Contributions

The framework automatically recognizes Claude Code contributions by looking for the standard signatures in commit messages:

```
🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

When commits include these signatures, they are properly attributed to Claude Code in metrics and reports.

## Basic Usage with Claude Code

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-code-metrics.git
cd ai-code-metrics

# Set up with uv
uv init
uv sync --all-extras --dev
```

### 2. Analyzing Claude Code Usage

Run the analyzer against your Git repository:

```bash
uv run python examples/track_ai_usage.py /path/to/your/repo
```

This will generate a report of all AI usage, including Claude Code-specific metrics.

### 3. Integrating with Your Workflow

To incorporate metrics collection into your ongoing development:

1. Add the decorator to functions where you use Claude Code:

```python
from ai_code_metrics.collectors import MetricsCollector

collector = MetricsCollector()

@collector.track_function(ai_assisted=True)
def implement_feature():
    # Your Claude Code-assisted implementation
    pass
```

2. Run the metrics dashboard periodically:

```bash
uv run python scripts/create_dashboard.py --repo-path /path/to/your/repo
```

## Claude Code Performance Analysis

### Productivity Metrics

Measure your productivity improvements with Claude Code by tracking:

- Time to complete tasks with and without Claude Code
- Lines of code generated per hour
- Number of iterations to reach a working solution
- Success rate for different task types

### Code Quality Metrics

Assess the quality of Claude Code-generated code:

- Linting scores
- Test coverage
- Cyclomatic complexity
- Security vulnerabilities

### Cost Analysis

Calculate the ROI of using Claude Code:

```bash
uv run python -m ai_code_metrics.cli roi --days 30 --hourly-rate 75
```

## Best Practices for Claude Code Metrics

1. **Always commit with Claude Code signature** - This ensures accurate attribution

2. **Track function-level metrics** - Use the decorators to get granular performance data

3. **Run regular analysis** - Set up a weekly job to generate reports

4. **Compare over time** - Track improvements as Claude models evolve

5. **Share metrics with team** - Use the dashboard to demonstrate value

## Example: Tracking a Claude Code Session

```bash
# Start timing a Claude Code session
SESSION_START=$(date +%s)

# Use Claude Code to implement a feature
# ...

# End timing
SESSION_END=$(date +%s)
DURATION=$((SESSION_END - SESSION_START))

# Record metrics
echo "{\"timestamp\": $(date +%s), \"duration\": $DURATION, \"ai_assisted\": true, \"model\": \"claude-4-sonnet\", \"task\": \"feature-implementation\"}" >> ~/.ai_metrics/manual_timing_$(date +%Y-%m-%d).jsonl

# Commit with proper attribution
git commit -m "Implement feature X

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Dashboard Integration

The metrics framework can generate dashboards showing Claude Code impact over time. View them at:

- Grafana dashboard: http://localhost:3000 (when running metrics infrastructure)
- Static HTML reports: Generated in the `dashboard/` directory