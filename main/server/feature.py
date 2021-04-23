import subprocess 
import logging 
import sys

class ProcessRunning:
    pass 
class AppRunning:
    pass
class ShutDown:
    '''
    Class which design and handle message for shutdown
        '''
    def __init__(self, timeout):
        self.timeout = timeout
    
    def do_task(self):
        platform = self.get_platform()
        if platform == 'Linux':
            # we cant shutdown a remotely linux machine without root access
            logging.debug('Linux platform')
            pass
        elif platform ==  'OS X':
            # the same thing to Linux machine
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
    pass 
class KeyStroke:
    pass 
class RegistryEdit:
    pass