import pandas as pd
import logging


class SWAPIDataManager:
    """
    Менеджер даних для роботи з SWAPI.
    """

    def __init__(self, client):
        self.client = client
        self.data = {}
        self.processors = {}  # Словник для зберігання процесорів
        self.logger = logging.getLogger(__name__)

    def register_processor(self, entity_type: str, processor):
        """
        Реєструє процесор для обробки конкретного типу сутності.

        Аргументи:
            entity_type (str): Тип сутності (наприклад, 'people').
            processor: Процесор для обробки даних цієї сутності.
        """
        self.processors[entity_type] = processor
        self.logger.info(f"Процесор для '{entity_type}' зареєстровано.")

    def fetch_entity(self, endpoint: str):
        """
        Завантажує сутність з API та перетворює її у DataFrame.
        """
        self.logger.info(f"Отримання даних для сутності: {endpoint}")
        json_data = self.client.fetch_json(endpoint)
        df = pd.DataFrame(json_data)

        # Якщо є зареєстрований процесор для цього типу сутності — застосувати його
        if endpoint in self.processors:
            processor = self.processors[endpoint]
            df = processor.process(df)

        self.data[endpoint] = df

    def apply_filter(self, endpoint: str, columns_to_drop: list):
        """
        Видаляє зазначені стовпці з DataFrame.
        """
        if endpoint in self.data:
            self.logger.info(f"Застосування фільтру для: {endpoint}")
            self.data[endpoint].drop(columns=columns_to_drop, inplace=True, errors='ignore')
        else:
            self.logger.warning(f"Сутність '{endpoint}' не завантажена!")

    def save_to_excel(self, filename: str):
        """
        Зберігає всі зібрані дані у файл Excel.
        """
        self.logger.info(f"Запис даних у Excel файл: {filename}")
        if not self.data:
            self.logger.warning("Немає даних для збереження!")
            return

        with pd.ExcelWriter(filename) as writer:
            for endpoint, dataframe in self.data.items():
                if not dataframe.empty:
                    dataframe.to_excel(writer, sheet_name=endpoint.capitalize(), index=False)
                else:
                    self.logger.warning(f"Сутність '{endpoint}' пуста та не буде записана!")
