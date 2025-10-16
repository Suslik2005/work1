import time

import win32api
import win32con
from pywinauto import mouse
import pyautogui
from pywinauto.timings import Timings
from pywinauto import Application

app1 = Application(backend='uia').connect(title="Конфигуратор АБАК ПЛК")
windo = app1.window(title="Конфигуратор АБАК ПЛК")
tree = windo.child_window(control_type="Tree")
buttons = tree.descendants(control_type="Text")


def rectic(element):
    #указатель
    #указывает мышкой на нужный элемент, без нажатия на него
    #нужен для испытания кода
    rect = element.rectangle()  # (left, top, right, bottom)
    center_x = (rect.left + rect.right) // 2
    center_y = (rect.top + rect.bottom) // 2
    if center_y == 0 and center_x == 0:
        print("eRRor")
    else:
        print(center_x, center_y)
        # Наведение курсора
        pyautogui.moveTo(center_x, center_y)
        time.sleep(1)


def check_element_visibility(tree, element):
    """
    Проверяет, виден ли элемент в TreeView.
    Возвращает:
        - "visible" (элемент в зоне видимости),
        - "up" (элемент выше видимой области),
        - "down" (элемент ниже видимой области).
    """
    # Получаем координаты элемента
    try:
        elem_rect = element.rectangle()
    except:
        return "down"  # Если не удалось получить координаты, предполагаем, что элемент ниже

    # Получаем координаты видимой области TreeView
    tree_rect = tree.rectangle()

    # Проверяем положение элемента относительно TreeView
    if elem_rect.bottom < tree_rect.top+5:
        return "up"  # Элемент выше видимой области
    elif elem_rect.top > tree_rect.bottom-5:
        return "down"  # Элемент ниже видимой области
    else:
        return "visible"  # Элемент виден


def scroll_to_visible_with_wheel(element, tree):
    direction = check_element_visibility(tree, element)
    if direction == "down":
        while check_element_visibility(tree, element) != "visible":
            print(check_element_visibility(tree, element))
            tree.scroll("down", "page", count=1)
            print("down+1")
            if check_element_visibility(tree, element) != 'down':
                break

    else:
        while check_element_visibility(tree, element) != "visible":
            tree.scroll("up", "page", count=1)
            print("up+1")
            if check_element_visibility(tree, element) != 'up':
                break
    return True



for i in buttons:
    print(i.texts())
    element_status = check_element_visibility(tree, i)
    print(element_status)
    if element_status != "visible":
        scroll_to_visible_with_wheel(i, tree)
    time.sleep(2)

    try:
        rectic(i)
    except:
        print("error")
