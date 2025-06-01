# Contributing to AI Code Metrics

Thank you for your interest in contributing to AI Code Metrics! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-code-metrics.git
cd ai-code-metrics
```

2. Set up the development environment:
```bash
# Install uv if you don't have it already
pip install uv

# Initialize the project
uv init

# Install all dependencies including development dependencies
uv sync --all-extras --dev
```

3. Install the package in development mode:
```bash
uv pip install -e .
```

## Development Workflow

### Code Style

This project uses:
- [Black](https://github.com/psf/black) for code formatting
- [Ruff](https://github.com/astral-sh/ruff) for linting
- [MyPy](https://github.com/python/mypy) for type checking

Before submitting a PR, please make sure your code passes all style checks:

```bash
# Run formatters
uv run black src/ tests/

# Run linters
uv run ruff check src/ tests/

# Run type checking
uv run mypy src/
```

### Testing

Write tests for new features and bug fixes. Run the test suite before submitting a PR:

```bash
uv run pytest
```

For test coverage:

```bash
uv run coverage run -m pytest
uv run coverage report
```

## Pull Request Process

1. Fork the repository and create a new branch for your feature or bugfix
2. Make your changes
3. Ensure code passes all tests and style checks
4. Submit a pull request with a clear description of the changes
5. Include information about AI assistance if applicable

## AI Assistance Tracking

This project tracks AI-assisted development. If you've used an AI coding assistant like Claude Code, GitHub Copilot, etc., please:

1. Include the AI assistant's signature in relevant commits:
   ```
   🤖 Generated with [Claude Code](https://claude.ai/code)
   
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

2. Mark the "AI Assistance" checkbox in your PR description
3. Provide an estimate of how much of the contribution was AI-assisted

This information helps us track the effectiveness of AI-assisted development and serves as valuable data for the project.

## Adding New Metrics

When adding new metrics to track:

1. Add the collector in `src/ai_code_metrics/collectors/`
2. Add any necessary analysis in `src/ai_code_metrics/analyzers/`
3. Include proper tests in `tests/`
4. Update the documentation in `docs/`
5. Consider adding a Grafana dashboard visualization if applicable

## Documentation

Update documentation when you change functionality. This includes:

- Code docstrings (Google style)
- README and other markdown files
- Example usage scripts

## Questions?

If you have any questions or need help with your contribution, please open an issue or reach out to the maintainers.