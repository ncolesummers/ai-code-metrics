#!/usr/bin/env python3
"""Generate a dashboard for AI coding assistant metrics."""

import argparse
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os

from ai_code_metrics.analyzers import CommitAnalyzer


def generate_commit_graphs(repo_path: str, output_dir: str, days: int = 30):
    """Generate graphs of commit activity by AI assistant."""
    try:
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)
        
        # Analyze repository
        analyzer = CommitAnalyzer(repo_path)
        
        # Get date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get commit data
        commits = analyzer.analyze_commits(since=start_date.strftime("%Y-%m-%d"))
        
        if not commits:
            print("No commits found in the specified time period.")
            return
            
        # Group commits by date
        commits_by_date = {}
        ai_commits_by_date = {}
        
        for commit in commits:
            date_str = commit['timestamp'].split('T')[0]  # Extract YYYY-MM-DD
            
            # Track all commits
            if date_str not in commits_by_date:
                commits_by_date[date_str] = []
            commits_by_date[date_str].append(commit)
            
            # Track AI-assisted commits
            if commit.get('ai_assisted', False):
                if date_str not in ai_commits_by_date:
                    ai_commits_by_date[date_str] = []
                ai_commits_by_date[date_str].append(commit)
        
        # Generate time series data
        dates = sorted(commits_by_date.keys())
        all_counts = [len(commits_by_date[d]) for d in dates]
        ai_counts = [len(ai_commits_by_date.get(d, [])) for d in dates]
        
        # Plot commit frequency
        plt.figure(figsize=(12, 6))
        plt.plot(dates, all_counts, label="All Commits", marker="o")
        plt.plot(dates, ai_counts, label="AI-Assisted Commits", marker="x")
        plt.xlabel("Date")
        plt.ylabel("Number of Commits")
        plt.title("Commit Activity Over Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.legend()
        plt.savefig(output_path / "commit_activity.png")
        
        # Generate AI assistant breakdown
        assistants = {}
        for commit in commits:
            if commit.get('ai_assisted', False) and commit.get('ai_assistant'):
                assistant = commit['ai_assistant']
                assistants[assistant] = assistants.get(assistant, 0) + 1
        
        if assistants:
            # Plot AI assistant breakdown
            plt.figure(figsize=(10, 6))
            assistant_names = list(assistants.keys())
            assistant_counts = [assistants[name] for name in assistant_names]
            
            plt.bar(assistant_names, assistant_counts)
            plt.xlabel("AI Assistant")
            plt.ylabel("Number of Commits")
            plt.title("AI Assistant Usage")
            plt.tight_layout()
            plt.savefig(output_path / "assistant_breakdown.png")
        
        # Calculate lines of code statistics
        human_lines = sum(c['lines_added'] for c in commits if not c.get('ai_assisted', False))
        ai_lines = sum(c['lines_added'] for c in commits if c.get('ai_assisted', False))
        total_lines = human_lines + ai_lines
        
        # Plot lines of code comparison
        plt.figure(figsize=(8, 8))
        labels = ['AI-Assisted', 'Human']
        sizes = [ai_lines, human_lines]
        colors = ['#ff9999','#66b3ff']
        explode = (0.1, 0)  # explode the AI slice
        
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title("Lines of Code Distribution")
        plt.tight_layout()
        plt.savefig(output_path / "code_distribution.png")
        
        # Generate summary report
        summary = {
            "repository": repo_path,
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "total_commits": len(commits),
            "ai_assisted_commits": sum(1 for c in commits if c.get('ai_assisted', False)),
            "ai_percentage": round(sum(1 for c in commits if c.get('ai_assisted', False)) / len(commits) * 100 if commits else 0, 2),
            "total_lines_added": total_lines,
            "ai_lines_percentage": round(ai_lines / total_lines * 100 if total_lines else 0, 2),
            "ai_assistants": assistants,
            "graphs": [
                str(output_path / "commit_activity.png"),
                str(output_path / "assistant_breakdown.png"),
                str(output_path / "code_distribution.png")
            ]
        }
        
        with open(output_path / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"Dashboard generated in {output_path}")
        print(f"Total commits: {summary['total_commits']}")
        print(f"AI-assisted commits: {summary['ai_assisted_commits']} ({summary['ai_percentage']}%)")
        print(f"AI-generated code: {summary['ai_lines_percentage']}%")
        
    except Exception as e:
        print(f"Error generating dashboard: {e}", file=sys.stderr)
        return 1
    
    return 0


def main():
    """Run the dashboard generator CLI."""
    parser = argparse.ArgumentParser(description="Generate AI coding metrics dashboard")
    parser.add_argument("--repo-path", type=str, default=".", help="Path to Git repository")
    parser.add_argument("--output-dir", type=str, default="./dashboard", help="Output directory for dashboard files")
    parser.add_argument("--days", type=int, default=30, help="Number of days to include in analysis")
    
    args = parser.parse_args()
    
    # Check for matplotlib
    try:
        import matplotlib
    except ImportError:
        print("Error: matplotlib is required for dashboard generation")
        print("Install with: uv add --dev matplotlib")
        return 1
    
    return generate_commit_graphs(args.repo_path, args.output_dir, args.days)


if __name__ == "__main__":
    sys.exit(main())