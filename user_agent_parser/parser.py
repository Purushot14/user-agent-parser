"""
    Created by prakash at 02/03/22
"""
__author__ = 'Prakash14'

import re
from typing import List, Tuple

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

    def _get_platform_str(self):
        if not self._platform_str:
            self._platform_str, self.last_closing_bract = get_str_from_long_text_under_bract(self._user_agent_str[12:])
        return self._platform_str

    def _get_device(self, _token: List[str]):
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
        elif _token.__len__() > 1 and _token[1].__contains__("Linux"):
            self._os = OS.LINUX
            self._device_type = DEVICE_TYPE.COMPUTER

    def _get_macintosh_device(self, _token):
        self._os_version = _token[1].split()[-1]
        self._os = OS.MAC_OS
        self._device_type = DEVICE_TYPE.COMPUTER
        self._device_name = DEVICE_NAME.MAC

    def _get_windows_device(self, _token):
        self._os_version = _token[1].split()[-1]
        self._os = OS.WINDOWS
        self._device_type = DEVICE_TYPE.COMPUTER

    def _get_iphone_device(self, _token):
        self._os_version = _token[1].split()[3]
        self._os = OS.IOS
        self._device_type = DEVICE_TYPE.MOBILE
        self._device_name = DEVICE_NAME.IPHONE

    def _get_ipad_device(self, _token):
        self._os_version = _token[1].split()[2]
        self._os = OS.IOS
        self._device_type = DEVICE_TYPE.MOBILE
        self._device_name = DEVICE_NAME.IPAD

    @staticmethod
    def _get_device_name_from_code(device_code: str):
        up_device_code = device_code.upper()
        if up_device_code.startswith("SAMSUNG"):
            device_code = device_code.replace("SAMSUNG ", "")
        device_name = MOBILE_DEVICE_CODE_NAME.get(device_code)
        if device_code.startswith("SM-"):
            device_name = MOBILE_DEVICE_CODE_NAME.get(device_code[:7])
        if not device_name:
            if up_device_code.startswith("ONEPLUS"):
                code = device_code.split()[-1]
                if code[1].isdigit():
                    model_name = code[1]
                    if code[-2] == "1":
                        model_name = f"{model_name}T"
                    device_name = f"OnePlus {model_name}"
                    return device_name.strip()
            elif up_device_code.startswith("REDMI") or up_device_code.startswith("PIXEL") or \
                    up_device_code.startswith("LENOVO") or up_device_code.startswith("POCO") or \
                    up_device_code.startswith("VIVO") or up_device_code.startswith("MOTO") or \
                    up_device_code.startswith("MI"):
                return device_code
            elif up_device_code.startswith("SAMSUNG") or up_device_code.startswith("SM-"):
                sub_name = ""
                if up_device_code[4] in ("T", "X"):
                    sub_name = " Tab"
                elif up_device_code[4] in ("M", "A"):
                    sub_name = f" {up_device_code[3:6]}"
                return f"Samsung Galaxy{sub_name}"
            elif up_device_code.startswith("RMX"):
                return "Realme"
            elif up_device_code.startswith("CPH"):
                return "Oppo"
            elif up_device_code.startswith("M20") or up_device_code.startswith("M21"):
                return "Redmi"
            elif up_device_code.startswith("V20") or up_device_code.startswith("V21"):
                return "vivo"
            elif up_device_code.startswith("LM-") or up_device_code.startswith("LGL") or \
                    up_device_code.startswith("LG-"):
                return "LG Mobile"
            elif up_device_code.startswith("ASUS"):
                return "Asus"
        return device_name

    def _get_linux_device(self, _token: List[str]):
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
            self._device_name = device_name
        else:
            self._os = OS.LINUX
            self._device_type = DEVICE_TYPE.COMPUTER

    def _get_x11_device(self, _token):
        os_name = _token[1].split()[0]
        self._device_type = DEVICE_TYPE.COMPUTER
        if os_name == "CrOS":
            self._os_version = _token[1].split()[-1]
            self._os = OS.CHROME_OS
            self._device_name = DEVICE_NAME.CHROME_BOOK
        else:
            self._os = os_name

    def _get_compatible_device(self, _token):
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
            self._device_name = _token[1]
            self._device_type = DEVICE_TYPE.BOT
            self._device_host = _token[-1]

    def _get_platform(self):
        _platform_str = self._get_platform_str()
        if _platform_str:
            _platform_str = _platform_str.replace(" U;", "")
            _platform_str = _platform_str.replace(" arm_64;", "")
            _platform_str = _platform_str.replace(" arm;", "")
            token = [t.strip() for t in _platform_str[1:-1].split(";")]
            getattr(self, f"_get_{token[0].lower()}_device", self._get_device)(token)
        return _platform_str

    def _get_browser(self):
        for browser_pattern, browser in Parser.browser_rules:
            match = re.compile(self._browser_version_re.format(pattern=browser_pattern), re.I).search(
                self._user_agent_str[self.last_closing_bract:])
            if match:
                self._browser_version = match.group(1)
                self._browser = browser
                break

    @property
    def browser(self) -> str:
        if not self._browser:
            self.__call__()
        return self._browser

    @property
    def browser_version(self) -> str:
        if not self._browser:
            self.__call__()
        return self._browser_version

    @property
    def os(self) -> str:
        if not self._os:
            self.__call__()
        return self._os

    @property
    def os_version(self) -> str:
        if not self._os:
            self.__call__()
        return self._os_version

    @property
    def device_type(self) -> str:
        if not self._os:
            self.__call__()
        return self._device_type

    @property
    def device_name(self) -> str:
        if not self._os:
            self.__call__()
        return self._device_name

    @property
    def device_host(self) -> str:
        if not self._os:
            self.__call__()
        return self._device_host
