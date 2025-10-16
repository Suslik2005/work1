from collections import defaultdict

from pywinauto import Application


def find_all_control_types(app_title, output_file):
    """
    Находит все существующие control_type в окне приложения и сохраняет в файл

    :param app_title: Заголовок окна приложения
    :param output_file: Путь к выходному файлу
    """
    try:
        # Подключаемся к приложению (пробуем оба бэкенда)
        for backend in ['uia', 'win32']:
            try:
                app = Application(backend=backend).connect(title=app_title)
                break
            except:
                continue
        else:
            raise Exception(f"Не удалось подключиться к приложению '{app_title}'")

        window = app.window(title=app_title)

        # Получаем все элементы
        all_elements = window.descendants()

        # Собираем статистику по типам элементов
        type_stats = defaultdict(list)
        tochto = set()
        for elem in all_elements:
            try:
                ctrl_type = elem.element_info.control_type
                type_stats[ctrl_type].append(elem)
                tochto.add(ctrl_type)

            except:
                continue
        print(tochto)
        # Сохраняем результаты
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Все control_type в окне '{app_title}':\n")
            f.write(f"Всего найдено типов: {len(type_stats)}\n")
            f.write(f"Всего элементов: {len(all_elements)}\n\n")

            for i, (ctrl_type, elements) in enumerate(type_stats.items(), 1):
                f.write(f"{i}. {ctrl_type} (найдено: {len(elements)})\n")

                # Примеры элементов для каждого типа
                for j, elem in enumerate(elements[:3], 1):  # Выводим первые 3 элемента каждого типа
                    try:
                        name = elem.window_text() or "N/A"
                    except:
                        name = "N/A"

                    f.write(f"   Пример {j}: {name}")
                    try:
                        f.write(f" | AutomationId: {elem.automation_id()}")
                    except:
                        pass
                    try:
                        f.write(f" | Координаты: {elem.rectangle()}\n")
                    except:
                        f.write("\n")

                if len(elements) > 3:
                    f.write(f"   ... и еще {len(elements) - 3} элементов\n")
                f.write("\n")

        print(f"Результаты сохранены в: {output_file}")
        return True

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False


# Пример использования
if __name__ == "__main__":
    # Настройки
    APP_TITLE = "Конфигуратор АБАК ПЛК"  # Замените на ваш заголовок окна
    OUTPUT_FILE = "all_control_types.txt"

    # Запуск поиска
    success = find_all_control_types(APP_TITLE, OUTPUT_FILE)

    if success:
        print(f"\nОткройте файл {OUTPUT_FILE} для просмотра всех типов элементов")
        print("Формат файла:")
        print("1. Button (найдено: 5)")
        print("   Пример 1: OK | AutomationId: btnOK | Координаты: (100, 200, 150, 220)")
        print("   Пример 2: Cancel | AutomationId: btnCancel | Координаты: (160, 200, 210, 220)")
        print("   ... и еще 3 элементов\n")
    else:
        print("\nНе удалось выполнить поиск элементов")