import subprocess

def log(message, service):

    proc_cmd = ['systemd-cat', '-t', service]
    proc = subprocess.Popen(proc_cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out, err = proc.communicate(input=message)

    if proc.returncode != 0:
        return False

    return True
