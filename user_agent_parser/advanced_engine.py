"""
Advanced User Agent Parsing Engine with ML-like Pattern Matching
Provides sophisticated device detection, browser fingerprinting, and confidence scoring.
"""

import hashlib
import json
import re
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, replace
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple

from .constants import MOBILE_DEVICE_CODE_NAME, DeviceType


class DetectionLevel(Enum):
    """Detection confidence levels."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class DeviceCategory(Enum):
    """Extended device categorization."""

    SMARTPHONE = "smartphone"
    TABLET = "tablet"
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    SMART_TV = "smart_tv"
    GAMING_CONSOLE = "gaming_console"
    SMART_WATCH = "smart_watch"
    IOT_DEVICE = "iot_device"
    BOT = "bot"
    UNKNOWN = "unknown"


@dataclass
class BrowserCapabilities:
    """Browser capability detection."""

    webgl_support: bool = False
    webrtc_support: bool = False
    service_worker_support: bool = False
    pwa_support: bool = False
    javascript_enabled: bool = True
    cookies_enabled: bool = True
    touch_support: bool = False
    accelerometer: bool = False
    geolocation: bool = False
    vr_support: bool = False
    webxr_support: bool = False


@dataclass
class SecurityFingerprint:
    """Security-focused fingerprinting data."""

    has_adblocker: bool = False
    privacy_mode: bool = False
    tracking_protection: bool = False
    do_not_track: bool = False
    security_headers: List[str] = None

    def __post_init__(self):
        if self.security_headers is None:
            self.security_headers = []


@dataclass
class AdvancedResult:
    """Comprehensive parsing result with confidence scoring."""

    # Basic detection
    browser: Optional[str] = None
    browser_version: Optional[str] = None
    browser_engine: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    device_type: Optional[str] = None
    device_name: Optional[str] = None
    device_brand: Optional[str] = None
    device_model: Optional[str] = None

    # Advanced detection
    device_category: DeviceCategory = DeviceCategory.UNKNOWN
    screen_resolution: Optional[str] = None
    pixel_density: Optional[str] = None
    architecture: Optional[str] = None
    cpu_cores: Optional[int] = None
    ram_gb: Optional[int] = None

    # Capabilities
    capabilities: BrowserCapabilities = None
    security: SecurityFingerprint = None

    # Confidence scoring
    detection_confidence: DetectionLevel = DetectionLevel.UNKNOWN
    confidence_score: float = 0.0
    detection_reasons: List[str] = None

    # Metadata
    is_mobile: bool = False
    is_tablet: bool = False
    is_desktop: bool = False
    is_bot: bool = False
    parsing_time_ms: float = 0.0
    fingerprint_hash: str = ""

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = BrowserCapabilities()
        if self.security is None:
            self.security = SecurityFingerprint()
        if self.detection_reasons is None:
            self.detection_reasons = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON representation."""
        data = self.to_dict()
        # Handle enum serialization
        data["device_category"] = self.device_category.value
        data["detection_confidence"] = self.detection_confidence.value
        return json.dumps(data, indent=2)


