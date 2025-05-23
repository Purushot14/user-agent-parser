"""
    Created by prakash at 02/03/22
"""
__author__ = "Prakash14"

import logging
from unittest import TestCase

from user_agent_parser.constants import OS, DeviceName, DeviceType
from user_agent_parser.parser import Parser

iphone_ua_str = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90"
    " Mobile/15E148 Safari/604.1"
)
ipad_ua_str = (
    "Mozilla/5.0 (iPad; CPU OS 14_3 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 "
    "Mobile/15E148 Safari/604.1"
)
chromebook_ua_str = (
    "Mozilla/5.0 (X11; CrOS aarch64 13982.82.0) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/92.0.4515.157 Safari/537.36"
)
redmi_ua_str = (
    "Mozilla/5.0 (Linux; Android 9; Redmi S2 Build/PKQ1.181203.001;"
    " wv) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Version/4.0 Chrome/92.0.4515.115 Mobile Safari/537.36 "
    "TrueMoneyName/truemoney TrueMoneyVersion/5.25.0"
    " TrueMoneyLanguage/th"
)
samsung_ua_str = (
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-N9810) "
    "AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/16.0 "
    "Chrome/92.0.4515.166 Mobile Safari/537.36"
)
mac_ua_str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55"
    " Safari/537.36"
)
mac_safari_ua_str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5"
    " Mobile/15E148 Safari/604.1"
)
win_firefox_ua_str = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:89.0) " "Gecko/20100101 Firefox/89.0"
android_firefox_ua_str = "Mozilla/5.0 (Android 8.0.0; Mobile; rv:97.0) " "Gecko/97.0 Firefox/97.0"
ubuntu_firefox_ua_str = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) " "Gecko/20100101 Firefox/72.0"
win_chrome_ua_str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/97.0.4692.71 Safari/537.36/CtmxtFNX-54"
)


