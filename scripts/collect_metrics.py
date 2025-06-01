#!/usr/bin/env python3
"""CLI script to collect metrics from a Git repository."""

import argparse
import json
import sys
from pathlib import Path

from ai_code_metrics.analyzers import GitMetricsAnalyzer, ROICalculator
from ai_code_metrics.security import CodeAnonymizer


def main():
    """Run the metrics collection CLI."""
    parser = argparse.ArgumentParser(description="Collect AI coding metrics from a Git repository")
    parser.add_argument("--repo-path", type=str, default=".", help="Path to the Git repository")
    parser.add_argument("--days", type=int, default=7, help="Number of days to analyze")
    parser.add_argument("--output", type=str, default="metrics_report.json", help="Output file path")
    parser.add_argument("--anonymize", action="store_true", help="Anonymize sensitive data")
    parser.add_argument("--hourly-rate", type=float, default=75.0, 
                        help="Hourly developer rate for ROI calculation")
    
    args = parser.parse_args()
    
    try:
        # Analyze Git repository
        analyzer = GitMetricsAnalyzer(args.repo_path)
        metrics = analyzer.analyze_recent_commits(days=args.days)
        
        # Anonymize if requested
        if args.anonymize:
            anonymizer = CodeAnonymizer()
            for metric in metrics:
                if 'author' in metric:
                    metric['author'] = anonymizer.anonymize_code_snippet(metric['author'])
        
        # Calculate basic stats
        total_commits = len(metrics)
        ai_commits = sum(1 for m in metrics if m.get('ai_generated_lines', 0) > 0)
        total_lines_added = sum(m.get('lines_added', 0) for m in metrics)
        total_lines_deleted = sum(m.get('lines_deleted', 0) for m in metrics)
        ai_lines = sum(m.get('ai_generated_lines', 0) for m in metrics)
        
        # Generate report
        report = {
            'repository': args.repo_path,
            'days_analyzed': args.days,
            'total_commits': total_commits,
            'ai_assisted_commits': ai_commits,
            'ai_assisted_percentage': round(ai_commits / total_commits * 100 if total_commits else 0, 2),
            'total_lines_added': total_lines_added,
            'total_lines_deleted': total_lines_deleted,
            'ai_generated_lines': ai_lines,
            'ai_generated_percentage': round(ai_lines / total_lines_added * 100 if total_lines_added else 0, 2),
            'commit_data': metrics
        }
        
        # Save to file
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Metrics saved to {args.output}")
        
        # Print summary
        print("\nSummary:")
        print(f"Total commits: {total_commits}")
        print(f"AI-assisted commits: {ai_commits} ({report['ai_assisted_percentage']}%)")
        print(f"Total lines added: {total_lines_added}")
        print(f"AI-generated lines: {ai_lines} ({report['ai_generated_percentage']}%)")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()