# AI Code Metrics Framework

A comprehensive framework for measuring AI coding assistant effectiveness, with a focus on Claude Code and other terminal-based AI coding assistants.

## Features

- Collect and analyze productivity metrics for AI-assisted coding
- Track API costs and calculate ROI
- Monitor code quality and security metrics
- Visualize metrics with Grafana dashboards
- Secure and private data handling

## Quick Start

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (for metrics infrastructure)
- Git repository to analyze

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-code-metrics.git
cd ai-code-metrics

# Set up with uv
uv init
uv add prometheus-client gitpython pylint coverage pytest flask tiktoken cryptography

# Start metrics infrastructure
docker-compose up -d
```

### Basic Usage

```python
from ai_code_metrics.collectors import MetricsCollector

# Initialize the metrics collector
collector = MetricsCollector()

# Track AI-assisted functions
@collector.track_function(ai_assisted=True)
def my_ai_assisted_function():
    # Your AI-assisted code here
    pass

# Use in your workflows
my_ai_assisted_function()
```

## Metrics Infrastructure

The metrics infrastructure uses:
- **Prometheus**: Time series database for metrics storage
- **Grafana**: Visualization and dashboards

Access the dashboards at:
- Grafana: http://localhost:3000 (default: admin/admin123)
- Prometheus: http://localhost:9090

## Documentation

See the [docs](./docs) directory for detailed documentation:

- [Research Plan](./docs/research/Research%20Plan.md)
- [Literature Review](./docs/research/Literature%20Review%20%26%20Existing%20Framework%20Analysis%20for%20Claude%20Code%20Evaluation%20Framework.md)
- [Implementation Plan](./docs/research/AI%20Coding%20Assistant%20Metrics%20Framework:%20Complete%20Implementation%20Plan.md)

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.