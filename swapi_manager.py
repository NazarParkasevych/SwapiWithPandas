import argparse
import os
import pandas as pd
import requests
from logger_config import logger

class OfflineSWAPIManager:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = {}

    def load_from_excel(self):
        """Завантаження даних з локального файлу Excel."""
        if os.path.exists(self.input_file):
            logger.info(f"Завантаження даних із {self.input_file}")
            self.data = pd.read_excel(self.input_file, sheet_name=None)
        else:
            logger.error(f"Файл {self.input_file} не знайдено! Перевірте шлях.")

    def save_to_excel(self, output_file):
        """Збереження даних у Excel."""
        if not self.data:
            logger.warning("Немає даних для збереження.")
            return

        with pd.ExcelWriter(output_file) as writer:
            for sheet, df in self.data.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
        logger.info(f"Дані успішно збережено у {output_file}")

    def fetch_online_data(self, endpoint):
        """Спроба отримати дані онлайн, якщо є підключення."""
        url = f"https://swapi.dev/api/{endpoint}/"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json().get('results', [])
            self.data[endpoint] = pd.DataFrame(data)
            logger.info(f"Отримано {len(data)} записів для {endpoint}")
        except requests.exceptions.RequestException:
            logger.warning(f"Не вдалося отримати {endpoint}. Використовуємо локальні дані.")

    def process_data(self, endpoints):
        """Обробка даних: отримання онлайн або використання локальних даних."""
        for endpoint in endpoints:
            if endpoint in self.data:
                logger.info(f"Використовуємо кешовані дані для {endpoint}")
            else:
                self.fetch_online_data(endpoint)

# Парсинг аргументів командного рядка
parser = argparse.ArgumentParser(description="SWAPI Manager Offline Mode")
parser.add_argument("--input", required=True, help="Файл вхідних даних (Excel)")
parser.add_argument("--endpoint", required=True, help="Список сутностей через кому (people, planets, etc.)")
parser.add_argument("--output", required=True, help="Файл для збереження результату (Excel)")
args = parser.parse_args()

# Запуск менеджера
manager = OfflineSWAPIManager(args.input)
manager.load_from_excel()
manager.process_data(args.endpoint.split(","))
manager.save_to_excel(args.output)