class AdvancedPatternMatcher:
    """ML-inspired pattern matching engine."""

    def __init__(self):
        self.device_patterns = self._build_device_patterns()
        self.browser_patterns = self._build_browser_patterns()
        self.os_patterns = self._build_os_patterns()
        self.bot_patterns = self._build_bot_patterns()
        self.feature_extractors = self._build_feature_extractors()

    def _build_device_patterns(self) -> Dict[str, List[Tuple[re.Pattern, Dict[str, Any]]]]:
        """Build sophisticated device detection patterns."""
        patterns = {
            "apple": [
                (
                    re.compile(r"iPhone.*?OS (\d+)_(\d+)", re.I),
                    {
                        "category": DeviceCategory.SMARTPHONE,
                        "brand": "Apple",
                        "confidence": DetectionLevel.HIGH,
                        "capabilities": {"touch_support": True, "accelerometer": True},
                    },
                ),
                (
                    re.compile(r"iPad.*?OS (\d+)_(\d+)", re.I),
                    {
                        "category": DeviceCategory.TABLET,
                        "brand": "Apple",
                        "confidence": DetectionLevel.HIGH,
                        "capabilities": {"touch_support": True},
                    },
                ),
                (
                    re.compile(r"Macintosh.*?Mac OS X (\d+)_(\d+)", re.I),
                    {"category": DeviceCategory.DESKTOP, "brand": "Apple", "confidence": DetectionLevel.HIGH},
                ),
            ],
            "android": [
                (
                    re.compile(r"Android.*?(\d+\.\d+).*?Mobile", re.I),
                    {
                        "category": DeviceCategory.SMARTPHONE,
                        "confidence": DetectionLevel.HIGH,
                        "capabilities": {"touch_support": True, "geolocation": True},
                    },
                ),
                (
                    re.compile(r"Android.*?(\d+\.\d+)(?!.*Mobile)", re.I),
                    {
                        "category": DeviceCategory.TABLET,
                        "confidence": DetectionLevel.MEDIUM,
                        "capabilities": {"touch_support": True},
                    },
                ),
            ],
            "samsung": [
                (
                    re.compile(r"SAMSUNG.*?(SM-[A-Z]\d{3})", re.I),
                    {"brand": "Samsung", "confidence": DetectionLevel.HIGH, "extract_model": True},
                )
            ],
            "gaming": [
                (
                    re.compile(r"PlayStation.*?(\d+)", re.I),
                    {"category": DeviceCategory.GAMING_CONSOLE, "brand": "Sony", "confidence": DetectionLevel.HIGH},
                ),
                (
                    re.compile(r"Xbox.*?(\w+)", re.I),
                    {
                        "category": DeviceCategory.GAMING_CONSOLE,
                        "brand": "Microsoft",
                        "confidence": DetectionLevel.HIGH,
                    },
                ),
            ],
        }

        # Compile patterns
        compiled_patterns = {}
        for category, pattern_list in patterns.items():
            compiled_patterns[category] = pattern_list

        return compiled_patterns

    def _build_browser_patterns(self) -> Dict[str, Tuple[re.Pattern, Dict[str, Any]]]:
        """Enhanced browser detection patterns."""
        return {
            "oculusbrowser": (
                re.compile(r"OculusBrowser/(\d+\.\d+)", re.I),
                {
                    "engine": "Blink",
                    "capabilities": {
                        "webgl_support": True,
                        "webrtc_support": True,
                        "vr_support": True,
                        "webxr_support": True,
                    },
                },
            ),
            "chrome": (
                re.compile(r"(?:Chrome|CriOS)/(\d+\.\d+)", re.I),
                {
                    "engine": "Blink",
                    "capabilities": {
                        "webgl_support": True,
                        "webrtc_support": True,
                        "service_worker_support": True,
                        "pwa_support": True,
                    },
                },
            ),
            "firefox": (
                re.compile(r"Firefox/(\d+\.\d+)", re.I),
                {
                    "engine": "Gecko",
                    "capabilities": {"webgl_support": True, "webrtc_support": True, "service_worker_support": True},
                },
            ),
            "safari": (
                re.compile(r"Version/(\d+\.\d+).*Safari", re.I),
                {"engine": "WebKit", "capabilities": {"webgl_support": True, "webrtc_support": False}},
            ),
            "edge": (
                re.compile(r"Edge/(\d+\.\d+)", re.I),
                {"engine": "EdgeHTML", "capabilities": {"webgl_support": True, "webrtc_support": True}},
            ),
        }

    def _build_os_patterns(self) -> Dict[str, Tuple[re.Pattern, Dict[str, Any]]]:
        """Enhanced OS detection patterns."""
        return {
            "windows": (re.compile(r"Windows NT (\d+\.\d+)", re.I), {"family": "Windows"}),
            "macos": (re.compile(r"Mac OS X (\d+)_(\d+)", re.I), {"family": "macOS"}),
            "linux": (re.compile(r"Linux.*?(\w+)", re.I), {"family": "Linux"}),
            "android": (re.compile(r"Android (\d+\.\d+)", re.I), {"family": "Android"}),
            "ios": (re.compile(r"OS (\d+)_(\d+)", re.I), {"family": "iOS"}),
        }

    def _build_bot_patterns(self) -> List[Tuple[re.Pattern, Dict[str, Any]]]:
        """Bot detection patterns."""
        return [
            (re.compile(r"Googlebot", re.I), {"bot_type": "search_engine", "vendor": "Google"}),
            (re.compile(r"Bingbot", re.I), {"bot_type": "search_engine", "vendor": "Microsoft"}),
            (re.compile(r"facebookexternalhit", re.I), {"bot_type": "social_media", "vendor": "Facebook"}),
            (re.compile(r"Twitterbot", re.I), {"bot_type": "social_media", "vendor": "Twitter"}),
            (re.compile(r"LinkedInBot", re.I), {"bot_type": "social_media", "vendor": "LinkedIn"}),
            (re.compile(r"WhatsApp", re.I), {"bot_type": "messaging", "vendor": "WhatsApp"}),
        ]

    def _build_feature_extractors(self) -> Dict[str, re.Pattern]:
        """Feature extraction patterns."""
        return {
            "architecture": re.compile(r"(?:x86_64|arm64|aarch64|i686|armv\w+)", re.I),
            "screen_resolution": re.compile(r"(\d{3,4}x\d{3,4})", re.I),
            "pixel_density": re.compile(r"(\d+(?:\.\d+)?dpi)", re.I),
            "webkit_version": re.compile(r"WebKit/(\d+\.\d+)", re.I),
            "build_number": re.compile(r"Build/([A-Z0-9]+)", re.I),
        }


