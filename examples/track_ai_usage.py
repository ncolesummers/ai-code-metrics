#!/usr/bin/env python3
"""Example script to track AI coding assistant usage in a repository."""

import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_code_metrics.analyzers import CommitAnalyzer


def main():
    """Run a basic analysis of AI usage in the current repository."""
    # Get the repository path (current directory or from argument)
    repo_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    
    print(f"Analyzing repository: {repo_path}")
    
    try:
        # Create analyzer
        analyzer = CommitAnalyzer(repo_path)
        
        # Get basic statistics
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
                print(f"- {assistant}: {count} commits ({round(count / stats['ai_assisted_commits'] * 100, 1)}%)")
        
        # Get detailed commit information
        print("\nRecent AI-assisted commits")
        print("------------------------")
        commits = analyzer.analyze_commits(limit=10)
        ai_commits = [c for c in commits if c.get('ai_assisted', False)]
        
        for commit in ai_commits[:5]:  # Show up to 5 recent AI commits
            print(f"\nCommit: {commit['commit_hash'][:8]}")
            print(f"Author: {commit['author']}")
            print(f"Date: {commit['timestamp'].split('T')[0]}")
            print(f"Assistant: {commit['ai_assistant']}")
            print(f"Lines added: {commit.get('lines_added', 'N/A')}")
            print(f"Files changed: {commit.get('files_changed', 'N/A')}")
            
        # Save full report
        output_file = "ai_usage_report.json"
        with open(output_file, "w") as f:
            json.dump({
                "summary": stats,
                "recent_commits": commits[:20],  # Include 20 recent commits
            }, f, indent=2)
            
        print(f"\nDetailed report saved to {output_file}")
            
    except Exception as e:
        print(f"Error analyzing repository: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())