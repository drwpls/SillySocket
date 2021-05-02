# https://docs.microsoft.com/ru-ru/windows/win32/api/winuser/nf-winuser-getancestor
import win32gui
import win32api
import win32con
import ctypes
# For test only:
from subprocess import Popen
from time import sleep
GetAncestor = ctypes.windll.user32.GetAncestor
# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowthreadprocessid
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId

def _get_top_level(hwnd:int, lst:list):
    root_win = GetAncestor(hwnd, win32con.GA_ROOTOWNER)
    # Exclude non top level windows:
    if root_win == win32con.NULL: return
    # Exclude invisible windows:
    if not win32gui.IsWindowVisible(root_win): return
    # Exclude windows outside of screen (questionable!):
    if any( [c < 0 for c in win32gui.GetWindowRect(root_win)] ): return
    # Exclude windows with empty titles (questionable!):
    if ( title := win32gui.GetWindowText(root_win) ):
        lst.append((root_win, title))

def get_pid_window(pid:int):
    # List item: (hwnd, 'title'):
    win_lst = []
    # Get a list of all top level windows and its titles:
    win32gui.EnumWindows(_get_top_level, win_lst)
    # Print all found windows:
    print(*win_lst, sep='\n')
    cur_pid = ctypes.c_int()
    for hwnd, title in win_lst:
        GetWindowThreadProcessId(hwnd, ctypes.byref(cur_pid))
        if cur_pid.value == pid: return title

# Let's test on the Calc:
pid = Popen('calc.exe').pid
# Give some time for initialization:
sleep(1)
print(f'Found ({pid}): {get_pid_window(pid)}')