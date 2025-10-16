from pywinauto import Application
from collections import defaultdict
import time


class TreeViewExplorer:
    def __init__(self, app_title):
        self.app = Application(backend="uia").connect(title=app_title)
        self.tree = self.app.window(title=app_title).TreeView
        self.leaf_paths = []  # Хранит все пути к конечным элементам
        self.node_paths = defaultdict(list)
        self.text = self.tree.descendants(control_type="Text")
        self.c = 0
        print(self.text)

    def scan_tree(self):
        """Полное сканирование дерева с построением всех путей"""
        self.leaf_paths = []
        self.node_paths = defaultdict(list)
        self._scan_node(self.tree, [])

    def _scan_node(self, node, current_path):
        """Рекурсивный обход дерева"""
        for child in node.children():
            try:
                child_text = self.text[self.c]
                new_path = current_path + [child_text]

                # Запоминаем путь для этого элемента
                self.node_paths[child_text].append(new_path)

                # Проверяем, является ли элемент конечным
                is_leaf = not child.children()

                if is_leaf:
                    self.leaf_paths.append(new_path)
                else:
                    # Раскрываем, если нужно
                    if hasattr(child, 'is_expanded') and not child.is_expanded():
                        child.expand()
                        time.sleep(0.3)  # Ждем обновления UI

                    # Рекурсивный обход детей
                    self._scan_node(child, new_path)

            except Exception as e:
                print(f"Ошибка при сканировании: {e}")
                continue
            self.c+=1
            print(self.leaf_paths)

    def get_all_leaf_paths(self):
        """Возвращает все пути к конечным элементам"""
        return self.leaf_paths

    def find_paths_by_pattern(self, pattern):
        """Находит пути к элементам, содержащим указанный текст"""
        return [path for text, paths in self.node_paths.items()
                if pattern.lower() in text.lower()
                for path in paths]


# Пример использования
if __name__ == "__main__":
    # Инициализация
    explorer = TreeViewExplorer("Конфигуратор АБАК ПЛК")

    # Сканирование дерева
    print("Сканируем структуру дерева...")
    explorer.scan_tree()

    # Получаем все конечные элементы
    all_leaves = explorer.get_all_leaf_paths()
    print(f"\nНайдено конечных элементов: {len(all_leaves)}")

    # Выводим первые 5 путей для примера
    print("\nПримеры путей к конечным элементам:")
    for path in all_leaves[:5]:
        print(" → ".join(str(path)))