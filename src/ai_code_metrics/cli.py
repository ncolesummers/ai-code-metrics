"""Command-line interface for AI Code Metrics."""

import argparse
import sys
from pathlib import Path

from ai_code_metrics.analyzers import GitMetricsAnalyzer, ROICalculator
from ai_code_metrics.exporters.prometheus_exporter import app as prometheus_app


def main():
    """Entry point for the AI Code Metrics CLI."""
    parser = argparse.ArgumentParser(
        description="AI Code Metrics - Measure AI coding assistant effectiveness"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze Git repository")
    analyze_parser.add_argument("--repo-path", type=str, default=".", help="Path to Git repository")
    analyze_parser.add_argument("--days", type=int, default=7, help="Number of days to analyze")
    analyze_parser.add_argument("--output", type=str, default="metrics_report.json", 
                               help="Output file path")
    analyze_parser.add_argument("--anonymize", action="store_true", help="Anonymize sensitive data")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export metrics to Prometheus")
    export_parser.add_argument("--host", type=str, default="0.0.0.0", 
                              help="Host to bind to")
    export_parser.add_argument("--port", type=int, default=8080, 
                              help="Port to listen on")
    export_parser.add_argument("--debug", action="store_true", 
                              help="Run in debug mode")
    
    # ROI command
    roi_parser = subparsers.add_parser("roi", help="Calculate ROI")
    roi_parser.add_argument("--metrics-dir", type=str, default=Path.home() / ".ai_metrics",
                           help="Directory containing metrics files")
    roi_parser.add_argument("--days", type=int, default=30, 
                           help="Number of days to include in calculation")
    roi_parser.add_argument("--hourly-rate", type=float, default=75.0,
                           help="Developer hourly rate for ROI calculation")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        run_analyze(args)
    elif args.command == "export":
        run_export(args)
    elif args.command == "roi":
        run_roi(args)
    else:
        parser.print_help()
        return 1
    
    return 0


def run_analyze(args):
    """Run Git repository analysis."""
    try:
        print(f"Analyzing repository: {args.repo_path}")
        analyzer = GitMetricsAnalyzer(args.repo_path)
        metrics = analyzer.analyze_recent_commits(days=args.days)
        
        # Calculate basic stats
        total_commits = len(metrics)
        ai_commits = sum(1 for m in metrics if m.get('ai_generated_lines', 0) > 0)
        total_lines_added = sum(m.get('lines_added', 0) for m in metrics)
        ai_lines = sum(m.get('ai_generated_lines', 0) for m in metrics)
        
        # Generate report
        import json
        with open(args.output, 'w') as f:
            json.dump({
                'repository': args.repo_path,
                'days_analyzed': args.days,
                'total_commits': total_commits,
                'ai_assisted_commits': ai_commits,
                'ai_assisted_percentage': round(ai_commits / total_commits * 100 if total_commits else 0, 2),
                'total_lines_added': total_lines_added,
                'ai_generated_lines': ai_lines,
                'ai_generated_percentage': round(ai_lines / total_lines_added * 100 if total_lines_added else 0, 2),
                'commit_data': metrics
            }, f, indent=2)
        
        print(f"Metrics saved to {args.output}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def run_export(args):
    """Run Prometheus metrics exporter."""
    try:
        print(f"Starting Prometheus exporter on {args.host}:{args.port}")
        prometheus_app.run(host=args.host, port=args.port, debug=args.debug)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def run_roi(args):
    """Run ROI calculator."""
    try:
        metrics_dir = Path(args.metrics_dir)
        if not metrics_dir.exists():
            print(f"Metrics directory not found: {metrics_dir}", file=sys.stderr)
            return 1
        
        metrics_files = list(metrics_dir.glob("timing_*.jsonl"))
        if not metrics_files:
            print(f"No metrics files found in {metrics_dir}", file=sys.stderr)
            return 1
        
        calculator = ROICalculator(hourly_rate=args.hourly_rate)
        roi_data = calculator.calculate_roi(metrics_files, period_days=args.days)
        
        print("\nROI Analysis:")
        print(f"Period: {args.days} days")
        print(f"Total hours saved: {roi_data['total_hours_saved']}")
        print(f"Dollar value saved: ${roi_data['dollar_value_saved']}")
        print(f"API cost: ${roi_data['total_api_cost']}")
        print(f"Net savings: ${roi_data['net_savings']}")
        print(f"ROI: {roi_data['roi_percentage']}%")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())