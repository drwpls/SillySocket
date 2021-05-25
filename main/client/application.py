from process import *


FEATURE_CODE = {
    'PING': '00',
    'ProcessRunning': '01',
    'AppRunning': '02',
    'Shutdown': '03',
    'Screenshot': '04',
    'Keystroke': '05',
    'RegistryEdit': '06',
}


class Application_Dialog(Process_Dialog):
    def __init__(self, sock):
        super().__init__(sock)
        self.FEATURE_CODE = FEATURE_CODE['AppRunning']
        self.setWindowTitle('Application')

    def get_process_list(self):
        self.list_process_data = []
        self.list_process_data_backup = []
        message = self.FEATURE_CODE + 'get__'
        self.sock.sendall(message.encode('utf-8'))
        self.list_process_data = self.receive_list()
