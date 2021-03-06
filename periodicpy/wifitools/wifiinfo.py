import subprocess
import re
from json import JSONEncoder, JSONDecoder

IFACE_STATUS_REGEX = re.compile(r"^[0-9]+:\s([a-zA-Z0-9]+):\s<([A-Za-z,-_]+)>.+state\s((DOWN|UP)).*")

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
            if m.group(3) == "DOWN":
                pass
            elif m.group(3) == "UP":
                return True

        #even if down, check the flags
        flag_list = m.group(2).split(',')
        if "UP" in flag_list:
            return True
        else:
            return False

    raise IFaceError('Unknown error while getting interface state')

def set_interface_up(interface_name):

    check_cmd = ['ip', 'link', 'set', interface_name, 'up']
    proc = subprocess.Popen(check_cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode != 0:
        #raise only if some output was given
        if len(out) > 0:
            raise IFaceError('Could not set interface to UP state')

class WifiInfo(object):
    """Store wi-fi information"""
    def __init__(self, ap_bss):
        self.BSS = ap_bss
        self.SSID = None
        self.current_signal = None
        self.has_key = False

    @staticmethod
    def from_dict(d):
        ret = WifiInfo(None)
        ret.__dict__ = d
        return ret

    def set_ssid(self, ssid):
        self.SSID = ssid

    def set_signal(self, signal):
        self.current_signal = signal

    def set_key(self, has_key):
        if has_key == True or has_key == False:
            self.has_key = has_key
        elif has_key == "on":
            self.has_key = True
        elif has_key == "off":
            self.has_key = False

    def __repr__(self):
        return "[{}] ({}): {} dBm".format(self.BSS, self.SSID, self.current_signal)

class WifiInfoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class WifiInfoDecoder(JSONDecoder):
    def __init__(self):
        super(WifiInfoDecoder, self).__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        ret = WifiInfo(d['BSS'])
        ret.current_signal = d['current_signal']
        ret.has_key = d['has_key']
        ret.SSID = d['SSID']

        return ret
