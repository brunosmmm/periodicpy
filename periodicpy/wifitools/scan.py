import subprocess
import re
from periodicpy.wifitools.iwparse import IWListParser
from periodicpy.wifitools.wifiinfo import check_interface_up, set_interface_up, IFaceError

class ScanError(Exception):
    pass

def scan_and_parse(interface_name, auto_up=False):

    #check if interface is UP
    iface_status = None
    try:
        iface_status = check_interface_up(interface_name)
    except IFaceError as err:
        raise #for now

    if iface_status == False:
        if auto_up == False:
            return None
        else:
            set_interface_up(interface_name)

    scan_cmd = ['iw', 'dev', interface_name, 'scan']

    proc = subprocess.Popen(scan_cmd,stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if out == None or proc.returncode != 0:
        raise ScanError('Cannot scan Wi-fi!')

    #parse
    iw_list = IWListParser.parse_text(out.split('\n'))

    return iw_list
