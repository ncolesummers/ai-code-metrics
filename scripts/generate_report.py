#!/usr/bin/env python3
"""Generate a metrics report for this repository."""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our package
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_code_metrics.analyzers import CommitAnalyzer
from ai_code_metrics.config import config


def main():
    """Generate a report for this repository."""
    # Get this repository path
    repo_path = Path(__file__).parent.parent
    
    print(f"Analyzing repository: {repo_path}")
    
    try:
        # Create the metrics directory if it doesn't exist
        metrics_path = config.get_metrics_path()
        metrics_path.mkdir(exist_ok=True)
        
        # Analyze repository
        analyzer = CommitAnalyzer(str(repo_path))
        stats = analyzer.get_ai_usage_stats()
        
        # Print summary
        print("\nRepository AI Usage Summary")
        print("==========================")
        print(f"Total commits: {stats['total_commits']}")
        print(f"AI-assisted commits: {stats['ai_assisted_commits']} ({stats['ai_percentage']}%)")
        
        if stats['assistant_breakdown']:
            print("\nAI Assistant Breakdown")
            print("---------------------")
            for assistant, count in stats['assistant_breakdown'].items():
                print(f"- {assistant}: {count} commits ({round(count / stats['ai_assisted_commits'] * 100 if stats['ai_assisted_commits'] else 0, 1)}%)")
        
        # Generate dashboard if matplotlib is available
        try:
            from scripts.create_dashboard import generate_commit_graphs
            dashboard_path = repo_path / "dashboard"
            generate_commit_graphs(str(repo_path), str(dashboard_path))
            print(f"\nDashboard generated in {dashboard_path}")
        except ImportError:
            print("\nMatplotlib not found. Skipping dashboard generation.")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())