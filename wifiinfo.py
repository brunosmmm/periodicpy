import subprocess
import re

IFACE_STATUS_REGEX = re.compile(r"^[0-9]+:\s([a-zA-Z0-9]+).+state\s((DOWN|UP)).*")

class IFaceError(Exception):
    pass

def check_interface_up(interface_name):

    check_cmd = ['ip', 'link', 'show', interface_name]

    proc = subprocess.Popen(check_cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if out == None or proc.returncode != 0:
        raise IFaceError('Could not get interface state!')

    #use regex
    m = IFACE_STATUS_REGEX.match(out)
    if m != None:
        if m.group(1) == interface_name:
            if m.group(2) == "DOWN":
                return False
            elif m.group(2) == "UP":
                return True

    raise IFaceError('Unknown error while getting interface state')


class WifiInfo(object):
    """Store wi-fi information"""
    def __init__(self, ap_bss):
        self.BSS = ap_bss
        self.SSID = None
        self.current_signal = None
        self.has_key = False

    def set_ssid(self, ssid):
        self.SSID = ssid

    def set_signal(self, signal):
        self.current_signal = signal

    def set_key(self, has_key):
        if has_key == True or has_key == False:
            self.has_key = has_key
        elif has_key == "yes":
            self.has_key = True
        elif has_key == "no":
            self.has_key = False

    def __repr__(self):
        return "[{}] ({})".format(self.BSS, self.SSID)
