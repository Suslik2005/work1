import subprocess
import psutil
import pyautogui
from pywinauto import Application
import time
import win32gui
import win32con
from pywinauto.keyboard import send_keys
app_name = "Настройки сетевых интерфейсов"
app = Application(backend='win32').connect(title = app_name)
main_window = app.window(title = "Настройки сетевых интерфейсов")
main_window.print_control_identifiers()
time.sleep(2)
main_window.click_input()
time.sleep(2)
#button = main_window.child_window(class_name="TextBlock")
#button.click_input()