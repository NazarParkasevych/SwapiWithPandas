from abc import ABC, abstractmethod
import pandas as pd
from SWAPIClient import SWAPIClient
from logger_config import logger


# Визначення інтерфейсів
class DataFetcher(ABC):
    @abstractmethod
    def fetch_entity(self, endpoint: str):
        """Отримує сутність із вказаного джерела."""


class DataProcessor(ABC):
    @abstractmethod
    def apply_filter(self, endpoint: str, columns_to_drop: list):
        """Фільтрує дані, видаляючи непотрібні стовпці."""

    @abstractmethod
    def register_processor(self, entity: str, processor):
        """Реєструє процесор для обробки певної сутності."""


class DataSaver(ABC):
    @abstractmethod
    def save_to_excel(self, filename: str):
        """Зберігає дані у файл Excel."""


# Реалізація SWAPIDataManager через ці інтерфейси
class SWAPIDataManager(DataFetcher, DataProcessor, DataSaver):
    def __init__(self, client: SWAPIClient):
        self.client = client
        self.data = {}
        self.processors = {}

    def fetch_entity(self, endpoint: str):
        raw_data = self.client.fetch_json(endpoint)
        self.data[endpoint] = pd.DataFrame(raw_data)
        logger.info(f"Fetched {len(raw_data)} records for {endpoint}")

    def register_processor(self, entity, processor):
        self.processors[entity] = processor

    def apply_filter(self, endpoint: str, columns_to_drop: list):
        if endpoint in self.data:
            self.data[endpoint] = self.data[endpoint].drop(columns=columns_to_drop, errors='ignore')
            logger.info(f"Applied filter for {endpoint}, dropped columns: {columns_to_drop}")
        else:
            logger.warning(f"Data for {endpoint} not found.")

    def save_to_excel(self, filename: str):
        with pd.ExcelWriter(filename) as writer:
            for endpoint, df in self.data.items():
                df.to_excel(writer, sheet_name=endpoint, index=False)
                logger.info(f"Saved {endpoint} data to sheet.")
        logger.info(f"Data successfully saved to {filename}.")


# Приклад класу, який реалізує тільки DataSaver
class ExcelDataManager(DataSaver):
    def save_to_excel(self, filename: str):
        # Реалізація тільки для збереження даних
        pass