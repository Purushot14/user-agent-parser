"""
Advanced Analytics and Batch Processing Module
Provides comprehensive analytics, reporting, and batch processing capabilities.
"""

import csv
import json
import statistics
import time
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator, List, Optional

from .advanced_engine import AdvancedResult, AdvancedUserAgentEngine, DetectionLevel, DeviceCategory


@dataclass
class AnalyticsReport:
    """Comprehensive analytics report."""

    total_requests: int = 0
    unique_user_agents: int = 0
    parsing_time_ms: float = 0.0

    # Browser analytics
    browser_distribution: Dict[str, int] = None
    browser_version_distribution: Dict[str, int] = None
    browser_engine_distribution: Dict[str, int] = None

    # OS analytics
    os_distribution: Dict[str, int] = None
    os_version_distribution: Dict[str, int] = None

    # Device analytics
    device_type_distribution: Dict[str, int] = None
    device_category_distribution: Dict[str, int] = None
    device_brand_distribution: Dict[str, int] = None
    mobile_vs_desktop: Dict[str, int] = None

    # Detection quality
    confidence_distribution: Dict[str, int] = None
    detection_success_rate: float = 0.0

    # Security insights
    bot_detection_rate: float = 0.0
    privacy_mode_usage: float = 0.0
    adblocker_usage: float = 0.0

    # Performance metrics
    avg_parsing_time_ms: float = 0.0
    max_parsing_time_ms: float = 0.0
    min_parsing_time_ms: float = 0.0
    cache_hit_rate: float = 0.0

    # Trends
    hourly_distribution: Dict[str, int] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.browser_distribution is None:
            self.browser_distribution = {}
        if self.browser_version_distribution is None:
            self.browser_version_distribution = {}
        if self.browser_engine_distribution is None:
            self.browser_engine_distribution = {}
        if self.os_distribution is None:
            self.os_distribution = {}
        if self.os_version_distribution is None:
            self.os_version_distribution = {}
        if self.device_type_distribution is None:
            self.device_type_distribution = {}
        if self.device_category_distribution is None:
            self.device_category_distribution = {}
        if self.device_brand_distribution is None:
            self.device_brand_distribution = {}
        if self.mobile_vs_desktop is None:
            self.mobile_vs_desktop = {}
        if self.confidence_distribution is None:
            self.confidence_distribution = {}
        if self.hourly_distribution is None:
            self.hourly_distribution = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)


