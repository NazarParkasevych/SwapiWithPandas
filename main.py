import logging
import json
from SWAPIClient import SWAPIClient
from SWAPIDataManager import SWAPIDataManager
from PeopleProcessor import PeopleProcessor
from PlanetsProcessor import PlanetsProcessor
from FilmsProcessor import FilmsProcessor

def main():
    """
    Основний вхідний пункт програми.
    """
    # Налаштування логування
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    # Статичні параметри
    endpoint = "people,planets,films"  # Список сутностей через кому
    output = "swapi_data.xlsx"  # Шлях до вихідного файлу
    filters = '{"people": ["films", "species"], "planets": ["films", "residents"]}'  # JSON із фільтрами

    # Логування параметрів
    logger.info(f"Сутності: {endpoint}")
    logger.info(f"Файл для збереження: {output}")
    logger.info(f"Фільтри: {filters}")

    # Ініціалізація SWAPIClient та SWAPIDataManager
    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)

    # Реєстрація процесорів
    manager.register_processor("people", PeopleProcessor())
    manager.register_processor("planets", PlanetsProcessor())
    manager.register_processor("films", FilmsProcessor())

    # Завантаження даних
    logger.info("Завантаження даних...")
    endpoints = endpoint.split(',')
    for ep in endpoints:
        manager.fetch_entity(ep)

    # Застосування фільтрів
    if filters:
        try:
            filter_dict = json.loads(filters)
            for ep, columns in filter_dict.items():
                manager.apply_filter(ep, columns)
        except json.JSONDecodeError:
            logger.error("Помилка: Неправильний формат фільтрів. Використовуйте валідний JSON.")
            return

    # Збереження у Excel
    logger.info(f"Збереження даних у файл: {output}")
    manager.save_to_excel(output)
    logger.info("Процес завершено успішно!")


if __name__ == "__main__":
    main()
