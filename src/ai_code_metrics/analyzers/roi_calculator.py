"""ROI calculation for AI coding assistants."""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


class ROICalculator:
    """Calculate return on investment for AI coding assistant usage."""
    
    def __init__(self, hourly_rate: float = 75.0):
        self.hourly_rate = hourly_rate
    
    def calculate_roi(self, metrics_files: list[Path], period_days: int = 30) -> dict[str, Any]:
        """Calculate ROI for AI coding assistant usage."""
        
        # Metrics collection
        total_time_saved = 0
        total_api_cost = 0
        quality_improvements = []
        metrics_count = 0
        
        # Time range for filtering
        cutoff_date = datetime.now() - timedelta(days=period_days)
        cutoff_timestamp = cutoff_date.timestamp()
        
        # Process each metrics file
        for metrics_file in metrics_files:
            if not metrics_file.exists():
                continue
                
            with open(metrics_file) as f:
                for line in f:
                    try:
                        metric = json.loads(line)
                        
                        # Skip metrics outside our time range
                        if metric.get('timestamp', 0) < cutoff_timestamp:
                            continue
                            
                        metrics_count += 1
                        
                        # Calculate time savings (assuming 30% improvement)
                        if metric.get('ai_assisted'):
                            baseline_time = metric['duration'] / 0.7  # Assuming 30% faster with AI
                            time_saved = baseline_time - metric['duration']
                            total_time_saved += time_saved
                        
                        # Track API costs
                        if 'api_cost' in metric:
                            total_api_cost += metric['api_cost']
                        
                        # Track quality improvements
                        if 'quality_score' in metric:
                            quality_improvements.append(metric['quality_score'])
                    except Exception:
                        continue
        
        # Calculate financial impact
        hours_saved = total_time_saved / 3600  # Convert seconds to hours
        dollar_value_saved = hours_saved * self.hourly_rate
        net_savings = dollar_value_saved - total_api_cost
        
        # Avoid division by zero
        if total_api_cost > 0:
            roi_percentage = (net_savings / total_api_cost) * 100
        else:
            roi_percentage = 0 if net_savings == 0 else float('inf')
        
        # Calculate quality improvement
        avg_quality = (
            sum(quality_improvements) / len(quality_improvements)
            if quality_improvements
            else 0
        )
        
        return {
            'period_days': period_days,
            'metrics_analyzed': metrics_count,
            'total_hours_saved': round(hours_saved, 2),
            'dollar_value_saved': round(dollar_value_saved, 2),
            'total_api_cost': round(total_api_cost, 2),
            'net_savings': round(net_savings, 2),
            'roi_percentage': round(roi_percentage, 2),
            'average_quality_score': round(avg_quality, 2),
            'report_date': datetime.now().isoformat()
        }