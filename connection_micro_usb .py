import subprocess
import psutil
import pyautogui
from pywinauto import Application
import time
import win32gui
import win32con
from pywinauto.keyboard import send_keys

pn = "AbakConfigurator.exe"
def is_process_running(name_process):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == name_process:
            return True
    return False

app_name = "Конфигуратор АБАК ПЛК"
def maximize_app_window(app_name):
    try:
        app = Application(backend='uia').connect(title = app_name)
        window = app.window(title = app_name)
        window.restore()
        window.set_focus()
        window.maximize()
    except Exception as e:
        print(f"Ошибка:  {e}")

if not is_process_running(pn):
    config_path = r"C:\Program Files (x86)\ABAK PLC Configurator\AbakConfigurator"
    subprocess.Popen(config_path)
    time.sleep(3)

maximize_app_window(app_name)

app = Application(backend='uia').connect(title = app_name)
main_window = app.window(title = app_name)

main_window.print_control_identifiers()

time.sleep(2)

#toolbar = main_window.child_window(auto_id = "toolBar1", control_type = "Button")
#toolbar.click_input()
toolbar = main_window.child_window(control_type="ToolBar")
buttons = toolbar.descendants(control_type="Image")

#for btn in range(len(buttons)):
#    print(btn)
buttons[0].click_input()
    #if btn.is_enabled():  # Проверяем, активна ли кнопка
    #    btn.click_input()
    #    break
time.sleep(2)

hwnd = win32gui.FindWindow(None, "Логин")
if hwnd:
    win32gui.SetForegroundWindow(hwnd)
    send_keys("root")
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_TAB, 0)
    send_keys("Zer0Day!")
    pyautogui.press('enter')
time.sleep(3)
app1 = Application(backend='win32').connect(title = "Условия использования")
windo1 = app1.window(title = "Условия использования")
windo1.print_control_identifiers()
windo1.restore()
windo1.set_focus()
windo1.maximize()

hwnd = win32gui.FindWindow(None, "Условия использования")
if hwnd:
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_TAB, 0)
    pyautogui.press('enter')
#for i in butt:
#    i.click_input()
#    time.sleep(2)
#    print("кнопка " + str(i) + " нажата")