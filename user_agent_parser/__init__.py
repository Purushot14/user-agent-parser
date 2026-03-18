"""
Advanced User Agent Parser with ML-inspired Pattern Matching
Created by prakash at 02/03/22
Enhanced with advanced analytics, batch processing, and comprehensive device detection.
"""

__author__ = "Prakash14"
__version__ = "0.2.1"

# Legacy API (backward compatibility)
# Advanced API
from .advanced_engine import (
    AdvancedResult,
    AdvancedUserAgentEngine,
    BrowserCapabilities,
    DetectionLevel,
    DeviceCategory,
    SecurityFingerprint,
    parse_advanced,
)

# Analytics and Batch Processing
from .analytics import AnalyticsReport, BatchProcessor, UserAgentAnalytics
from .parser import Parser, _cached_parse_user_agent


def parse(user_agent_str: str):
    """
    Fast cached parsing of user agent strings (legacy API).

    Args:
        user_agent_str: The user agent string to parse

    Returns:
        Tuple of (browser, browser_version, os, os_version, device_type, device_name, device_host)
    """
    return _cached_parse_user_agent(user_agent_str)


def analyze(user_agent_str: str, include_security: bool = False, include_capabilities: bool = True) -> AdvancedResult:
    """
    Advanced user agent analysis with comprehensive metadata extraction.

    Args:
        user_agent_str: User agent string to analyze
        include_security: Include security fingerprinting analysis
        include_capabilities: Include browser capabilities detection

    Returns:
        AdvancedResult with comprehensive analysis including confidence scoring,
        device categorization, browser capabilities, and security insights.

    Example:
        >>> result = analyze("Mozilla/5.0 (iPhone; CPU iPhone OS 13_6...")
        >>> print(f"Device: {result.device_name} ({result.confidence_score:.2f})")
        >>> print(f"Capabilities: WebGL={result.capabilities.webgl_support}")
        >>> print(result.to_json())
    """
    return parse_advanced(user_agent_str, include_security=include_security, include_capabilities=include_capabilities)


def batch_analyze(user_agents: list, max_workers: int = 4) -> list:
    """
    Analyze multiple user agents in parallel with advanced detection.

    Args:
        user_agents: List of user agent strings
        max_workers: Number of parallel workers (default: 4)

    Returns:
        List of AdvancedResult objects

    Example:
        >>> user_agents = ["Mozilla/5.0...", "Chrome/96.0..."]
        >>> results = batch_analyze(user_agents)
        >>> for result in results:
        ...     print(f"{result.browser} on {result.device_category.value}")
    """
    from .advanced_engine import advanced_engine

    return advanced_engine.batch_parse(user_agents, max_workers=max_workers)


def generate_analytics(user_agents: list, export_format: str = None, filename: str = None) -> AnalyticsReport:
    """
    Generate comprehensive analytics report from user agent data.

    Args:
        user_agents: List of user agent strings to analyze
        export_format: Optional export format ('json' or 'csv')
        filename: Optional filename for export

    Returns:
        AnalyticsReport with detailed insights and distributions

    Example:
        >>> user_agents = ["Mozilla/5.0...", "Chrome/96.0..."]
        >>> report = generate_analytics(user_agents, export_format='json')
        >>> print(f"Mobile traffic: {report.mobile_vs_desktop['mobile']} requests")
        >>> print(f"Top browser: {max(report.browser_distribution, key=report.browser_distribution.get)}")
    """
    analytics = UserAgentAnalytics()
    report = analytics.analyze_batch(user_agents)

    if export_format and filename:
        analytics.export_report(report, export_format, filename)
    elif export_format:
        analytics.export_report(report, export_format)

    return report


# Convenience aliases for different use cases
parse_simple = parse  # For basic parsing
parse_detailed = analyze  # For detailed analysis
parse_batch = batch_analyze  # For batch processing

# Export main classes and functions
__all__ = [
    # Legacy API
    "Parser",
    "parse",
    # Advanced API
    "AdvancedUserAgentEngine",
    "AdvancedResult",
    "DeviceCategory",
    "DetectionLevel",
    "BrowserCapabilities",
    "SecurityFingerprint",
    "analyze",
    "batch_analyze",
    "parse_advanced",
    # Analytics
    "UserAgentAnalytics",
    "BatchProcessor",
    "AnalyticsReport",
    "generate_analytics",
    # Convenience aliases
    "parse_simple",
    "parse_detailed",
    "parse_batch",
]
