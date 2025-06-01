#!/usr/bin/env python3
"""Run the Prometheus metrics exporter."""

import argparse
import sys
from ai_code_metrics.exporters.prometheus_exporter import app


def main():
    """Run the Prometheus metrics exporter."""
    parser = argparse.ArgumentParser(description="Run the Prometheus metrics exporter")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    args = parser.parse_args()
    
    try:
        print(f"Starting Prometheus exporter on {args.host}:{args.port}")
        app.run(host=args.host, port=args.port, debug=args.debug)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()