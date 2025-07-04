import subprocess
import psutil
from pywinauto import Application
import time

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

element = main_window.child_window(auto_id = "Button4")
element[0].click_input()
#app = Application(backend="uia").connect(title="Конфигуратор АБАК ПЛК")
#
#main_window = app.window(title="Конфигуратор АБАК ПЛК")
#main_window.child_window(title="", control_type = "Button").click_input()