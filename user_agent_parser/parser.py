"""
    Created by prakash at 02/03/22
    Optimized version
"""
__author__ = 'Prakash14'

import re
from typing import List, Tuple, Dict, Callable, Optional, Any

from .constants import MOBILE_DEVICE_CODE_NAME, DEVICE_TYPE, OS, DEVICE_NAME


def get_str_from_long_text_under_bract(search_str: str):
    start_idx = search_str.find("(")
    stop_idx = 0
    bract_counter = 0
    for match in re.finditer(r'\(|\)', search_str):
        stop_idx = match.start()
        if search_str[stop_idx] == '(':
            bract_counter += 1
        else:
            bract_counter -= 1
        if bract_counter == 0:
            break
    _str = search_str[start_idx:stop_idx + 1]
    return _str, stop_idx + 1


class Parser:
    # Browser detection rules
    browser_rules: Tuple[Tuple[str, str]] = (
        ("googlebot", "Google"),
        ("msnbot", "MSN"),
        ("yahoo", "Yahoo"),
        ("ask jeeves", "Ask"),
        (r"aol|america\s+online\s+browser", "aol"),
        (r"opera|opr", "Opera"),
        ("edge|edg", "Edge"),
        ("chrome|crios", "Chrome"),
        ("seamonkey", "Seamonkey"),
        ("firefox|firebird|phoenix|iceweasel", "Firefox"),
        ("galeon", "Galeon"),
        ("safari|version", "Safari"),
        ("webkit", "Webkit"),
        ("camino", "Camino"),
        ("konqueror", "Konqueror"),
        ("k-meleon", "Kmeleon"),
        ("netscape", "Netscape"),
        (r"msie|microsoft\s+internet\s+explorer|trident/.+? rv:", "Internet Explorer"),
        ("lynx", "Lynx"),
        ("links", "Links"),
        ("Baiduspider", "Baidu"),
        ("bingbot", "Bing"),
        ("mozilla", "Mozilla"),
    )

    _browser_version_re = r"(?:{pattern})[/\sa-z(]*(\d+[.\da-z]+)?"

    # Pre-compiled regex patterns for browser detection
    _browser_version_patterns: Dict[str, re.Pattern] = {}

    # Device code handlers
    _device_handlers: Dict[str, Callable[[str], str]] = {}

    def __init__(self, user_agent_str: str):
        self._user_agent_str = user_agent_str
        self._platform_str = None
        self.last_closing_bract = None
        self._browser = None
        self._browser_version = None
        self._os = None
        self._os_version = None
        self._device_type = None
        self._device_name = None
        self._device_host = None

    def __call__(self, *args, **kwargs):
        self._get_platform()
        self._get_browser()
        return self._browser, self._browser_version, self._os, self._os_version, self._device_type, \
               self._device_name, self._device_host

    def _lazy_init(self) -> None:
        """Helper method for lazy initialization"""
        if not self._browser:
            self.__call__()

    def _get_platform_str(self):
        if not self._platform_str:
            self._platform_str, self.last_closing_bract = get_str_from_long_text_under_bract(self._user_agent_str[12:])
        return self._platform_str

    def _get_device(self, _token: List[str]) -> None:
        """
        :param _token: :return:
        TODO: Need to hand windows phone and UC Browser
        Sample:  Mozilla/5.0 (compatible; MSIE 10.0; Windows
        Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920) UCBrowser/10.1.0.563 Mobile
        """
        if _token[0].startswith("Windows NT"):
            self._os_version = _token[0].split()[-1]
            self._os = OS.WINDOWS
            self._device_type = DEVICE_TYPE.COMPUTER
        elif _token[0].startswith("Android"):
            self._os_version = _token[0].split()[-1]
            self._os = OS.ANDROID
            self._device_type = DEVICE_TYPE.MOBILE
            self._device_name = DEVICE_NAME.ANDROID
        elif _token[0].startswith(OS.WINDOWS_PHONE):
            self._os_version = _token[0].split()[-1]
            self._os = OS.WINDOWS_PHONE
            self._device_type = DEVICE_TYPE.MOBILE
        elif _token[0].startswith("Apple Mac OS"):
            self._os_version = _token[0].split()[-1]
            self._os = OS.MAC_OS
            self._device_type = DEVICE_TYPE.COMPUTER
        elif len(_token) > 1 and "Linux" in _token[1]:
            self._os = OS.LINUX
            self._device_type = DEVICE_TYPE.COMPUTER

    def _get_macintosh_device(self, _token: List[str]) -> None:
        self._os_version = _token[1].split()[-1]
        self._os = OS.MAC_OS
        self._device_type = DEVICE_TYPE.COMPUTER
        self._device_name = DEVICE_NAME.MAC

    def _get_windows_device(self, _token: List[str]) -> None:
        self._os_version = _token[1].split()[-1]
        self._os = OS.WINDOWS
        self._device_type = DEVICE_TYPE.COMPUTER

    def _get_iphone_device(self, _token: List[str]) -> None:
        self._os_version = _token[1].split()[3]
        self._os = OS.IOS
        self._device_type = DEVICE_TYPE.MOBILE
        self._device_name = DEVICE_NAME.IPHONE

    def _get_ipad_device(self, _token: List[str]) -> None:
        self._os_version = _token[1].split()[2]
        self._os = OS.IOS
        self._device_type = DEVICE_TYPE.MOBILE
        self._device_name = DEVICE_NAME.IPAD

    @staticmethod
    def _handle_oneplus(device_code: str) -> Optional[str]:
        code = device_code.split()[-1]
        if code[1].isdigit():
            model_name = code[1]
            if code[-2] == "1":
                model_name = f"{model_name}T"
            return f"OnePlus {model_name}".strip()
        return None

    @staticmethod
    def _handle_samsung(device_code: str) -> str:
        up_device_code = device_code.upper()
        sub_name = ""
        if up_device_code[4] in ("T", "X"):
            sub_name = " Tab"
        elif up_device_code[4] in ("M", "A"):
            sub_name = f" {up_device_code[3:6]}"
        return f"Samsung Galaxy{sub_name}"

    @staticmethod
    def _get_device_name_from_code(device_code: str) -> Optional[str]:
        # Handle Samsung special case
        up_device_code = device_code.upper()
        if up_device_code.startswith("SAMSUNG"):
            device_code = device_code.replace("SAMSUNG ", "")

        # Check device code map first
        device_name = MOBILE_DEVICE_CODE_NAME.get(device_code)
        if device_code.startswith("SM-"):
            device_name = MOBILE_DEVICE_CODE_NAME.get(device_code[:7])

        if device_name:
            return device_name

        # Map of prefixes to device names or functions
        prefix_map = {
            "ONEPLUS": lambda c: Parser._handle_oneplus(c),
            "REDMI": lambda c: c,
            "PIXEL": lambda c: c,
            "LENOVO": lambda c: c,
            "POCO": lambda c: c,
            "VIVO": lambda c: c,
            "MOTO": lambda c: c,
            "MI": lambda c: c,
            "SAMSUNG": lambda c: "Samsung Galaxy",
            "SM-": lambda c: Parser._handle_samsung(c),
            "RMX": lambda c: "Realme",
            "CPH": lambda c: "Oppo",
            "M20": lambda c: "Redmi",
            "M21": lambda c: "Redmi",
            "V20": lambda c: "vivo",
            "V21": lambda c: "vivo",
            "LM-": lambda c: "LG Mobile",
            "LGL": lambda c: "LG Mobile",
            "LG-": lambda c: "LG Mobile",
            "ASUS": lambda c: "Asus",
            "A0": lambda c: f"Nothing {c}",
        }

        # Check each prefix
        for prefix, handler in prefix_map.items():
            if up_device_code.startswith(prefix):
                return handler(device_code)

        return None

    def _get_linux_device(self, _token: List[str]) -> None:
        if _token[1].lower().startswith("android"):
            self._os_version = _token[1].split()[-1]
            self._os = OS.ANDROID
            self._device_type = DEVICE_TYPE.MOBILE
            device_name = _token[-1] if _token[-1] != "wv" else _token[-2]
            device_name = device_name.split("Build/")[0]
            if device_name.startswith(OS.ANDROID):
                self._os_version = device_name.split()[-1]
                device_name = None
            else:
                device_name = self._get_device_name_from_code(device_name.strip()) or device_name
            self._device_name = device_name.title()
        else:
            self._os = OS.LINUX
            self._device_type = DEVICE_TYPE.COMPUTER

    def _get_x11_device(self, _token: List[str]) -> None:
        os_name = _token[1].split()[0]
        self._device_type = DEVICE_TYPE.COMPUTER
        if os_name == "CrOS":
            self._os_version = _token[1].split()[-1]
            self._os = OS.CHROME_OS
            self._device_name = DEVICE_NAME.CHROME_BOOK
        else:
            self._os = os_name

    def _get_compatible_device(self, _token: List[str]) -> None:
        os_name = _token[1].split()[0]
        if _token[1].lower() == "google-apps-script":
            self._os = os_name
            self._device_type = DEVICE_TYPE.SERVER
            try:
                self._device_host = _token[3]
            except IndexError:
                pass
        elif os_name.upper() == "MSIE":
            self._browser = "Internet Explorer"
            self._os_version = _token[2].split()[-1]
            self._os = OS.WINDOWS
            self._device_type = DEVICE_TYPE.COMPUTER
        else:
            self._os = _token[1]
            self._device_name = _token[1].title()
            self._device_type = DEVICE_TYPE.BOT
            self._device_host = _token[-1]

    def _get_platform(self) -> Optional[str]:
        _platform_str = self._get_platform_str()
        if _platform_str:
            # Combine multiple replacements efficiently
            for pattern in (" U;", " arm_64;", " arm;"):
                _platform_str = _platform_str.replace(pattern, "")

            token = [t.strip() for t in _platform_str[1:-1].split(";")]
            handler_name = f"_get_{token[0].lower()}_device"
            handler = getattr(self, handler_name, self._get_device)
            handler(token)
        return _platform_str

    @classmethod
    def _get_browser_regex(cls, browser_pattern: str) -> re.Pattern:
        """Get or create compiled regex pattern for browser detection"""
        if browser_pattern not in cls._browser_version_patterns:
            pattern = cls._browser_version_re.format(pattern=browser_pattern)
            cls._browser_version_patterns[browser_pattern] = re.compile(pattern, re.I)
        return cls._browser_version_patterns[browser_pattern]

    def _get_browser(self) -> None:
        for browser_pattern, browser in self.browser_rules:
            match = self._get_browser_regex(browser_pattern).search(
                self._user_agent_str[self.last_closing_bract:])
            if match:
                self._browser_version = match.group(1)
                self._browser = browser
                break

    @property
    def browser(self) -> str:
        self._lazy_init()
        return self._browser

    @property
    def browser_version(self) -> str:
        self._lazy_init()
        return self._browser_version

    @property
    def os(self) -> str:
        self._lazy_init()
        return self._os

    @property
    def os_version(self) -> str:
        self._lazy_init()
        return self._os_version

    @property
    def device_type(self) -> str:
        self._lazy_init()
        return self._device_type

    @property
    def device_name(self) -> str:
        self._lazy_init()
        return self._device_name

    @property
    def device_host(self) -> str:
        self._lazy_init()
        return self._device_host