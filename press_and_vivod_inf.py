#есть раскрыв деерва
#есть наведение на каждый элемент с прокруткой scrollbar
#осталось вывод информации с DataGrid
#вывод информации, затем объединение
import time

import pyautogui
from pywinauto.timings import Timings
from pywinauto import Application

app1 = Application(backend='uia').connect(title="Конфигуратор АБАК ПЛК")
windo = app1.window(title="Конфигуратор АБАК ПЛК")
tree = windo.child_window(control_type="DataGrid")
buttons = tree.descendants(control_type="Text")


def print_pretty_table(headers, data, column_width=25, columns=4):
    """
    Выводит данные в виде форматированной таблицы
    :param headers: список заголовков (должен соответствовать количеству столбцов)
    :param data: список данных (пустые значения пропускаются)
    :param column_width: максимальная ширина столбца
    :param columns: количество столбцов
    """
    # Фильтруем пустые значения
    filtered_data = [str(item) if item is not None and str(item).strip() else ""
                     for item in data]

    # Проверяем соответствие количества заголовков
    if len(headers) != columns:
        print(f"Ошибка: ожидается {columns} заголовков, получено {len(headers)}")
        return

    # Рассчитываем ширину столбцов
    col_width = min(column_width, max(len(str(item)) for item in headers + filtered_data) + 2)

    # Символы для рамки
    border = {
        'top': '┌' + '┬'.join(['─' * col_width for _ in range(columns)]) + '┐',
        'middle': '├' + '┼'.join(['─' * col_width for _ in range(columns)]) + '┤',
        'bottom': '└' + '┴'.join(['─' * col_width for _ in range(columns)]) + '┘',
        'vertical': '│'
    }

    # Функция форматирования ячейки
    def format_cell(text):
        text = str(text)
        if len(text) > col_width - 2:
            text = text[:col_width - 3] + '...'
        return f' {text.ljust(col_width - 2)} '

    # Вывод таблицы
    print(border['top'])

    # Заголовки
    header_row = border['vertical'] + border['vertical'].join(
        [format_cell(header) for header in headers]
    ) + border['vertical']
    print(header_row)
    print(border['middle'])

    # Данные
    for i in range(0, len(filtered_data), columns):
        row = filtered_data[i:i + columns]
        # Пропускаем полностью пустые строки
        if any(cell.strip() for cell in row):
            data_row = border['vertical'] + border['vertical'].join(
                [format_cell(cell) for cell in row]
            ) + border['vertical']
            print(data_row)

    print(border['bottom'])
    print(f"Выведено строк: {len([x for x in filtered_data if x.strip()]) // columns}")


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

for i in buttons:
    a = i.texts()
    if a  == "":
        pass
    else:
        print()
    print(i.texts())
    try:
        rectic(i)
    except:
        print("error")