class AdvancedUserAgentEngine:
    """Advanced user agent parsing engine with comprehensive analysis."""

    def __init__(self, enable_caching: bool = True, cache_size: int = 1024):
        self.pattern_matcher = AdvancedPatternMatcher()
        self.enable_caching = enable_caching
        self.cache_size = cache_size
        self.analytics = defaultdict(int)

        if enable_caching:
            self._parse_cached = lru_cache(maxsize=cache_size)(self._parse_internal)
        else:
            self._parse_cached = self._parse_internal

    def parse(
        self, user_agent: str, include_security: bool = False, include_capabilities: bool = True
    ) -> AdvancedResult:
        """
        Parse user agent with advanced detection and confidence scoring.

        Args:
            user_agent: User agent string to parse
            include_security: Include security fingerprinting
            include_capabilities: Include browser capabilities detection

        Returns:
            AdvancedResult with comprehensive analysis
        """
        start_time = time.time()

        result = replace(self._parse_cached(user_agent, include_security, include_capabilities))

        # Calculate parsing time
        result.parsing_time_ms = (time.time() - start_time) * 1000

        # Generate fingerprint hash
        result.fingerprint_hash = self._generate_fingerprint(user_agent, result)

        # Update analytics
        self.analytics["total_parses"] += 1
        self.analytics[f"confidence_{result.detection_confidence.value}"] += 1

        return result

    def _parse_internal(self, user_agent: str, include_security: bool, include_capabilities: bool) -> AdvancedResult:
        """Internal parsing logic."""
        result = AdvancedResult()
        confidence_factors = []

        # Bot detection first
        bot_info = self._detect_bot(user_agent)
        if bot_info:
            result.is_bot = True
            result.device_type = DeviceType.BOT
            result.device_category = DeviceCategory.BOT
            result.detection_confidence = DetectionLevel.HIGH
            result.confidence_score = 0.95
            result.detection_reasons.append("Bot pattern matched")
            return result

        # Browser detection
        browser_info = self._detect_browser(user_agent)
        if browser_info:
            result.browser = browser_info.get("name")
            result.browser_version = browser_info.get("version")
            result.browser_engine = browser_info.get("engine")
            if include_capabilities:
                result.capabilities = BrowserCapabilities(**browser_info.get("capabilities", {}))
            confidence_factors.append(("browser", 0.3))
            result.detection_reasons.append(f"Browser detected: {result.browser}")

        # OS detection
        os_info = self._detect_os(user_agent)
        if os_info:
            result.os = os_info.get("name")
            result.os_version = os_info.get("version")
            confidence_factors.append(("os", 0.2))
            result.detection_reasons.append(f"OS detected: {result.os}")

        # Device detection
        device_info = self._detect_device(user_agent)
        if device_info:
            result.device_name = device_info.get("name")
            result.device_brand = device_info.get("brand")
            result.device_model = device_info.get("model")
            result.device_category = device_info.get("category", DeviceCategory.UNKNOWN)
            result.device_type = self._map_category_to_type(result.device_category)
            confidence_factors.append(("device", 0.4))
            result.detection_reasons.append(f"Device detected: {result.device_name}")

        # Set device flags
        self._set_device_flags(result)

        # Feature extraction
        features = self._extract_features(user_agent)
        result.architecture = features.get("architecture")
        result.screen_resolution = features.get("screen_resolution")
        result.pixel_density = features.get("pixel_density")

        # Security fingerprinting
        if include_security:
            result.security = self._analyze_security(user_agent)

        # Calculate confidence
        self._calculate_confidence(result, confidence_factors)

        return result

    def _detect_bot(self, user_agent: str) -> Optional[Dict[str, Any]]:
        """Advanced bot detection."""
        for pattern, info in self.pattern_matcher.bot_patterns:
            if pattern.search(user_agent):
                return {"type": info["bot_type"], "vendor": info["vendor"]}
        return None

    def _detect_browser(self, user_agent: str) -> Optional[Dict[str, Any]]:
        """Advanced browser detection."""
        for name, (pattern, info) in self.pattern_matcher.browser_patterns.items():
            match = pattern.search(user_agent)
            if match:
                return {
                    "name": name.title(),
                    "version": match.group(1) if match.groups() else "Unknown",
                    "engine": info.get("engine"),
                    "capabilities": info.get("capabilities", {}),
                }
        return None

    def _detect_os(self, user_agent: str) -> Optional[Dict[str, Any]]:
        """Advanced OS detection."""
        for name, (pattern, info) in self.pattern_matcher.os_patterns.items():
            match = pattern.search(user_agent)
            if match:
                version = match.group(1) if match.groups() else "Unknown"
                if name == "macos" and len(match.groups()) > 1 or name == "ios" and len(match.groups()) > 1:
                    version = f"{match.group(1)}.{match.group(2)}"

                return {"name": info["family"], "version": version}
        return None

    def _detect_device(self, user_agent: str) -> Optional[Dict[str, Any]]:
        """Advanced device detection."""
        for category, patterns in self.pattern_matcher.device_patterns.items():
            for pattern, info in patterns:
                match = pattern.search(user_agent)
                if match:
                    device_info = {
                        "category": info.get("category", DeviceCategory.UNKNOWN),
                        "brand": info.get("brand"),
                        "confidence": info.get("confidence", DetectionLevel.MEDIUM),
                    }

                    # Extract model if specified
                    if info.get("extract_model") and match.groups():
                        device_info["model"] = match.group(1)
                        device_info["name"] = f"{device_info['brand']} {device_info['model']}"

                    # Try to get device name from constants
                    if not device_info.get("name") and device_info.get("model"):
                        device_info["name"] = MOBILE_DEVICE_CODE_NAME.get(device_info["model"], device_info["model"])

                    return device_info
        return None

    def _extract_features(self, user_agent: str) -> Dict[str, str]:
        """Extract additional features from user agent."""
        features = {}

        for feature, pattern in self.pattern_matcher.feature_extractors.items():
            match = pattern.search(user_agent)
            if match:
                features[feature] = match.group(1) if match.groups() else match.group(0)

        return features

    def _analyze_security(self, user_agent: str) -> SecurityFingerprint:
        """Analyze security-related indicators."""
        security = SecurityFingerprint()

        # Privacy indicators
        if re.search(r"Private|Incognito|InPrivate", user_agent, re.I):
            security.privacy_mode = True

        # Ad blocker indicators
        if re.search(r"uBlock|AdBlock|Ghostery", user_agent, re.I):
            security.has_adblocker = True

        # Tracking protection
        if re.search(r"TrackingProtection|DoNotTrack", user_agent, re.I):
            security.tracking_protection = True
            security.do_not_track = True

        return security

    def _set_device_flags(self, result: AdvancedResult) -> None:
        """Set device type flags."""
        if result.device_category in [DeviceCategory.SMARTPHONE]:
            result.is_mobile = True
        elif result.device_category in [DeviceCategory.TABLET]:
            result.is_tablet = True
        elif result.device_category in [DeviceCategory.DESKTOP, DeviceCategory.LAPTOP]:
            result.is_desktop = True
        elif result.device_category == DeviceCategory.BOT:
            result.is_bot = True

    def _map_category_to_type(self, category: DeviceCategory) -> str:
        """Map device category to legacy device type."""
        mapping = {
            DeviceCategory.SMARTPHONE: DeviceType.MOBILE,
            DeviceCategory.TABLET: DeviceType.MOBILE,
            DeviceCategory.DESKTOP: DeviceType.COMPUTER,
            DeviceCategory.LAPTOP: DeviceType.COMPUTER,
            DeviceCategory.BOT: DeviceType.BOT,
            DeviceCategory.SMART_TV: DeviceType.COMPUTER,
            DeviceCategory.GAMING_CONSOLE: DeviceType.COMPUTER,
        }
        return mapping.get(category, DeviceType.COMPUTER)

    def _calculate_confidence(self, result: AdvancedResult, confidence_factors: List[Tuple[str, float]]) -> None:
        """Calculate detection confidence score."""
        total_weight = sum(weight for _, weight in confidence_factors)

        if total_weight >= 0.8:
            result.detection_confidence = DetectionLevel.HIGH
            result.confidence_score = min(0.95, total_weight)
        elif total_weight >= 0.5:
            result.detection_confidence = DetectionLevel.MEDIUM
            result.confidence_score = total_weight
        elif total_weight > 0:
            result.detection_confidence = DetectionLevel.LOW
            result.confidence_score = total_weight
        else:
            result.detection_confidence = DetectionLevel.UNKNOWN
            result.confidence_score = 0.0

    def _generate_fingerprint(self, user_agent: str, result: AdvancedResult) -> str:
        """Generate unique fingerprint for the detection."""
        fingerprint_data = f"{user_agent}{result.browser}{result.os}{result.device_name}"
        return hashlib.md5(fingerprint_data.encode()).hexdigest()[:16]

    def batch_parse(self, user_agents: List[str], max_workers: int = 4) -> List[AdvancedResult]:
        """Parse multiple user agents in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ua = {executor.submit(self.parse, ua): ua for ua in user_agents}

            for future in as_completed(future_to_ua):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # Create error result
                    error_result = AdvancedResult()
                    error_result.detection_reasons.append(f"Parse error: {str(e)}")
                    results.append(error_result)

        return results

    def get_analytics(self) -> Dict[str, int]:
        """Get parsing analytics."""
        return dict(self.analytics)

    def clear_cache(self) -> None:
        """Clear the parsing cache."""
        if hasattr(self._parse_cached, "cache_clear"):
            self._parse_cached.cache_clear()

    def get_cache_info(self) -> Dict[str, int]:
        """Get cache statistics."""
        if hasattr(self._parse_cached, "cache_info"):
            info = self._parse_cached.cache_info()
            return {"hits": info.hits, "misses": info.misses, "maxsize": info.maxsize, "currsize": info.currsize}
        return {}


# Global instance for convenience
advanced_engine = AdvancedUserAgentEngine()


def parse_advanced(user_agent: str, **kwargs) -> AdvancedResult:
    """Convenience function for advanced parsing."""
    return advanced_engine.parse(user_agent, **kwargs)