class UserAgentAnalytics:
    """Advanced analytics processor for user agent data."""

    def __init__(self, engine: Optional[AdvancedUserAgentEngine] = None):
        self.engine = engine or AdvancedUserAgentEngine()
        self.results_cache: List[AdvancedResult] = []
        self.timestamps: List[datetime] = []

    def analyze_batch(self, user_agents: List[str], max_workers: int = 4, save_results: bool = True) -> AnalyticsReport:
        """
        Analyze a batch of user agents and generate comprehensive analytics.

        Args:
            user_agents: List of user agent strings
            max_workers: Number of parallel workers
            save_results: Whether to save results for historical analysis

        Returns:
            Comprehensive analytics report
        """
        start_time = time.time()

        # Parse all user agents
        results = self.engine.batch_parse(user_agents, max_workers=max_workers)

        # Save results if requested
        if save_results:
            self.results_cache.extend(results)
            self.timestamps.extend([datetime.now()] * len(results))

        # Generate analytics
        report = self._generate_report(results, user_agents)
        report.parsing_time_ms = (time.time() - start_time) * 1000

        return report

    def _generate_report(self, results: List[AdvancedResult], user_agents: List[str]) -> AnalyticsReport:
        """Generate comprehensive analytics report."""
        report = AnalyticsReport()

        # Basic stats
        report.total_requests = len(results)
        report.unique_user_agents = len(set(user_agents))

        # Browser analytics
        browsers = [r.browser for r in results if r.browser]
        report.browser_distribution = dict(Counter(browsers))

        browser_versions = [f"{r.browser} {r.browser_version}" for r in results if r.browser and r.browser_version]
        report.browser_version_distribution = dict(Counter(browser_versions))

        engines = [r.browser_engine for r in results if r.browser_engine]
        report.browser_engine_distribution = dict(Counter(engines))

        # OS analytics
        operating_systems = [r.os for r in results if r.os]
        report.os_distribution = dict(Counter(operating_systems))

        os_versions = [f"{r.os} {r.os_version}" for r in results if r.os and r.os_version]
        report.os_version_distribution = dict(Counter(os_versions))

        # Device analytics
        device_types = [r.device_type for r in results if r.device_type]
        report.device_type_distribution = dict(Counter(device_types))

        device_categories = [r.device_category.value for r in results if r.device_category != DeviceCategory.UNKNOWN]
        report.device_category_distribution = dict(Counter(device_categories))

        device_brands = [r.device_brand for r in results if r.device_brand]
        report.device_brand_distribution = dict(Counter(device_brands))

        # Mobile vs Desktop
        mobile_count = sum(1 for r in results if r.is_mobile or r.is_tablet)
        desktop_count = sum(1 for r in results if r.is_desktop)
        bot_count = sum(1 for r in results if r.is_bot)
        other_count = len(results) - mobile_count - desktop_count - bot_count

        report.mobile_vs_desktop = {
            "mobile": mobile_count,
            "desktop": desktop_count,
            "bot": bot_count,
            "other": other_count,
        }

        # Detection quality
        confidence_levels = [r.detection_confidence.value for r in results]
        report.confidence_distribution = dict(Counter(confidence_levels))

        successful_detections = sum(1 for r in results if r.detection_confidence != DetectionLevel.UNKNOWN)
        report.detection_success_rate = successful_detections / len(results) if results else 0

        # Security insights
        report.bot_detection_rate = sum(1 for r in results if r.is_bot) / len(results) if results else 0

        privacy_users = sum(1 for r in results if r.security and r.security.privacy_mode)
        report.privacy_mode_usage = privacy_users / len(results) if results else 0

        adblocker_users = sum(1 for r in results if r.security and r.security.has_adblocker)
        report.adblocker_usage = adblocker_users / len(results) if results else 0

        # Performance metrics
        parsing_times = [r.parsing_time_ms for r in results if r.parsing_time_ms > 0]
        if parsing_times:
            report.avg_parsing_time_ms = statistics.mean(parsing_times)
            report.max_parsing_time_ms = max(parsing_times)
            report.min_parsing_time_ms = min(parsing_times)

        # Cache statistics
        cache_info = self.engine.get_cache_info()
        if cache_info:
            total_requests = cache_info.get("hits", 0) + cache_info.get("misses", 0)
            report.cache_hit_rate = cache_info.get("hits", 0) / total_requests if total_requests else 0

        return report

    def analyze_trends(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Analyze trends over time."""
        if not self.results_cache or not self.timestamps:
            return {"error": "No historical data available"}

        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)

        # Filter recent results
        recent_indices = [i for i, ts in enumerate(self.timestamps) if ts >= cutoff_time]
        recent_results = [self.results_cache[i] for i in recent_indices]
        recent_timestamps = [self.timestamps[i] for i in recent_indices]

        if not recent_results:
            return {"error": "No recent data available"}

        # Hourly distribution
        hourly_counts = defaultdict(int)
        for ts in recent_timestamps:
            hour_key = ts.strftime("%Y-%m-%d %H:00")
            hourly_counts[hour_key] += 1

        # Browser trends
        browser_trends = defaultdict(list)
        for result, ts in zip(recent_results, recent_timestamps):
            if result.browser:
                hour_key = ts.strftime("%Y-%m-%d %H:00")
                browser_trends[result.browser].append(hour_key)

        return {
            "time_window_hours": time_window_hours,
            "total_requests": len(recent_results),
            "hourly_distribution": dict(hourly_counts),
            "browser_trends": {browser: dict(Counter(hours)) for browser, hours in browser_trends.items()},
            "avg_requests_per_hour": len(recent_results) / time_window_hours,
        }

    def export_report(self, report: AnalyticsReport, format: str = "json", filename: Optional[str] = None) -> str:
        """Export analytics report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if not filename:
            filename = f"user_agent_analytics_{timestamp}"

        if format.lower() == "json":
            filename += ".json"
            with open(filename, "w") as f:
                f.write(report.to_json())

        elif format.lower() == "csv":
            filename += ".csv"
            self._export_csv(report, filename)

        else:
            raise ValueError(f"Unsupported format: {format}")

        return filename

    def _export_csv(self, report: AnalyticsReport, filename: str) -> None:
        """Export report as CSV format."""
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Summary section
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Requests", report.total_requests])
            writer.writerow(["Unique User Agents", report.unique_user_agents])
            writer.writerow(["Detection Success Rate", f"{report.detection_success_rate:.2%}"])
            writer.writerow(["Bot Detection Rate", f"{report.bot_detection_rate:.2%}"])
            writer.writerow(["Cache Hit Rate", f"{report.cache_hit_rate:.2%}"])
            writer.writerow([])

            # Browser distribution
            writer.writerow(["Browser", "Count", "Percentage"])
            total = report.total_requests or 1
            for browser, count in report.browser_distribution.items():
                writer.writerow([browser, count, f"{count / total:.2%}"])
            writer.writerow([])

            # OS distribution
            writer.writerow(["Operating System", "Count", "Percentage"])
            for os, count in report.os_distribution.items():
                writer.writerow([os, count, f"{count / total:.2%}"])

    def generate_insights(self, report: AnalyticsReport) -> List[str]:
        """Generate actionable insights from the analytics report."""
        insights = []

        # Browser insights
        if report.browser_distribution:
            top_browser = max(report.browser_distribution, key=report.browser_distribution.get)
            top_browser_percent = report.browser_distribution[top_browser] / report.total_requests * 100
            insights.append(f"Most popular browser: {top_browser} ({top_browser_percent:.1f}% of traffic)")

        # Mobile vs Desktop insights
        if report.mobile_vs_desktop:
            mobile_percent = report.mobile_vs_desktop.get("mobile", 0) / report.total_requests * 100
            desktop_percent = report.mobile_vs_desktop.get("desktop", 0) / report.total_requests * 100

            if mobile_percent > desktop_percent:
                insights.append(
                    f"Mobile-first audience: {mobile_percent:.1f}% mobile vs {desktop_percent:.1f}% desktop"
                )
            else:
                insights.append(
                    f"Desktop-heavy audience: {desktop_percent:.1f}% desktop vs {mobile_percent:.1f}% mobile"
                )

        # Bot detection insights
        if report.bot_detection_rate > 0.1:
            insights.append(f"High bot traffic detected: {report.bot_detection_rate:.1%} of requests")
        elif report.bot_detection_rate > 0.05:
            insights.append(f"Moderate bot traffic: {report.bot_detection_rate:.1%} of requests")

        # Privacy insights
        if report.privacy_mode_usage > 0.05:
            insights.append(f"Privacy-conscious users: {report.privacy_mode_usage:.1%} using private browsing")

        if report.adblocker_usage > 0.1:
            insights.append(f"Ad blocker usage: {report.adblocker_usage:.1%} of users have ad blockers")

        # Performance insights
        if report.cache_hit_rate > 0.8:
            insights.append(f"Excellent caching performance: {report.cache_hit_rate:.1%} cache hit rate")
        elif report.cache_hit_rate > 0.6:
            insights.append(f"Good caching performance: {report.cache_hit_rate:.1%} cache hit rate")
        else:
            insights.append(f"Consider cache optimization: {report.cache_hit_rate:.1%} cache hit rate")

        # Detection quality insights
        if report.detection_success_rate < 0.8:
            insights.append(f"Detection accuracy could be improved: {report.detection_success_rate:.1%} success rate")
        else:
            insights.append(f"High detection accuracy: {report.detection_success_rate:.1%} success rate")

        return insights


class BatchProcessor:
    """High-performance batch processing for large datasets."""

    def __init__(self, engine: Optional[AdvancedUserAgentEngine] = None):
        self.engine = engine or AdvancedUserAgentEngine()
        self.analytics = UserAgentAnalytics(self.engine)

    def process_file(
        self, filepath: str, format: str = "txt", chunk_size: int = 1000, max_workers: int = 4
    ) -> AnalyticsReport:
        """
        Process user agents from a file with chunked processing.

        Args:
            filepath: Path to file containing user agents
            format: File format ('txt', 'csv', 'json')
            chunk_size: Number of user agents to process per chunk
            max_workers: Number of parallel workers

        Returns:
            Comprehensive analytics report
        """
        user_agents = self._read_file(filepath, format)

        # Process in chunks
        all_results = []
        for chunk in self._chunk_list(user_agents, chunk_size):
            results = self.engine.batch_parse(chunk, max_workers=max_workers)
            all_results.extend(results)

        # Generate comprehensive report
        return self.analytics._generate_report(all_results, user_agents)

    def process_stream(self, user_agent_stream: Iterator[str], max_workers: int = 4) -> Iterator[AnalyticsReport]:
        """Process streaming user agent data."""
        batch = []
        batch_size = 100

        for ua in user_agent_stream:
            batch.append(ua)

            if len(batch) >= batch_size:
                results = self.engine.batch_parse(batch, max_workers=max_workers)
                yield self.analytics._generate_report(results, batch)
                batch = []

        # Process remaining batch
        if batch:
            results = self.engine.batch_parse(batch, max_workers=max_workers)
            yield self.analytics._generate_report(results, batch)

    def _read_file(self, filepath: str, format: str) -> List[str]:
        """Read user agents from file."""
        user_agents = []

        if format == "txt":
            with open(filepath) as f:
                user_agents = [line.strip() for line in f if line.strip()]

        elif format == "csv":
            with open(filepath) as f:
                reader = csv.reader(f)
                # Assume first column contains user agents
                user_agents = [row[0] for row in reader if row]

        elif format == "json":
            with open(filepath) as f:
                data = json.load(f)
                if isinstance(data, list):
                    user_agents = data
                elif isinstance(data, dict) and "user_agents" in data:
                    user_agents = data["user_agents"]

        else:
            raise ValueError(f"Unsupported format: {format}")

        return user_agents

    def _chunk_list(self, lst: List[str], chunk_size: int) -> Iterator[List[str]]:
        """Split list into chunks."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i : i + chunk_size]