class TestUserAgentParser(TestCase):
    def test_iphone_ua(self):
        ua_parser = Parser(iphone_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DeviceName.IPHONE)
        self.assertEqual(ua_parser.os_version, "13_6")
        self.assertEqual(ua_parser.os, OS.IOS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.90")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)

    def test_ipad_ua(self):
        ua_parser = Parser(ipad_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DeviceName.IPAD)
        self.assertEqual(ua_parser.os_version, "14_3")
        self.assertEqual(ua_parser.os, OS.IOS)
        self.assertEqual(ua_parser.browser, "Safari")
        self.assertEqual(ua_parser.browser_version, "14.0.2")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)

    def test_redmin_ua(self):
        ua_parser = Parser(redmi_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, "Redmi S2")
        self.assertEqual(ua_parser.os_version, "9")
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.115")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)

    def test_samsung_ua(self):
        ua_parser = Parser(samsung_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, "Samsung Galaxy Note 20")
        self.assertEqual(ua_parser.os_version, "11")
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.166")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)

    def test_android_firefox_ua(self):
        ua_parser = Parser(android_firefox_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DeviceName.ANDROID)
        self.assertEqual(ua_parser.os_version, "8.0.0")
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Firefox")
        self.assertEqual(ua_parser.browser_version, "97.0")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)

    def test_chromebook_ua(self):
        ua_parser = Parser(chromebook_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DeviceName.CHROME_BOOK)
        self.assertEqual(ua_parser.os_version, "13982.82.0")
        self.assertEqual(ua_parser.os, OS.CHROME_OS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.157")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_mac_ua(self):
        ua_parser = Parser(mac_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DeviceName.MAC)
        self.assertEqual(ua_parser.os_version, "10_12_0")
        self.assertEqual(ua_parser.os, OS.MAC_OS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "96.0.4664.55")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_mac_safari_ua(self):
        ua_parser = Parser(mac_safari_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DeviceName.MAC)
        self.assertEqual(ua_parser.os_version, "10_15")
        self.assertEqual(ua_parser.os, OS.MAC_OS)
        self.assertEqual(ua_parser.browser, "Safari")
        self.assertEqual(ua_parser.browser_version, "13.0.5")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_win_firefox_ua(self):
        ua_parser = Parser(win_firefox_ua_str)
        ua_parser()
        self.assertIsNone(ua_parser.device_name)
        self.assertEqual(ua_parser.os_version, "6.3")
        self.assertEqual(ua_parser.os, OS.WINDOWS)
        self.assertEqual(ua_parser.browser, "Firefox")
        self.assertEqual(ua_parser.browser_version, "89.0")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_win_chrome_ua(self):
        ua_parser = Parser(win_chrome_ua_str)
        ua_parser()
        self.assertIsNone(ua_parser.device_name)
        self.assertEqual(ua_parser.os_version, "10.0")
        self.assertEqual(ua_parser.os, OS.WINDOWS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "97.0.4692.71")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_ubuntu_firefox_ua(self):
        ua_parser = Parser(ubuntu_firefox_ua_str)
        ua_parser()
        self.assertIsNone(ua_parser.device_name)
        self.assertIsNone(ua_parser.os_version)
        self.assertEqual(ua_parser.os, "Ubuntu")
        self.assertEqual(ua_parser.browser, "Firefox")
        self.assertEqual(ua_parser.browser_version, "72.0")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_google_pixel_ua(self):
        ua_str = (
            "Mozilla/5.0 (Linux; Android 12; Pixel 6 Pro) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 "
            "Mobile Safari/537.36"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, "Google Pixel 6 Pro")

    def test_samsung_s22_ua(self):
        ua_str = (
            "Mozilla/5.0 (Linux; Android 12; SM-S908B) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, "Samsung Galaxy S22 Ultra")

    def test_iphone_14_ua(self):
        ua_str = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0"
            " Mobile/15E148 Safari/604.1"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.IOS)
        self.assertEqual(ua_parser.browser, "Safari")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, DeviceName.IPHONE)

    def test_huawei_ua(self):
        ua_str = (
            "Mozilla/5.0 (Linux; Android 10; HUAWEI P30 Pro) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127"
            " Mobile Safari/537.36"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, "Huawei P30 Pro")

    def test_windows_desktop_chrome(self):
        ua_str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.WINDOWS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_macos_safari(self):
        ua_str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.MAC_OS)
        self.assertEqual(ua_parser.browser, "Safari")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_firefox_browser(self):
        ua_str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.WINDOWS)
        self.assertEqual(ua_parser.browser, "Firefox")

    def test_ipad_device(self):
        ua_str = "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.IOS)
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, DeviceName.IPAD)

    def test_malformed_ua_string(self):
        ua_str = "Mozilla/5.0"  # Very short/incomplete UA string
        ua_parser = Parser(ua_str)
        ua_parser()
        # Assert default values based on your implementation

    def test_linux_firefox(self):
        ua_str = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
        ua_parser = Parser(ua_str)
        logging.info(ua_parser.device_host)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.LINUX)
        self.assertEqual(ua_parser.browser, "Firefox")
        self.assertEqual(ua_parser.device_type, DeviceType.COMPUTER)

    def test_samsung_s24_ultra_ua(self):
        ua_str = (
            "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/121.0.6167.164 Mobile Safari/537.36"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, "Samsung Galaxy")

    def test_samsung_tab_s10_ultra_ua(self):
        ua_str = (
            "Mozilla/5.0 (Linux; Android 14; SM-X920) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/123.0.6312.70 Mobile Safari/537.36"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, "Samsung Galaxy Tab")

    def test_samsung_a_ua(self):
        ua_str = (
            "Mozilla/5.0 (Linux; Android 14; SM-A26) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/123.0.6312.70 Mobile Safari/537.36"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, "Samsung Galaxy A26")

    def test_samsung_m_ua(self):
        ua_str = (
            "Mozilla/5.0 (Linux; Android 14; SM-M55) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/123.0.6312.70 Mobile Safari/537.36"
        )
        ua_parser = Parser(ua_str)
        ua_parser()
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.device_type, DeviceType.MOBILE)
        self.assertEqual(ua_parser.device_name, "Samsung Galaxy M55")
