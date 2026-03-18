"""
Modern Device Database with Latest Device Models and Browsers
Comprehensive database of 2024-2025 devices, browsers, and their capabilities.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass
class DeviceSpec:
    """Detailed device specifications."""

    name: str
    brand: str
    category: str
    release_year: int
    screen_size: Optional[float] = None
    resolution: Optional[str] = None
    chipset: Optional[str] = None
    ram_gb: Optional[int] = None
    os_version: Optional[str] = None
    capabilities: Set[str] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = set()


# Modern Device Database (2024-2025)
MODERN_DEVICE_DATABASE = {
    # iPhone 15 Series (2024)
    "iPhone16,1": DeviceSpec(
        name="iPhone 15",
        brand="Apple",
        category="smartphone",
        release_year=2024,
        screen_size=6.1,
        resolution="2556x1179",
        chipset="A16 Bionic",
        ram_gb=6,
        capabilities={"5G", "wireless_charging", "face_id", "dynamic_island"},
    ),
    "iPhone16,2": DeviceSpec(
        name="iPhone 15 Plus",
        brand="Apple",
        category="smartphone",
        release_year=2024,
        screen_size=6.7,
        resolution="2796x1290",
        chipset="A16 Bionic",
        ram_gb=6,
        capabilities={"5G", "wireless_charging", "face_id", "dynamic_island"},
    ),
    "iPhone16,3": DeviceSpec(
        name="iPhone 15 Pro",
        brand="Apple",
        category="smartphone",
        release_year=2024,
        screen_size=6.1,
        resolution="2556x1179",
        chipset="A17 Pro",
        ram_gb=8,
        capabilities={"5G", "wireless_charging", "face_id", "dynamic_island", "titanium", "action_button"},
    ),
    # Samsung Galaxy S24 Series (2024)
    "SM-S921": DeviceSpec(
        name="Samsung Galaxy S24",
        brand="Samsung",
        category="smartphone",
        release_year=2024,
        screen_size=6.2,
        resolution="2340x1080",
        chipset="Snapdragon 8 Gen 3",
        ram_gb=8,
        capabilities={"5G", "wireless_charging", "ai_features", "galaxy_ai"},
    ),
    "SM-S926": DeviceSpec(
        name="Samsung Galaxy S24+",
        brand="Samsung",
        category="smartphone",
        release_year=2024,
        screen_size=6.7,
        resolution="3120x1440",
        chipset="Snapdragon 8 Gen 3",
        ram_gb=12,
        capabilities={"5G", "wireless_charging", "ai_features", "galaxy_ai"},
    ),
    "SM-S928": DeviceSpec(
        name="Samsung Galaxy S24 Ultra",
        brand="Samsung",
        category="smartphone",
        release_year=2024,
        screen_size=6.8,
        resolution="3120x1440",
        chipset="Snapdragon 8 Gen 3",
        ram_gb=16,
        capabilities={"5G", "wireless_charging", "s_pen", "ai_features", "galaxy_ai", "titanium"},
    ),
    # Google Pixel 8 Series (2024)
    "Pixel 8": DeviceSpec(
        name="Google Pixel 8",
        brand="Google",
        category="smartphone",
        release_year=2024,
        screen_size=6.2,
        resolution="2400x1080",
        chipset="Google Tensor G3",
        ram_gb=8,
        capabilities={"5G", "wireless_charging", "pure_android", "ai_features", "magic_eraser"},
    ),
    "Pixel 8 Pro": DeviceSpec(
        name="Google Pixel 8 Pro",
        brand="Google",
        category="smartphone",
        release_year=2024,
        screen_size=6.7,
        resolution="2992x1344",
        chipset="Google Tensor G3",
        ram_gb=12,
        capabilities={"5G", "wireless_charging", "pure_android", "ai_features", "magic_eraser", "temperature_sensor"},
    ),
    # OnePlus 12 Series (2024)
    "CPH2581": DeviceSpec(
        name="OnePlus 12",
        brand="OnePlus",
        category="smartphone",
        release_year=2024,
        screen_size=6.82,
        resolution="3168x1440",
        chipset="Snapdragon 8 Gen 3",
        ram_gb=16,
        capabilities={"5G", "wireless_charging", "fast_charging_100w", "alert_slider"},
    ),
    # iPad Pro M4 (2024)
    "iPad16,3": DeviceSpec(
        name="iPad Pro 11-inch (M4)",
        brand="Apple",
        category="tablet",
        release_year=2024,
        screen_size=11.0,
        resolution="2420x1668",
        chipset="M4",
        ram_gb=16,
        capabilities={"5G", "face_id", "apple_pencil_pro", "magic_keyboard", "thunderbolt"},
    ),
    "iPad16,4": DeviceSpec(
        name="iPad Pro 12.9-inch (M4)",
        brand="Apple",
        category="tablet",
        release_year=2024,
        screen_size=12.9,
        resolution="2732x2048",
        chipset="M4",
        ram_gb=16,
        capabilities={"5G", "face_id", "apple_pencil_pro", "magic_keyboard", "thunderbolt"},
    ),
    # MacBook Pro M4 (2024)
    "MacBookPro19,1": DeviceSpec(
        name="MacBook Pro 14-inch (M4)",
        brand="Apple",
        category="laptop",
        release_year=2024,
        screen_size=14.2,
        resolution="3024x1964",
        chipset="M4 Pro",
        ram_gb=32,
        capabilities={"thunderbolt_4", "macos_sequoia", "liquid_retina_xdr", "promotion"},
    ),
    # Gaming Consoles
    "PlayStation 5 Pro": DeviceSpec(
        name="PlayStation 5 Pro",
        brand="Sony",
        category="gaming_console",
        release_year=2024,
        resolution="4320x7680",  # 8K support
        chipset="AMD RDNA 3",
        ram_gb=32,
        capabilities={"8k_gaming", "ray_tracing", "pssr", "wifi_7"},
    ),
    # Smart TV (2024)
    "SAMSUNG_QN90D": DeviceSpec(
        name="Samsung Neo QLED QN90D",
        brand="Samsung",
        category="smart_tv",
        release_year=2024,
        screen_size=75.0,
        resolution="7680x4320",  # 8K
        capabilities={"8k", "hdr10_plus", "dolby_vision", "gaming_hub", "tizen_os"},
    ),
    # VR Headsets
    "Meta Quest 3": DeviceSpec(
        name="Meta Quest 3",
        brand="Meta",
        category="vr_headset",
        release_year=2024,
        resolution="2064x2208",  # Per eye
        chipset="Snapdragon XR2 Gen 2",
        ram_gb=8,
        capabilities={"mixed_reality", "passthrough", "hand_tracking", "wifi_6e"},
    ),
    # Smart Watches (2024)
    "Watch7,1": DeviceSpec(
        name="Apple Watch Series 9",
        brand="Apple",
        category="smart_watch",
        release_year=2024,
        screen_size=1.9,
        resolution="484x396",
        chipset="S9",
        ram_gb=1,
        capabilities={"health_sensors", "ecg", "blood_oxygen", "double_tap", "ultra_wideband"},
    ),
    "SM-R950": DeviceSpec(
        name="Samsung Galaxy Watch 6 Classic",
        brand="Samsung",
        category="smart_watch",
        release_year=2024,
        screen_size=1.5,
        resolution="480x480",
        capabilities={"health_sensors", "ecg", "blood_pressure", "rotating_bezel", "wear_os"},
    ),
}


# Modern Browser Database (2024-2025)
MODERN_BROWSER_DATABASE = {
    "Chrome": {
        "latest_version": "120.0.6099.109",
        "engine": "Blink",
        "capabilities": {
            "webgpu": True,
            "webassembly": True,
            "service_workers": True,
            "pwa": True,
            "webxr": True,
            "web_share": True,
            "payment_request": True,
            "background_sync": True,
            "push_notifications": True,
            "webrtc": True,
            "media_session": True,
            "gamepad": True,
            "bluetooth": True,
            "usb": True,
            "serial": True,
            "webgl2": True,
            "webcodecs": True,
            "origin_trial": True,
        },
        "security_features": {
            "coop": True,  # Cross-Origin-Opener-Policy
            "coep": True,  # Cross-Origin-Embedder-Policy
            "corp": True,  # Cross-Origin-Resource-Policy
            "permissions_policy": True,
            "trusted_types": True,
            "isolation": True,
        },
    },
    "Firefox": {
        "latest_version": "121.0",
        "engine": "Gecko",
        "capabilities": {
            "webgpu": False,  # Experimental
            "webassembly": True,
            "service_workers": True,
            "pwa": True,
            "webxr": False,
            "web_share": False,
            "payment_request": False,
            "background_sync": False,
            "push_notifications": True,
            "webrtc": True,
            "media_session": True,
            "gamepad": True,
            "bluetooth": False,
            "usb": False,
            "serial": False,
            "webgl2": True,
            "webcodecs": False,
            "tracking_protection": True,
        },
    },
    "Safari": {
        "latest_version": "17.1",
        "engine": "WebKit",
        "capabilities": {
            "webgpu": True,
            "webassembly": True,
            "service_workers": True,
            "pwa": True,
            "webxr": False,
            "web_share": True,
            "payment_request": True,
            "background_sync": False,
            "push_notifications": True,
            "webrtc": True,
            "media_session": False,
            "gamepad": True,
            "bluetooth": False,
            "usb": False,
            "serial": False,
            "webgl2": True,
            "webcodecs": True,
            "intelligent_tracking_prevention": True,
            "private_relay": True,
        },
    },
    "Edge": {
        "latest_version": "120.0.2210.77",
        "engine": "Blink",
        "capabilities": {
            "webgpu": True,
            "webassembly": True,
            "service_workers": True,
            "pwa": True,
            "webxr": True,
            "web_share": True,
            "payment_request": True,
            "background_sync": True,
            "push_notifications": True,
            "webrtc": True,
            "media_session": True,
            "gamepad": True,
            "bluetooth": True,
            "usb": True,
            "serial": True,
            "webgl2": True,
            "webcodecs": True,
            "enhanced_security": True,
            "smartscreen": True,
        },
    },
}


# Modern OS Database (2024-2025)
MODERN_OS_DATABASE = {
    "iOS": {
        "latest_version": "17.2",
        "features": {
            "standby_mode": True,
            "interactive_widgets": True,
            "contact_posters": True,
            "live_voicemail": True,
            "check_in": True,
            "airdrop_improvements": True,
            "focus_modes": True,
            "stage_manager": True,
            "app_tracking_transparency": True,
            "privacy_report": True,
        },
    },
    "Android": {
        "latest_version": "14.0",
        "features": {
            "magic_eraser": True,
            "live_translate": True,
            "car_crash_detection": True,
            "material_you": True,
            "privacy_dashboard": True,
            "approximate_location": True,
            "clipboard_access_notifications": True,
            "nearby_share": True,
            "digital_wellbeing": True,
            "adaptive_battery": True,
        },
    },
    "Windows": {
        "latest_version": "11 23H2",
        "features": {
            "copilot": True,
            "widgets": True,
            "snap_layouts": True,
            "virtual_desktops": True,
            "microsoft_teams_integration": True,
            "windows_hello": True,
            "windows_defender": True,
            "power_automate": True,
            "xbox_game_pass_integration": True,
        },
    },
    "macOS": {
        "latest_version": "14.2 Sonoma",
        "features": {
            "interactive_widgets": True,
            "game_mode": True,
            "web_apps_in_dock": True,
            "profiles_in_safari": True,
            "focus_modes": True,
            "stage_manager": True,
            "continuity_camera": True,
            "universal_control": True,
            "airdrop_improvements": True,
            "privacy_report": True,
        },
    },
}


class ModernDeviceDetector:
    """Advanced device detection using modern device database."""

    def __init__(self):
        self.device_db = MODERN_DEVICE_DATABASE
        self.browser_db = MODERN_BROWSER_DATABASE
        self.os_db = MODERN_OS_DATABASE

        # Compile regex patterns for efficient matching
        self.device_patterns = self._compile_device_patterns()
        self.browser_patterns = self._compile_browser_patterns()
        self.os_patterns = self._compile_os_patterns()

    def _compile_device_patterns(self) -> Dict[str, re.Pattern]:
        """Compile device detection patterns."""
        patterns = {}

        # Apple devices
        patterns["iphone_15"] = re.compile(r"iPhone16,[1-4]", re.I)
        patterns["ipad_m4"] = re.compile(r"iPad16,[3-6]", re.I)
        patterns["macbook_m4"] = re.compile(r"MacBookPro19,[1-4]", re.I)
        patterns["apple_watch_9"] = re.compile(r"Watch7,[1-4]", re.I)

        # Samsung devices
        patterns["galaxy_s24"] = re.compile(r"SM-S92[1568]", re.I)
        patterns["galaxy_watch_6"] = re.compile(r"SM-R95[0-9]", re.I)

        # Google Pixel
        patterns["pixel_8"] = re.compile(r"Pixel 8( Pro)?", re.I)

        # OnePlus
        patterns["oneplus_12"] = re.compile(r"CPH258[1-9]|OnePlus.*12", re.I)

        # Gaming consoles
        patterns["ps5_pro"] = re.compile(r"PlayStation 5.*Pro", re.I)
        patterns["xbox_series"] = re.compile(r"Xbox Series [XS]", re.I)

        # VR/AR
        patterns["meta_quest_3"] = re.compile(r"Quest 3|OculusBrowser.*Quest", re.I)
        patterns["apple_vision"] = re.compile(r"Apple Vision Pro|visionOS", re.I)

        return patterns

    def _compile_browser_patterns(self) -> Dict[str, re.Pattern]:
        """Compile modern browser detection patterns."""
        return {
            "chrome_120": re.compile(r"Chrome/12[0-9]\.\d+", re.I),
            "firefox_121": re.compile(r"Firefox/12[1-9]\.\d+", re.I),
            "safari_17": re.compile(r"Version/17\.\d+.*Safari", re.I),
            "edge_120": re.compile(r"Edg/12[0-9]\.\d+", re.I),
            "arc_browser": re.compile(r"Arc/", re.I),
            "brave": re.compile(r"Brave/", re.I),
            "opera_gx": re.compile(r"OPR/.*GX", re.I),
            "vivaldi": re.compile(r"Vivaldi/", re.I),
        }

    def _compile_os_patterns(self) -> Dict[str, re.Pattern]:
        """Compile modern OS detection patterns."""
        return {
            "ios_17": re.compile(r"OS 17_\d+", re.I),
            "android_14": re.compile(r"Android 14", re.I),
            "windows_11": re.compile(r"Windows NT 10\.0.*22000|Windows NT 10\.0.*22621", re.I),
            "macos_14": re.compile(r"Mac OS X 14_\d+", re.I),
            "visionos": re.compile(r"visionOS \d+\.\d+", re.I),
            "wear_os": re.compile(r"Wear OS \d+", re.I),
            "tizen": re.compile(r"Tizen \d+\.\d+", re.I),
            "harmony_os": re.compile(r"HarmonyOS \d+\.\d+", re.I),
        }

    def detect_modern_device(self, user_agent: str) -> Optional[DeviceSpec]:
        """Detect modern devices from user agent."""
        for pattern_name, pattern in self.device_patterns.items():
            if pattern.search(user_agent):
                # Map pattern to device spec
                device_key = self._map_pattern_to_device(pattern_name, user_agent)
                if device_key and device_key in self.device_db:
                    return self.device_db[device_key]
        return None

    def detect_modern_browser(self, user_agent: str) -> Optional[Dict]:
        """Detect modern browser capabilities."""
        for pattern_name, pattern in self.browser_patterns.items():
            if pattern.search(user_agent):
                browser_name = pattern_name.split("_")[0].title()
                if browser_name.lower() in ["chrome", "firefox", "safari", "edge"]:
                    return self.browser_db.get(browser_name, {})
        return None

    def detect_modern_os(self, user_agent: str) -> Optional[Dict]:
        """Detect modern OS features."""
        for pattern_name, pattern in self.os_patterns.items():
            if pattern.search(user_agent):
                os_name = pattern_name.split("_")[0]
                if os_name == "ios":
                    return self.os_db.get("iOS", {})
                elif os_name == "android":
                    return self.os_db.get("Android", {})
                elif os_name == "windows":
                    return self.os_db.get("Windows", {})
                elif os_name == "macos":
                    return self.os_db.get("macOS", {})
        return None

    def _map_pattern_to_device(self, pattern_name: str, user_agent: str) -> Optional[str]:
        """Map pattern match to device database key."""
        # iPhone 15 series
        if pattern_name == "iphone_15":
            if "iPhone16,1" in user_agent:
                return "iPhone16,1"
            elif "iPhone16,2" in user_agent:
                return "iPhone16,2"
            elif "iPhone16,3" in user_agent:
                return "iPhone16,3"

        # Samsung Galaxy S24 series
        elif pattern_name == "galaxy_s24":
            if "SM-S921" in user_agent:
                return "SM-S921"
            elif "SM-S926" in user_agent:
                return "SM-S926"
            elif "SM-S928" in user_agent:
                return "SM-S928"

        # Google Pixel 8 series
        elif pattern_name == "pixel_8":
            if "Pixel 8 Pro" in user_agent:
                return "Pixel 8 Pro"
            elif "Pixel 8" in user_agent:
                return "Pixel 8"

        # Add more mappings as needed
        return None

    def get_device_capabilities(self, device_spec: DeviceSpec) -> List[str]:
        """Get comprehensive device capabilities."""
        capabilities = list(device_spec.capabilities)

        # Add inferred capabilities based on specs
        if device_spec.ram_gb and device_spec.ram_gb >= 8:
            capabilities.append("high_performance")

        if device_spec.release_year >= 2024:
            capabilities.append("latest_generation")

        if device_spec.chipset and any(chip in device_spec.chipset for chip in ["A17", "M4", "Snapdragon 8 Gen 3"]):
            capabilities.append("flagship_performance")

        if device_spec.resolution and ("4320" in device_spec.resolution or "7680" in device_spec.resolution):
            capabilities.append("8k_display")
        elif device_spec.resolution and "2556" in device_spec.resolution:
            capabilities.append("high_resolution_display")

        return capabilities


# Global instance
modern_detector = ModernDeviceDetector()
