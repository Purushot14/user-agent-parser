"""
Comprehensive test suite for advanced user agent parsing engine.
Tests advanced features, analytics, batch processing, and modern device detection.
"""

import json
import time
import unittest
from unittest.mock import patch

from user_agent_parser import (
    AdvancedResult,
    AnalyticsReport,
    BrowserCapabilities,
    DetectionLevel,
    DeviceCategory,
    SecurityFingerprint,
    analyze,
    batch_analyze,
    generate_analytics,
)
from user_agent_parser.advanced_engine import AdvancedUserAgentEngine
from user_agent_parser.analytics import BatchProcessor, UserAgentAnalytics
from user_agent_parser.modern_devices import DeviceSpec, ModernDeviceDetector


class TestAdvancedEngine(unittest.TestCase):
    """Test cases for the advanced parsing engine."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = AdvancedUserAgentEngine()

        # Modern test user agents
        self.iphone_15_ua = "Mozilla/5.0 (iPhone16,3; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
        self.galaxy_s24_ua = "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36"
        self.pixel_8_ua = "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.109 Mobile Safari/537.36"
        self.macbook_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        self.bot_ua = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

    def test_basic_analysis(self):
        """Test basic analysis functionality."""
        result = analyze(self.iphone_15_ua)

        self.assertIsInstance(result, AdvancedResult)
        self.assertIsNotNone(result.browser)
        self.assertIsNotNone(result.os)
        self.assertIsNotNone(result.device_type)
        self.assertTrue(result.is_mobile)
        self.assertFalse(result.is_bot)

    def test_confidence_scoring(self):
        """Test confidence scoring system."""
        # High confidence for modern devices
        result = analyze(self.galaxy_s24_ua)
        self.assertGreater(result.confidence_score, 0.5)
        self.assertIn(result.detection_confidence, [DetectionLevel.HIGH, DetectionLevel.MEDIUM])

        # Low confidence for minimal UA
        minimal_ua = "Mozilla/5.0"
        result = analyze(minimal_ua)
        self.assertLess(result.confidence_score, 0.5)

    def test_device_categorization(self):
        """Test device category detection."""
        # Smartphone
        result = analyze(self.iphone_15_ua)
        self.assertEqual(result.device_category, DeviceCategory.SMARTPHONE)
        self.assertTrue(result.is_mobile)

        # Desktop/Laptop
        result = analyze(self.macbook_ua)
        self.assertIn(result.device_category, [DeviceCategory.DESKTOP, DeviceCategory.LAPTOP])
        self.assertTrue(result.is_desktop)

        # Bot
        result = analyze(self.bot_ua)
        self.assertEqual(result.device_category, DeviceCategory.BOT)
        self.assertTrue(result.is_bot)

    def test_browser_capabilities(self):
        """Test browser capabilities detection."""
        result = analyze(self.galaxy_s24_ua, include_capabilities=True)

        self.assertIsInstance(result.capabilities, BrowserCapabilities)
        # Chrome should have these capabilities
        self.assertTrue(result.capabilities.webgl_support)
        self.assertTrue(result.capabilities.javascript_enabled)
        self.assertTrue(result.capabilities.cookies_enabled)

    def test_security_fingerprinting(self):
        """Test security fingerprinting features."""
        result = analyze(self.macbook_ua, include_security=True)

        self.assertIsInstance(result.security, SecurityFingerprint)
        self.assertIsInstance(result.security.has_adblocker, bool)
        self.assertIsInstance(result.security.privacy_mode, bool)
        self.assertIsInstance(result.security.tracking_protection, bool)

    def test_bot_detection(self):
        """Test bot detection accuracy."""
        bot_agents = [
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)",
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "Twitterbot/1.0",
        ]

        for ua in bot_agents:
            result = analyze(ua)
            self.assertTrue(result.is_bot, f"Failed to detect bot: {ua}")
            self.assertEqual(result.device_category, DeviceCategory.BOT)

    def test_detection_reasons(self):
        """Test that detection reasons are populated."""
        result = analyze(self.pixel_8_ua)

        self.assertIsInstance(result.detection_reasons, list)
        self.assertGreater(len(result.detection_reasons), 0)
        # Should have reasons for browser, OS, and device detection
        self.assertTrue(any("Browser" in reason for reason in result.detection_reasons))

    def test_result_serialization(self):
        """Test result serialization to JSON."""
        result = analyze(self.iphone_15_ua)

        # Test to_dict
        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertIn("browser", result_dict)
        self.assertIn("confidence_score", result_dict)

        # Test to_json
        result_json = result.to_json()
        self.assertIsInstance(result_json, str)
        parsed_json = json.loads(result_json)
        self.assertIsInstance(parsed_json, dict)

    def test_parsing_time_tracking(self):
        """Test that parsing time is tracked."""
        result = analyze(self.galaxy_s24_ua)

        self.assertGreater(result.parsing_time_ms, 0)
        self.assertLess(result.parsing_time_ms, 100)  # Should be fast

    def test_fingerprint_generation(self):
        """Test unique fingerprint generation."""
        result1 = analyze(self.iphone_15_ua)
        result2 = analyze(self.galaxy_s24_ua)
        result3 = analyze(self.iphone_15_ua)  # Same as result1

        self.assertIsNotNone(result1.fingerprint_hash)
        self.assertNotEqual(result1.fingerprint_hash, result2.fingerprint_hash)
        # Same UA should generate consistent fingerprint
        self.assertEqual(result1.fingerprint_hash, result3.fingerprint_hash)

    def test_cache_functionality(self):
        """Test caching mechanism."""
        # First call - cache miss
        result1 = self.engine.parse(self.macbook_ua)

        # Second call - should hit cache
        result2 = self.engine.parse(self.macbook_ua)

        # Results should be identical
        self.assertEqual(result1.browser, result2.browser)
        self.assertEqual(result1.os, result2.os)

        # Check cache stats
        cache_info = self.engine.get_cache_info()
        self.assertGreater(cache_info.get("hits", 0), 0)

    def test_empty_user_agent(self):
        """Test handling of empty user agent."""
        result = analyze("")

        self.assertIsInstance(result, AdvancedResult)
        self.assertEqual(result.detection_confidence, DetectionLevel.UNKNOWN)
        self.assertEqual(result.confidence_score, 0.0)


class TestBatchProcessing(unittest.TestCase):
    """Test cases for batch processing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.6099.109",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0",
            "Mozilla/5.0 (compatible; Googlebot/2.1)",
            "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) Safari/604.1",
        ]

    def test_batch_analyze(self):
        """Test batch analysis of multiple user agents."""
        results = batch_analyze(self.user_agents, max_workers=2)

        self.assertEqual(len(results), len(self.user_agents))
        for result in results:
            self.assertIsInstance(result, AdvancedResult)

    def test_parallel_processing(self):
        """Test that batch processing is faster than sequential."""
        large_dataset = self.user_agents * 20  # 100 user agents

        # Sequential processing
        start_seq = time.time()
        for ua in large_dataset[:10]:  # Test subset
            analyze(ua)
        seq_time = time.time() - start_seq

        # Batch processing
        start_batch = time.time()
        batch_analyze(large_dataset[:10], max_workers=4)
        batch_time = time.time() - start_batch

        # Batch should be comparable (thread pool has overhead for fast ops)
        self.assertLess(batch_time, seq_time * 10)

    def test_error_handling_in_batch(self):
        """Test error handling in batch processing."""
        # Include some problematic user agents
        mixed_agents = self.user_agents + [None, "", "Invalid\x00UA"]

        results = batch_analyze(mixed_agents, max_workers=2)

        # Should still return results for all
        self.assertEqual(len(results), len(mixed_agents))

        # Valid UAs should be parsed correctly
        valid_results = [r for r in results[: len(self.user_agents)] if r.browser]
        self.assertGreater(len(valid_results), 0)


