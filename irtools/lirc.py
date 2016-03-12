import socket
from periodicpy.irtools.remote import RemoteKey

class LircCommunicationError(Exception):
    pass

class LircCommandError(Exception):
    pass

LIRC_COMMANDS = ['VERSION', 'SEND_ONCE', 'SEND_START', 'SEND_STOP', 'LIST',
                 'SET_INPUTLOG', 'DRV_OPTION', 'SIMULATE', 'SET_TRANSMITTERS']

class LircClient(object):
    def __init__(self, address):
        self.srv_addr = address

        #self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def _sock_recv_line(self):
        data = ''
        block_counter = 0
        done = False
        while done == False:
            if block_counter > 10000:
                raise LircCommunicationError('malformed response')

            recv_char = self.sock.recv(1)

            if recv_char == '\n':
                done = True
            else:
                data += recv_char

            block_counter += 1

        return data

    def _receive_lirc_packet(self, has_data=False):

        #socket must be open!
        #receive BEGIN
        if self._sock_recv_line() != 'BEGIN':
            raise LircCommunicationError('malformed response')

        #receive command
        if self._sock_recv_line() not in LIRC_COMMANDS:
            #raise LircCommunicationError('malformed response')
            pass

        #receive status
        status = self._sock_recv_line()
        if status == 'ERROR':
            raise LircCommandError('command failed')
        elif status != 'SUCCESS':
            raise LircCommunicationError('malformed response')

        #expect end if no data
        if has_data == False:
            if self._sock_recv_line() != 'END':
                raise LircCommandError('malformed response')
            return None

        #get data
        if self._sock_recv_line() != 'DATA':
            raise LircCommunicationError('malformed response')

        data_count = int(self._sock_recv_line())
        data_lines = []
        while data_count > 0:

            data_lines.append(self._sock_recv_line())
            data_count -= 1

        if self._sock_recv_line() != 'END':
            raise LircCommunicationError('malformed response')

        return data_lines

    def _send_command(self, command, has_response=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.srv_addr, 6000))
        self.sock.send(command+'\n')

        response = self._receive_lirc_packet(has_response)
        self.sock.close()

        return response

    def get_lircd_version(self):
        return self._send_command('VERSION', True)[0]

    def get_remote_list(self):
        return self._send_command('LIST', True)

    def get_remote_key_list(self, remote):
        key_list = self._send_command(' '.join(['LIST', remote]), True)
        return [RemoteKey(code=int(x.split(' ')[0], 16),
                          key_name=x.split(' ')[1]) for x in key_list]

    def send_key_once(self, remote, key_name):
        self._send_command(' '.join(['SEND_ONCE', remote, key_name]))

    def start_send_key(self, remote, key_name, repeat_count=0):
        self._send_command(' '.join(['SEND_START', remote, key_name, repeat_count]))

    def stop_send_key(self, remote, key_name):
        self._send_command(' '.join(['SEND_STOP', remote, key_name]))
