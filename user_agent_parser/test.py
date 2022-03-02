"""
    Created by prakash at 02/03/22
"""
__author__ = 'Prakash14'

from unittest import TestCase

from .constants import DEVICE_NAME, OS, DEVICE_TYPE
from .parser import Parser

iphone_ua_str = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/92.0.4515.90 Mobile/15E148 Safari/604.1"
ipad_ua_str = "Mozilla/5.0 (iPad; CPU OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1"
chromebook_ua_str = "Mozilla/5.0 (X11; CrOS aarch64 13982.82.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.157 Safari/537.36"
redmi_ua_str = "Mozilla/5.0 (Linux; Android 9; Redmi S2 Build/PKQ1.181203.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.115 Mobile Safari/537.36 TrueMoneyName/truemoney TrueMoneyVersion/5.25.0 TrueMoneyLanguage/th"
samsung_ua_str = "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-N9810) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/16.0 Chrome/92.0.4515.166 Mobile Safari/537.36"
mac_ua_str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36"
mac_safari_ua_str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Safari/604.1"
win_firefox_ua_str = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
android_firefox_ua_str = "Mozilla/5.0 (Android 8.0.0; Mobile; rv:97.0) Gecko/97.0 Firefox/97.0"
ubuntu_firefox_ua_str = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
win_chrome_ua_str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36/CtmxtFNX-54"


class TestUserAgentParser(TestCase):

    def test_iphone_ua(self):
        ua_parser = Parser(iphone_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DEVICE_NAME.IPHONE)
        self.assertEqual(ua_parser.os_version, "13_6")
        self.assertEqual(ua_parser.os, OS.IOS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.90")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.MOBILE)

    def test_ipad_ua(self):
        ua_parser = Parser(ipad_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DEVICE_NAME.IPAD)
        self.assertEqual(ua_parser.os_version, "14_3")
        self.assertEqual(ua_parser.os, OS.IOS)
        self.assertEqual(ua_parser.browser, "Safari")
        self.assertEqual(ua_parser.browser_version, "14.0.2")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.MOBILE)

    def test_redmin_ua(self):
        ua_parser = Parser(redmi_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, "Redmi S2")
        self.assertEqual(ua_parser.os_version, "9")
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.115")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.MOBILE)

    def test_samsung_ua(self):
        ua_parser = Parser(samsung_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, "Samsung Galaxy Note 20")
        self.assertEqual(ua_parser.os_version, "11")
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.166")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.MOBILE)

    def test_android_firefox_ua(self):
        ua_parser = Parser(android_firefox_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DEVICE_NAME.ANDROID)
        self.assertEqual(ua_parser.os_version, "8.0.0")
        self.assertEqual(ua_parser.os, OS.ANDROID)
        self.assertEqual(ua_parser.browser, "Firefox")
        self.assertEqual(ua_parser.browser_version, "97.0")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.MOBILE)

    def test_chromebook_ua(self):
        ua_parser = Parser(chromebook_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DEVICE_NAME.CHROME_BOOK)
        self.assertEqual(ua_parser.os_version, "13982.82.0")
        self.assertEqual(ua_parser.os, OS.CHROME_OS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "92.0.4515.157")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.COMPUTER)

    def test_mac_ua(self):
        ua_parser = Parser(mac_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DEVICE_NAME.MAC)
        self.assertEqual(ua_parser.os_version, "10_12_0")
        self.assertEqual(ua_parser.os, OS.MAC_OS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "96.0.4664.55")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.COMPUTER)

    def test_mac_safari_ua(self):
        ua_parser = Parser(mac_safari_ua_str)
        ua_parser()
        self.assertEqual(ua_parser.device_name, DEVICE_NAME.MAC)
        self.assertEqual(ua_parser.os_version, "10_15")
        self.assertEqual(ua_parser.os, OS.MAC_OS)
        self.assertEqual(ua_parser.browser, "Safari")
        self.assertEqual(ua_parser.browser_version, "13.0.5")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.COMPUTER)

    def test_win_firefox_ua(self):
        ua_parser = Parser(win_firefox_ua_str)
        ua_parser()
        self.assertIsNone(ua_parser.device_name)
        self.assertEqual(ua_parser.os_version, "6.3")
        self.assertEqual(ua_parser.os, OS.WINDOWS)
        self.assertEqual(ua_parser.browser, "Firefox")
        self.assertEqual(ua_parser.browser_version, "89.0")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.COMPUTER)

    def test_win_chrome_ua(self):
        ua_parser = Parser(win_chrome_ua_str)
        ua_parser()
        self.assertIsNone(ua_parser.device_name)
        self.assertEqual(ua_parser.os_version, "10.0")
        self.assertEqual(ua_parser.os, OS.WINDOWS)
        self.assertEqual(ua_parser.browser, "Chrome")
        self.assertEqual(ua_parser.browser_version, "97.0.4692.71")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.COMPUTER)

    def test_ubuntu_firefox_ua(self):
        ua_parser = Parser(ubuntu_firefox_ua_str)
        ua_parser()
        self.assertIsNone(ua_parser.device_name)
        self.assertIsNone(ua_parser.os_version)
        self.assertEqual(ua_parser.os, "Ubuntu")
        self.assertEqual(ua_parser.browser, "Firefox")
        self.assertEqual(ua_parser.browser_version, "72.0")
        self.assertEqual(ua_parser.device_type, DEVICE_TYPE.COMPUTER)
