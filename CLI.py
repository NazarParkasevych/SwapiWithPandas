import argparse
import logging

from SWAPIClient import SWAPIClient
from SWAPIDataManager import SWAPIDataManager


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="SWAPI Data Manager CLI")
    parser.add_argument("--fetch", nargs='+', help="Сутності для отримання даних (наприклад, 'people', 'planets')")
    parser.add_argument("--filter", nargs=2, action='append', help="Фільтрувати сутність: назва_сутності стовпці_для_видалення")
    parser.add_argument("--save", help="Шлях до Excel файлу для збереження даних")

    args = parser.parse_args()

    # Ініціалізація клієнта та менеджера
    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)

    # Отримання даних
    if args.fetch:
        for endpoint in args.fetch:
            manager.fetch_entity(endpoint)

    # Застосування фільтрів
    if args.filter:
        for endpoint, columns in args.filter:
            columns_to_drop = columns.split(',')
            manager.apply_filter(endpoint, columns_to_drop)

    # Збереження в Excel
    if args.save:
        manager.save_to_excel(args.save)
        logger.info(f"Дані успішно збережено у файл: {args.save}")


if __name__ == "__main__":
    main()
