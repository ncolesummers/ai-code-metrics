"""Tests for timing metrics collection."""

import pytest
import time
import tempfile
import json
from pathlib import Path
from ai_code_metrics.collectors import MetricsCollector


def test_timing_decorator():
    """Test that the timing decorator correctly records function execution."""
    # Create a temporary directory for metrics
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a collector that stores metrics in our temp directory
        collector = MetricsCollector(storage_path=temp_path)
        
        # Define a test function using the decorator
        @collector.track_function(ai_assisted=True)
        def test_function():
            time.sleep(0.1)  # Simulate work
            return "result"
        
        # Call the function
        result = test_function()
        
        # Check the function executed correctly
        assert result == "result"
        
        # Verify metrics were stored
        metrics_files = list(temp_path.glob('timing_*.jsonl'))
        assert len(metrics_files) == 1
        
        # Read the metrics file
        with open(metrics_files[0], 'r') as f:
            metrics = [json.loads(line) for line in f]
        
        # Check the metrics content
        assert len(metrics) == 1
        metric = metrics[0]
        assert metric['function_name'] == 'test_function'
        assert metric['ai_assisted'] is True
        assert metric['success'] is True
        assert metric['duration'] >= 0.1  # Should be at least the sleep time
        assert 'timestamp' in metric


def test_timing_exception_handling():
    """Test that the timing decorator handles exceptions correctly."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        collector = MetricsCollector(storage_path=temp_path)
        
        # Define a function that raises an exception
        @collector.track_function(ai_assisted=False)
        def failing_function():
            raise ValueError("Test error")
        
        # Call the function and expect an exception
        with pytest.raises(ValueError):
            failing_function()
        
        # Verify metrics were stored
        metrics_files = list(temp_path.glob('timing_*.jsonl'))
        assert len(metrics_files) == 1
        
        # Read the metrics file
        with open(metrics_files[0], 'r') as f:
            metrics = [json.loads(line) for line in f]
        
        # Check the metrics content
        assert len(metrics) == 1
        metric = metrics[0]
        assert metric['function_name'] == 'failing_function'
        assert metric['ai_assisted'] is False
        assert metric['success'] is False  # Should be false due to the exception