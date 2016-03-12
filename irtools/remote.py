from collections import namedtuple

RemoteKey = namedtuple('RemoteKey', ['code', 'key_name'])

class Remote(object):
    def __init__(self, remote_name, key_list):
        self.remote_name = remote_name
        self.key_list = key_list

    def key_press(self, key):
        pass
