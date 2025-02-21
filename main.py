import argparse
from SWAPIClient import SWAPIClient
from ExcelSWAPIClient import ExcelSWAPIClient
from SWAPIDataManager import SWAPIDataManager
from PlanetsProcessor import PlanetsProcessor
from PeopleProcessor import PeopleProcessor
from FilmsProcessor import FilmsProcessor

# Ініціалізація парсера командного рядка
parser = argparse.ArgumentParser(description="SWAPI Data Manager")
parser.add_argument('--input', required=True, help="URL або шлях до .xlsx файлу")
parser.add_argument('--endpoints', required=True, help="Список сутностей через кому (наприклад, people,planets,films)")
parser.add_argument('--output', required=True, help="Ім'я вихідного Excel-файлу")
args = parser.parse_args()

# Вибір клієнта в залежності від вхідного параметра
if args.input.startswith("http"):
    client = SWAPIClient(base_url=args.input)
else:
    client = ExcelSWAPIClient(file_path=args.input)

# Ініціалізація менеджера даних
manager = SWAPIDataManager(client)

# Реєстрація процесорів для обробки сутностей
manager.register_processor("people", PeopleProcessor())
manager.register_processor("planets", PlanetsProcessor())
manager.register_processor("films", FilmsProcessor())

# Завантаження даних для кожної сутності
for endpoint in args.endpoints.split(','):
    manager.fetch_entity(endpoint)

# Збереження даних у файл Excel
manager.save_to_excel(args.output)
print(f"Дані успішно збережено у файл {args.output}")
