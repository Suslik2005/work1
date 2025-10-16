from pywinauto import Application
from pywinauto.timings import Timings
import time
from collections import deque

# Настройка временных параметров
Timings.window_find_timeout = 10
Timings.after_clickinput_wait = 0.5


class TreeViewAnalyzer:
    def __init__(self, app_title):
        self.app = Application(backend="uia").connect(title=app_title)
        self.tree = self.app.window(title=app_title).TreeView
        self.all_paths = []

    def _get_element_text(self, element):
        """Безопасное получение текста элемента"""
        try:
            # Пробуем разные методы по порядку
            if element.texts() and isinstance(element.texts()[0], str):
                return element.texts()[0]
            if hasattr(element, 'window_text'):
                text = element.window_text()
                if text.strip(): return text
            if hasattr(element, 'name'):
                return element.name
            return "Без названия"
        except Exception:
            return "Без названия"

    def analyze_tree(self):
        """Итеративный обход дерева с построением путей"""
        self.all_paths = []
        stack = deque()

        # Инициализация стека (элемент, путь, уровень)
        for child in self.tree.children():
            stack.append((child, [], 0))

        while stack:
            element, current_path, level = stack.pop()

            try:
                # Получаем текст элемента
                element_text = self._get_element_text(element)
                new_path = current_path + [element_text]

                # Сохраняем текущий путь
                self.all_paths.append(new_path)

                # Раскрываем элемент, если нужно
                if hasattr(element, 'is_expanded') and not element.is_expanded():
                    try:
                        element.expand()
                        time.sleep(0.3)
                    except:
                        # Альтернативные методы раскрытия
                        expand_btn = element.child_window(auto_id="Expander", control_type="Button")
                        if expand_btn.exists():
                            expand_btn.click()
                            time.sleep(0.3)

                # Добавляем детей в стек (в обратном порядке для правильного обхода)
                children = element.children()
                for child in reversed(children):
                    stack.append((child, new_path, level + 1))

            except Exception as e:
                print(f"Ошибка при обработке элемента: {str(e)}")
                continue

    def get_all_paths(self):
        """Возвращает все пути в дереве"""
        return self.all_paths

    def find_paths_by_pattern(self, pattern):
        """Находит пути, содержащие указанный текст"""
        return [path for path in self.all_paths
                if any(pattern.lower() in str(item).lower() for item in path)]

    def print_leaf_paths(self):
        """Печатает только пути к конечным элементам"""
        leaf_paths = []
        all_paths_str = [" → ".join(path) for path in self.all_paths]

        for path_str in all_paths_str:
            is_leaf = not any(
                other != path_str and other.startswith(path_str + " → ")
                for other in all_paths_str
            )
            if is_leaf:
                leaf_paths.append(path_str)

        print("\nКонечные элементы:")
        for path in leaf_paths[:20]:  # Выводим первые 20 для примера
            print(path)


# Пример использования
if __name__ == "__main__":
    analyzer = TreeViewAnalyzer("Конфигуратор АБАК ПЛК")

    print("Начинаем анализ TreeView...")
    analyzer.analyze_tree()

    print("\nВсего найдено путей:", len(analyzer.get_all_paths()))

    # Поиск специфических элементов
    print("\nПоиск элементов 'CParamsGroup':")
    for path in analyzer.find_paths_by_pattern("CParamsGroup")[:10]:
        print(" → ".join(path))

    # Вывод конечных элементов
    analyzer.print_leaf_paths()