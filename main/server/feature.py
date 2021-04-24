import os
import sys
import socket
import winreg
import subprocess
from PIL import Image, ImageGrab
import wmi
from io import BytesIO
from server_connect import *

class ProcessRunning:
    def __init__(self, _sock, opcode):
        self.sock = _sock
        self.opcode = opcode
    
class AppRunning:
    pass
class ShutDown:
    '''
    Class which design and handle message for shutdown
        '''
    def __init__(self, _sock, timeout):
        self.timeout = timeout
    
    def do_task(self):
        platform = self.get_platform()
        if platform == 'Linux':
            # we cant shutdown a remotely linux machine without root access
            logging.debug('Linux platform')
            pass
        elif platform ==  'OS X':
            # the same thing to OS X machine
            logging.debug('OSX platform')
            pass 
        elif platform == 'Windows': 
            #self.command = 'Shutdown.exe -s -t ' + str(self.timeout)
            subprocess.Popen(['Shutdown.exe', '-s', '-t', self.timeout])
            logging.debug('Window platform')
            return '00' # Successful

    def get_platform(self):
        platforms = {
            'linux1' : 'Linux',
            'linux2' : 'Linux',
            'darwin' : 'OS X',
            'win32' : 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        return platforms[sys.platform]

class ShotScreen:
    def __init(self, _sock, opcode):
        self.opcode = opcode
        self.sock = _sock

    def do_work(self):
        if self.opcode == 'exit':
            return '01' # stop code
        elif self.opcode == 'take':
            img = ImageGrab.grab()

            img.save('screenshot.png', format='PNG')
            file = open('screnshot.png', 'rb')
            data = file.read(1024)
            while (data):
                self._sock.send(data)
                data = file.read(1024)
            self._sock.send(bytes('done', 'utf8'))
            file.close()
            return '00'  # Successful

class KeyStroke:
    pass 
class RegistryEdit:
    def __init__(self, sock, opcode):
        self.sock = sock
        self.opcode = opcode

    def base_registry(self, link):
        a = None
        if (link.index('\\') >= 0):
            base_str = link[0, link.index('\\')].upper()
            if base_str == 'HKEY_CLASSES_ROOT':
                a = winreg.HKEY_CLASSES_ROOT
            elif base_str == 'HKEY_CURRENT_USER':
                a = winreg.HKEY_CURRENT_USER
            elif base_str == 'HKEY_LOCAL_MACHINE':
                a = winreg.HKEY_LOCAL_MACHINE
            elif base_str == 'HKEY_USERS':
                a = winreg.HKEY_USERS
            elif base_str == 'HKEY_CURRENT_CONFIG':
                a = winreg.HKEY_CURRENT_CONFIG
        return a

    def get_value(self, a, link, valueName):
        a = winreg.OpenKey(self.base_registry(link), link.replace(self.base_registry(link), ''))
        if a == None:
            return 'Error'
        op = winreg.QueryValue(link, valueName)
        if op != None:
            s = ''
            if winreg.QueryValueEx(link, valueName)[1] == winreg.REG_MULTI_SZ:
                for i in range(0, len(op)):
                    s += op[i] + ' '
            else:
                if winreg.QueryValueEx(link, valueName)[1] == winreg.REG_BINARY:
                    for i in range(0, len(op)):
                        s += op[i] + ' '
                else:
                    s = str(op)
            return s
        else:
            return 'Error'

    def set_value(self, a, link, valueName, value, valueType):
        try:
            a = winreg.OpenKey(self.base_registry(link), link.replace(self.base_registry(link), ''))
        except:
            return 'Error'
        if (a == None):
            return 'Error'
        kind = winreg.REG_SZ
        if valueType == 'String':
            kind = winreg.REG_SZ
        elif valueType == 'Binary':
            kind = winreg.REG_BINARY
        elif valueType == 'DWORD':
            kind = winreg.REG_DWORD
        elif valueType == 'QWORD':
            kind = winreg.REG_QWORD
        elif valueType == 'Multi-String':
            kind = winreg.REG_MULTI_SZ
        elif valueType == 'Expandable String':
            kind = winreg.REG_EXPAND_SZ
        else:
            return 'Error'
        try:
            winreg.SetValue(link, valueName, kind, value)
        except:
            return 'Error'
        return 'Value set successfully'

    def delete_value(self, a, link, valueName):
        try:
            a = winreg.OpenKey(self.base_registry(link), link.replace(self.base_registry(link), ''))
        except:
            return 'Error'
        if a == None:
            return 'Error'
        test = False
        try:
            winreg.DeleteValue(a, valueName)
        except:
            return 'Error'
        else:
            return 'Value deleted successfully'

    def delete_key(self, a, link):
        try:
            winreg.DeleteKey(a, link.replace(self.base_registry(link), ''))
        except:
            return 'Error'
        else:
            return 'Value deleted successfully'

    def do_work(self):
        fs = open('fileReg.reg', 'x')
        fs.close()
        if self.opcode == 'exit':
            return '01' # exit

        elif self.opcode[2:6] == 'regf':  # open a registry file
            s = self.opcode[6:]
            fin = open('fileReg.reg', 'w')
            fin.write(s)
            fin.close()
            s = str(os.path.dirname(sys.executable)) + '\\fileReg.reg'
            isSuccess = True
            try:
                subprocess.run('regedit.exe /s \"' + s + '\"', timeout=20)
            except:
                isSuccess = False
            if isSuccess:
                print('Succeeded')
                return '00' # Successful
            else:
                print('Failed')
                return '02' # Failed

        elif self.opcode[2:6] == 'send':  # send multiple registry data
            opcode, option, link, valueName, value, valueType = self.opcode.split('~')

            a = self.base_registry(link)
            link2 = link[link.index('\\') + 1:]
            if a == None:
                s = 'Error'
            else:
                if option == 'CK':
                    a = winreg.CreateKey(a, link2)
                    s = 'Key successfully created'
                    return '00'
                elif option == 'Delete key':
                    s = self.delete_key(a, link2)
                    return '00'
                elif option == 'Get value':
                    s = self.get_value(a, link2, valueName)
                    return '00'
                elif option == 'Set value':
                    s = self.set_value(a, link2, valueName, value, valueType)
                    return '00'
                elif option == 'Delete value':
                    s = self.delete_value(a, link2, valueName)
                    return '00'
                else:
                    s = 'Error'
                    return '02'
            print(s)
