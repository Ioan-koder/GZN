import json
import os
from datetime import datetime

# Класс для управления земельными участками
class LandInspector:
    def __init__(self, data_file="land_data.json"):
        self.data_file = data_file
        self.land_plots = self.load_data()

    def load_data(self):
        """Загружает данные из JSON-файла."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self):
        """Сохраняет данные в JSON-файл."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.land_plots, f, ensure_ascii=False, indent=4)

    def add_plot(self, cadastral_number, area, category, permitted_use):
        """Добавляет новый участок."""
        plot = {
            'cadastral_number': cadastral_number,
            'area': area,
            'category': category,
            'permitted_use': permitted_use,
            'actual_use': None,
            'violations': []
        }
        self.land_plots.append(plot)
        self.save_data()
        print(f"Участок {cadastral_number} добавлен.")

    def update_actual_use(self, cadastral_number, actual_use):
        """Обновляет фактическое использование участка."""
        for plot in self.land_plots:
            if plot['cadastral_number'] == cadastral_number:
                plot['actual_use'] = actual_use
                self.check_violations(plot)
                self.save_data()
                print(f"Фактическое использование для участка {cadastral_number} обновлено.")
                return
        print(f"Участок с номером {cadastral_number} не найден.")

    def check_violations(self, plot):
        """Проверяет нарушения в использовании земли."""
        plot['violations'] = []
        if plot['actual_use'] and plot['actual_use'] != plot['permitted_use']:
            violation = f"Несоответствие использования: разрешено '{plot['permitted_use']}', фактически '{plot['actual_use']}'"
            plot['violations'].append(violation)

    def generate_report(self, output_file="land_report.txt"):
        """Генерирует отчет о нарушениях."""
        report = f"Отчет по земельным участкам ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n"
        violations_found = False

        for plot in self.land_plots:
            report += f"Кадастровый номер: {plot['cadastral_number']}\n"
            report += f"Площадь: {plot['area']} га\n"
            report += f"Категория: {plot['category']}\n"
            report += f"Разрешенное использование: {plot['permitted_use']}\n"
            report += f"Фактическое использование: {plot['actual_use'] or 'Не указано'}\n"
            if plot['violations']:
                violations_found = True
                report += "Нарушения:\n"
                for violation in plot['violations']:
                    report += f"- {violation}\n"
            else:
                report += "Нарушений не выявлено.\n"
            report += "-" * 50 + "\n"

        if not violations_found:
            report += "\nНарушений по всем участкам не выявлено.\n"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Отчет сохранен в файл {output_file}")

def main():
    inspector = LandInspector()
    while True:
        print("\nМеню:")
        print("1. Добавить участок")
        print("2. Обновить фактическое использование")
        print("3. Сгенерировать отчет")
        print("4. Выход")
        choice = input("Выберите действие (1-4): ")

        if choice == '1':
            cadastral_number = input("Введите кадастровый номер: ")
            area = float(input("Введите площадь (га): "))
            category = input("Введите категорию земли (например, сельхозназначения): ")
            permitted_use = input("Введите разрешенное использование: ")
            inspector.add_plot(cadastral_number, area, category, permitted_use)

        elif choice == '2':
            cadastral_number = input("Введите кадастровый номер: ")
            actual_use = input("Введите фактическое использование: ")
            inspector.update_actual_use(cadastral_number, actual_use)

        elif choice == '3':
            inspector.generate_report()

        elif choice == '4':
            print("Программа завершена.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()