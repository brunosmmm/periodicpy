import subprocess
import re

LOADED_REGEX = re.compile(r'^\s*Loaded:\s*([a-zA-Z_\-\.,]+).*')
ACTIVE_REGEX = re.compile(r'^\s*Active:\s*([a-zA-Z_\-\.,]+).*')

class ServiceStatus(object):
    RUNNING = 0
    FAILED = 1
    DEAD = 2

class ServiceNotFoundError(Exception):
    pass

def check_service_status(service_name):

    check_cmd = ['systemctl', 'status', service_name]

    proc = subprocess.Popen(check_cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if proc.returncode != 0:
        #error: service not found or not running or failed
        for line in out.split('\n'):

            m = LOADED_REGEX.match(line)
            if m != None:
                if m.group(1) == "not-found":
                    raise ServiceNotFoundError('requested service not found')

                if m.group(1) == "loaded":
                    continue

            m = ACTIVE_REGEX.match(line)
            if m != None:
                if m.group(1) == "active":
                    return ServiceStatus.RUNNING

                if m.group(1) == "inactive":
                    return ServiceStatus.DEAD

                if m.group(1) == "failed":
                    return ServiceStatus.FAILED
        
    else:
        return ServiceStatus.RUNNING
