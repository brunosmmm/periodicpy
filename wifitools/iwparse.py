import re
from periodicpy.wifitools.wifiinfo import WifiInfo

BSS_REGEX = re.compile(r"^BSS\s([0-9A-Fa-f:]+).*")
SSID_REGEX = re.compile(r"\s*SSID:\s([a-zA-Z0-9_-]+).*")
SIGNAL_REGEX = re.compile(r"\s*signal:\s(-?[0-9]+\.[0-9]+)\sdBm.*")
KEY_REGEX = re.compile(r"\s*WPA:\s*\*.*")#re.compile(r"\s*Encryption\skey:\s*((on|off)).*")

class IWListParser(object):

    def __init__(self):
        pass

    @staticmethod
    def parse_text(text):

        wifi_list = []
        current_object = None
        for line in text:

            m = BSS_REGEX.match(line)
            if m != None:
                if current_object != None:
                    wifi_list.append(current_object)
                current_object = WifiInfo(m.group(1))
                continue

            m = SSID_REGEX.match(line)
            if m!= None:
                current_object.set_ssid(m.group(1))
                continue

            m = SIGNAL_REGEX.match(line)
            if m != None:
                current_object.set_signal(m.group(1))
                continue

            m = KEY_REGEX.match(line)
            if m != None:
                current_object.set_key(True)
                continue

        return wifi_list
