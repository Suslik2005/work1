import time
from datetime import datetime
from pywinauto import Application


class imcomconiglib:
    class Tree:
        def __init__(self):
            self.app_name = "Конфигуратор АБАК ПЛК"
            self.app = Application(backend='uia').connect(title=self.app_name)
            self.main_window = self.app.window(title=self.app_name)
            self.tree = self.main_window.child_window(control_type="Tree")
            self.buttons = self.tree.descendants(control_type="Button")
            self.treeitems = self.tree.descendants(control_type="TreeItem")

        def datatime(self):
            if self.buttons[0].get_toggle_state():
                self.buttons[0].click_input()
            time.sleep(1)
            self.buttons[1].click_input()
            time.sleep(1)
            self.buttons[4].click_input()
            time.sleep(1)
            self.treeitems[10].click_input()