class TestAnalytics(unittest.TestCase):
    """Test cases for analytics functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.analytics = UserAgentAnalytics()
        self.test_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) Safari/604.1",
            "Mozilla/5.0 (Android 14; SM-S928B) Chrome/120.0",
            "Mozilla/5.0 (Windows NT 10.0) Edge/120.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) Safari/17.1",
            "Googlebot/2.1",
        ]

    def test_analytics_report_generation(self):
        """Test analytics report generation."""
        report = self.analytics.analyze_batch(self.test_agents)

        self.assertIsInstance(report, AnalyticsReport)
        self.assertEqual(report.total_requests, len(self.test_agents))
        self.assertGreater(report.unique_user_agents, 0)

    def test_browser_distribution(self):
        """Test browser distribution analysis."""
        report = generate_analytics(self.test_agents)

        self.assertIsInstance(report.browser_distribution, dict)
        self.assertGreater(len(report.browser_distribution), 0)

        # Check that totals add up
        total_browsers = sum(report.browser_distribution.values())
        self.assertLessEqual(total_browsers, report.total_requests)

    def test_device_categorization_analytics(self):
        """Test device category distribution."""
        report = generate_analytics(self.test_agents)

        self.assertIsInstance(report.mobile_vs_desktop, dict)
        self.assertIn("mobile", report.mobile_vs_desktop)
        self.assertIn("desktop", report.mobile_vs_desktop)
        self.assertIn("bot", report.mobile_vs_desktop)

    def test_confidence_distribution(self):
        """Test confidence score distribution."""
        report = generate_analytics(self.test_agents)

        self.assertIsInstance(report.confidence_distribution, dict)
        # Should have some confidence levels
        self.assertGreater(len(report.confidence_distribution), 0)

    def test_performance_metrics(self):
        """Test performance metrics in analytics."""
        report = generate_analytics(self.test_agents)

        self.assertGreaterEqual(report.avg_parsing_time_ms, 0)
        self.assertGreaterEqual(report.detection_success_rate, 0)
        self.assertLessEqual(report.detection_success_rate, 1.0)

    def test_security_insights(self):
        """Test security-related analytics."""
        report = generate_analytics(self.test_agents)

        self.assertGreaterEqual(report.bot_detection_rate, 0)
        self.assertLessEqual(report.bot_detection_rate, 1.0)
        self.assertGreaterEqual(report.privacy_mode_usage, 0)
        self.assertGreaterEqual(report.adblocker_usage, 0)

    def test_export_functionality(self):
        """Test report export to different formats."""
        report = generate_analytics(self.test_agents)

        # Test JSON export
        json_str = report.to_json()
        self.assertIsInstance(json_str, str)
        parsed = json.loads(json_str)
        self.assertIsInstance(parsed, dict)

        # Test dict conversion
        report_dict = report.to_dict()
        self.assertIsInstance(report_dict, dict)
        self.assertIn("total_requests", report_dict)

    def test_insights_generation(self):
        """Test actionable insights generation."""
        report = generate_analytics(self.test_agents)
        insights = self.analytics.generate_insights(report)

        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)

        # Insights should be strings
        for insight in insights:
            self.assertIsInstance(insight, str)
            self.assertGreater(len(insight), 0)


class TestModernDevices(unittest.TestCase):
    """Test cases for modern device detection."""

    def setUp(self):
        """Set up test fixtures."""
        self.detector = ModernDeviceDetector()

        # 2024 device user agents
        self.iphone_15_pro = "Mozilla/5.0 (iPhone16,3; CPU iPhone OS 17_2 like Mac OS X) Safari/604.1"
        self.galaxy_s24_ultra = "Mozilla/5.0 (Linux; Android 14; SM-S928B) Chrome/120.0"
        self.pixel_8_pro = "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) Chrome/120.0"
        self.quest_3 = "Mozilla/5.0 (X11; Linux x86_64; Quest 3) OculusBrowser/29.0"

    def test_modern_device_detection(self):
        """Test detection of 2024-2025 devices."""
        # Test iPhone 15 detection
        device = self.detector.detect_modern_device(self.iphone_15_pro)
        if device:
            self.assertIsInstance(device, DeviceSpec)
            self.assertEqual(device.brand, "Apple")
            self.assertEqual(device.category, "smartphone")
            self.assertEqual(device.release_year, 2024)

    def test_device_capabilities(self):
        """Test device capability detection."""
        device = self.detector.detect_modern_device(self.galaxy_s24_ultra)
        if device:
            capabilities = self.detector.get_device_capabilities(device)
            self.assertIsInstance(capabilities, list)
            self.assertIn("5G", device.capabilities)

    def test_modern_browser_detection(self):
        """Test modern browser feature detection."""
        chrome_120_ua = "Mozilla/5.0 Chrome/120.0.6099.109"
        browser_info = self.detector.detect_modern_browser(chrome_120_ua)

        if browser_info:
            self.assertIn("capabilities", browser_info)
            self.assertIn("engine", browser_info)

    def test_modern_os_detection(self):
        """Test modern OS feature detection."""
        ios_17_ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X)"
        os_info = self.detector.detect_modern_os(ios_17_ua)

        if os_info:
            self.assertIn("features", os_info)
            self.assertIn("latest_version", os_info)

    def test_gaming_console_detection(self):
        """Test gaming console detection."""
        ps5_pro_ua = "Mozilla/5.0 (PlayStation 5 Pro 2.26) AppleWebKit/605.1.15"

        result = analyze(ps5_pro_ua)
        self.assertEqual(result.device_category, DeviceCategory.GAMING_CONSOLE)

    def test_vr_device_detection(self):
        """Test VR/AR device detection."""
        result = analyze(self.quest_3)
        # Browser and OS should be detected
        self.assertIsNotNone(result.browser)
        self.assertIsNotNone(result.os)
        self.assertTrue(result.capabilities.vr_support)

    def test_flagship_detection(self):
        """Test flagship device detection."""
        # Galaxy S24 Ultra should be detected as flagship
        device = self.detector.detect_modern_device(self.galaxy_s24_ultra)
        if device:
            capabilities = self.detector.get_device_capabilities(device)
            # Should have high-end features
            if device.ram_gb and device.ram_gb >= 12:
                self.assertIn("high_performance", capabilities)


class TestBatchProcessor(unittest.TestCase):
    """Test cases for batch file processing."""

    def setUp(self):
        """Set up test fixtures."""
        self.processor = BatchProcessor()

    def test_chunk_processing(self):
        """Test chunked list processing."""
        large_list = list(range(100))
        chunks = list(self.processor._chunk_list(large_list, 10))

        self.assertEqual(len(chunks), 10)
        self.assertEqual(len(chunks[0]), 10)

        # Verify all elements are included
        flattened = [item for chunk in chunks for item in chunk]
        self.assertEqual(flattened, large_list)

    @patch("builtins.open", create=True)
    def test_file_reading(self, mock_open):
        """Test reading user agents from file."""
        # Mock file content
        mock_open.return_value.__enter__.return_value.read.return_value = (
            '["Mozilla/5.0 Chrome/120.0", "Mozilla/5.0 Firefox/121.0"]'
        )

        user_agents = self.processor._read_file("test.json", "json")
        self.assertEqual(len(user_agents), 2)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""

    def test_end_to_end_workflow(self):
        """Test complete workflow from parsing to analytics."""
        # Sample user agents
        user_agents = [
            "Mozilla/5.0 (iPhone16,3; CPU iPhone OS 17_2) Safari/604.1",
            "Mozilla/5.0 (SM-S928B; Android 14) Chrome/120.0",
            "Googlebot/2.1",
            "Mozilla/5.0 (Windows NT 10.0) Firefox/121.0",
            "Mozilla/5.0 (iPad; CPU OS 17_2) Safari/604.1",
        ]

        # Parse all agents
        results = batch_analyze(user_agents)
        self.assertEqual(len(results), len(user_agents))

        # Generate analytics
        report = generate_analytics(user_agents)

        # Verify report completeness
        self.assertGreater(report.total_requests, 0)
        self.assertGreater(len(report.browser_distribution), 0)
        self.assertGreater(len(report.os_distribution), 0)

        # Check for bot detection
        self.assertGreater(report.bot_detection_rate, 0)

        # Verify mobile vs desktop split
        total_categorized = sum(report.mobile_vs_desktop.values())
        self.assertEqual(total_categorized, len(user_agents))

    def test_performance_under_load(self):
        """Test performance with large dataset."""
        # Generate large dataset
        base_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2) Safari/604.1",
            "Mozilla/5.0 (Android 14) Chrome/120.0",
            "Mozilla/5.0 (Windows NT 10.0) Edge/120.0",
        ]
        large_dataset = base_agents * 100  # 300 user agents

        start_time = time.time()
        results = batch_analyze(large_dataset, max_workers=4)
        end_time = time.time()

        # Should complete in reasonable time
        processing_time = end_time - start_time
        self.assertLess(processing_time, 5.0)  # Should complete in 5 seconds

        # All should be processed
        self.assertEqual(len(results), len(large_dataset))

        # Most should be successfully parsed
        successful = [r for r in results if r.browser]
        self.assertGreater(len(successful) / len(results), 0.5)


if __name__ == "__main__":
    unittest.main()
