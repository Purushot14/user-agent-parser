"""
File: test_utils
Author: prakash
Created: 19/05/25.
"""

__author__ = "prakash"
__date__ = "19/05/25"

import pytest

from user_agent_parser import Parser
from user_agent_parser.parser import get_str_from_long_text_under_bract

TEST_VECTORS = [
    # WIN desktop 10
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.6312.86 Safari/537.36",
        {"browser": "Chrome", "os": "Windows", "dev_type": "Computer"},
    ),
    # ChromeOS on Chromebook
    (
        "Mozilla/5.0 (X11; CrOS aarch64 15054.66.0) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/95.0.4638.69 Safari/537.36",
        {"browser": "Chrome", "os": "Chrome OS", "dev_type": "Computer", "dev_name": "Chrome Book"},
    ),
    # iPhone - Safari
    (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        {"browser": "Safari", "os": "iOS", "dev_type": "Mobile", "dev_name": "Iphone"},
    ),
    # Android 13 – OnePlus
    (
        "Mozilla/5.0 (Linux; Android 13; ONEPLUS A6010 Build/TKQ1.230604.014) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.129 Mobile Safari/537.36",
        {"browser": "Chrome", "os": "Android", "dev_type": "Mobile", "dev_name": "OnePlus 6T"},
    ),
    # Android tablet – Samsung Tab
    (
        "Mozilla/5.0 (Linux; Android 12; SM-T970 Build/SP1A.210812.016) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.126 Safari/537.36",
        {"browser": "Chrome", "os": "Android", "dev_type": "Mobile", "dev_name": "Samsung Galaxy Tab S7+"},
    ),
    # Googlebot (bot path incl. _get_compatible_device)
    (
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        {"browser": None, "dev_type": "Bot"},
    ),
]


def test_get_str_from_long_text_under_bract():
    s = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    inside, stop = get_str_from_long_text_under_bract(s[12:])
    assert inside == "(Windows NT 10.0; Win64; x64)"
    # verify returned index is just past the closing “)”
    assert s[12:][stop - 1] == ")"


def test_browser_regex_cache_singleton():
    # First call populates the cache
    pat = Parser.browser_rules[0][0]
    first = Parser._get_browser_regex(pat)
    # Second call should hand back the *same* compiled pattern object
    assert Parser._get_browser_regex(pat) is first


@pytest.mark.parametrize(
    "code, expected",
    [
        ("ONEPLUS A6010", "OnePlus 6T"),
        ("ONEPLUS A5000", "OnePlus 5"),
        ("SM-T970", "Samsung Galaxy Tab S7+"),
        ("SM-M325F", "Samsung Galaxy M32"),
        ("PIXEL 8", "PIXEL 8"),  # passthrough
        ("RMX3085", "Realme"),
        ("CPH2451", "Oppo"),
        ("LGL123", "LG Mobile"),
        ("UnknownModel", None),
    ],
)
def test_device_code_helpers(code, expected):
    assert Parser._get_device_name_from_code(code) == expected


@pytest.mark.parametrize("ua, expected", TEST_VECTORS)
def test_parser_end_to_end(ua, expected):
    p = Parser(ua)
    browser, br_ver, os_, os_ver, dev_type, dev_name, dev_host = p()

    assert browser == expected["browser"]
    # some UA strings legitimately leave version or OS unset → guard with .get
    if "os" in expected:
        assert os_ == expected["os"]
    assert dev_type == expected["dev_type"]
    if "dev_name" in expected:
        # normalise case because code returns .title()
        assert (dev_name or "").lower() == expected["dev_name"].lower()


@pytest.mark.parametrize(
    "code, expected",
    [
        ("A065", "Nothing A065"),  # A0-prefix (“Nothing …”)
        ("POCO X6", "POCO X6"),  # POCO passthrough
        ("MI 11", "MI 11"),  # Xiaomi / MI
        ("M210XYZ", "Redmi"),  # M21* → Redmi
        ("V20PRO", "Vivo"),  # V20* → Vivo
    ],
)
def test_prefix_map_branches(code, expected):
    assert Parser._get_device_name_from_code(code) == expected


END_TO_END_VECTORS = [
    # 2.1 Generic Linux via fallback _get_device (len>1 and "Linux" in token[1])
    (
        "Mozilla/5.0 (FooBar; Linux x86_64) Gecko/20100101 Firefox/99.0",
        {"os": "Linux", "device_type": "Computer"},
    ),
    # 2.2 Macintosh desktop
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
        {"os": "Mac Os", "device_type": "Computer", "device_name": "Mac", "browser": "Safari"},
    ),
    # 2.3 Windows token → _get_windows_device
    (
        "Mozilla/5.0 (Windows; Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        {"os": "Windows", "device_type": "Computer"},
    ),
    # 2.4 iPad
    (
        "Mozilla/5.0 (iPad; CPU OS 15_4 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
        {"os": "iOS", "device_type": "Mobile", "device_name": "iPad"},
    ),
    # 2.5 X11 + Ubuntu → _get_x11_device else-branch
    (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0",
        {"os": "Ubuntu", "device_type": "Computer", "browser": "Firefox"},
    ),
    # 2.6 Google-Apps-Script “server” UA
    (
        "Mozilla/5.0 (compatible; Google-Apps-Script; script.google.com)",
        {"device_type": "Server", "os": "Google-Apps-Script", "device_host": "script.google.com"},
    ),
    # 2.7 Old Internet Explorer on Windows Phone → MSIE branch
    (
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; "
        "Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)",
        {"browser": "Internet Explorer", "os": "Windows", "device_type": "Computer"},
    ),
    # 2.8 Android WebView where device_name starts with “Android”
    (
        "Mozilla/5.0 (Linux; Android 14; Android 14; wv) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36",
        {"os": "Android", "device_type": "Mobile", "device_name": None},
    ),
]


@pytest.mark.parametrize("ua, expected", END_TO_END_VECTORS)
def test_remaining_code_paths(ua, expected):
    p = Parser(ua)
    res = p()  # tuple unpack left as-is
    (
        browser,
        _browser_ver,
        os_,
        _os_ver,
        dev_type,
        dev_name,
        dev_host,
    ) = res

    for key, value in expected.items():
        if key == "browser":
            assert browser == value
        elif key == "os":
            assert os_ == value
        elif key == "device_type":
            assert dev_type == value
        elif key == "device_name":
            assert dev_name == value
        elif key == "device_host":
            assert dev_host == value
