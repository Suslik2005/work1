import time

import pyautogui

from pywinauto import Application


dict_raspoloveniye = dict()

mass_iz_ctrl_type = ['DataItem', 'DataGrid']

app1 = Application(backend='uia').connect(title = "Конфигуратор АБАК ПЛК")
windo1 = app1.window(title = "Конфигуратор АБАК ПЛК")
#windo1.print_control_identifiers()
boxes = set()
clickable = set()

for i in mass_iz_ctrl_type:
    try:
        j = windo1.child_window(control_type=i)
        rect = j.rectangle()
        print(rect)
        center_x = (rect.left + rect.right) // 2
        center_y = (rect.top + rect.bottom) // 2
        if center_y == 0 and center_x == 0:
            print("error")
        else:
            boxes.add(i)
            print(center_x, center_y)
            # Наведение курсора
            pyautogui.moveTo(center_x, center_y)
            time.sleep(2)
            print("кнопка " + str(i) + " нажата")

    except:
        clickable.add(i)
        print("error")




print(boxes)
print(clickable)


for box in boxes:
    box_connection = windo1.child_window(control_type=box)
    box_connection.click_input()
    print("проверка боксов " + box)
    for buut in clickable:
        buttes = box_connection.descendants(control_type=buut)
        print("проверка бокса " + box + " кнопок вида: " + buut)
        for butt in buttes:
            try:
                rect = butt.rectangle()  # (left, top, right, bottom)
                center_x = (rect.left + rect.right) // 2
                center_y = (rect.top + rect.bottom) // 2
                if center_y == 0 and center_x == 0:
                    print("error")
                    break
                else:
                    print(center_x, center_y)
                    # Наведение курсора
                    pyautogui.moveTo(center_x, center_y)
                    time.sleep(1)
                print("все ок, кнопка вида " + buut + " работает")
                if box not in dict_raspoloveniye:
                    dict_raspoloveniye[box] = set()
                    dict_raspoloveniye[box].add(buut)
                else:
                    dict_raspoloveniye[box].add(buut)

            except:
                print("ERROR")
                break
print(dict_raspoloveniye)
