import subprocess
import re
from wifitools.iwparse import IWListParser
from wifitools.wifiinfo import check_interface_up, IFaceError

class ScanError(Exception):
    pass

def scan_and_parse(interface_name):

    #check if interface is UP
    iface_status = None
    try:
        iface_status = check_interface_up(interface_name)
    except IFaceError as err:
        raise #for now

    if iface_status == False:
        print "inteface is down, exiting"
        exit(0)
    else:
        print "inteface is up"

    scan_cmd = ['iw', 'dev', interface_name, 'scan']

    proc = subprocess.Popen(scan_cmd,stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if out == None or proc.returncode != 0:
        raise ScanError('Cannot scan Wi-fi!')

    #parse
    iw_list = IWListParser.parse_text(out.split('\n'))

    print iw_list
