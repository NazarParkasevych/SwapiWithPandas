import argparse
import logging
import json
from SWAPIClient import SWAPIClient
from SWAPIDataManager import SWAPIDataManager


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="SWAPI Data Manager CLI")
    parser.add_argument("--endpoint", required=True, help="Список сутностей через кому (наприклад, people,planets).")
    parser.add_argument("--output", required=True, help="Шлях до вихідного Excel-файлу.")
    parser.add_argument("--filters", help="JSON-рядок із фільтрами для кожної сутності.")

    args = parser.parse_args()

    # Ініціалізація клієнта та менеджера
    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)

    # Завантаження даних для вказаних сутностей
    endpoints = args.endpoint.split(',')
    for endpoint in endpoints:
        manager.fetch_entity(endpoint)

    # Застосування фільтрів, якщо вони є
    if args.filters:
        filters = json.loads(args.filters)
        for endpoint, columns in filters.items():
            manager.apply_filter(endpoint, columns)

    # Збереження у Excel
    manager.save_to_excel(args.output)
    logger.info(f"Дані успішно збережено у файл: {args.output}")


if __name__ == "__main__":
    main()
