from pywinauto import Application

app = Application(backend="uia").connect(title="Конфигуратор АБАК ПЛК")
tree = app.window(title="Конфигуратор АБАК ПЛК").TreeView

tree.dump_tree()
# Находим нужные элементы
params_group = tree.child_window(
    title="AbakConfigurator.CParamsGroup",
    control_type="TreeItem",
    found_index=0  # Берём первый из найденных элементов
)
modules_list = tree.child_window(title="AbakConfigurator.CModulesList", control_type="TreeItem")

# Раскрываем элементы (если ещё не раскрыты)
if not params_group.is_expanded():
    params_group.expand()

if not modules_list.is_expanded():
    modules_list.expand()

# Получаем и выводим дочерние элементы
print("Содержимое AbakConfigurator.CParamsGroup:")
for child in params_group.children():
    print(f" - {child.texts()[0]}")

print("\nСодержимое AbakConfigurator.CModulesList:")
for child in modules_list.children():
    print(f" - {child.texts()[0]}")