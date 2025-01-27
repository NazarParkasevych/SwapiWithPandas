import requests
import logging
import pandas as pd
from abc import ABC, abstractmethod


class SWAPIClient:
    """
    Клієнт для роботи з API SWAPI.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def fetch_json(self, endpoint: str) -> list:
        """
        Завантажує дані з API з підтримкою пагінації.
        Аргументи:
            endpoint (str): Кінцева точка API (наприклад, 'people').
        Повертає:
            list: Список об'єктів JSON.
        """
        url = f"{self.base_url}{endpoint}/"
        all_data = []

        while url:
            self.logger.info(f"Отримання даних з: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data['results'])
            url = data.get('next')  # Наступна сторінка, якщо доступна

        return all_data


class EntityProcessor(ABC):
    """
    Абстрактний базовий клас для обробки сутностей.
    """

    @abstractmethod
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Метод для обробки даних сутності.
        """
        pass


class PeopleProcessor(EntityProcessor):
    """
    Процесор для обробки сутності 'people'.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['full_name'] = data['name']  # Додаємо колонку full_name
        return data


class PlanetsProcessor(EntityProcessor):
    """
    Процесор для обробки сутності 'planets'.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['population'] = pd.to_numeric(data['population'], errors='coerce')  # Перетворюємо на числовий формат
        return data


class FilmsProcessor(EntityProcessor):
    """
    Процесор для обробки сутності 'films'.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['title_length'] = data['title'].apply(len)  # Додаємо довжину назви фільму
        return data


class SWAPIDataManager:
    """
    Менеджер даних для роботи з SWAPI.
    """

    def __init__(self, client: SWAPIClient):
        self.client = client
        self.data = {}
        self.processors = {}
        self.logger = logging.getLogger(__name__)

    def register_processor(self, entity: str, processor: EntityProcessor):
        """
        Реєструє процесор для конкретної сутності.
        """
        self.processors[entity] = processor

    def fetch_entity(self, endpoint: str):
        """
        Завантажує сутність з API та перетворює її у DataFrame.
        """
        self.logger.info(f"Отримання даних для сутності: {endpoint}")
        json_data = self.client.fetch_json(endpoint)
        dataframe = pd.DataFrame(json_data)

        # Якщо зареєстрований процесор, обробляємо дані
        if endpoint in self.processors:
            self.logger.info(f"Обробка даних для сутності: {endpoint}")
            dataframe = self.processors[endpoint].process(dataframe)

        self.data[endpoint] = dataframe

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


# CLI-інтерфейс
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Ініціалізація клієнта та менеджера
    client = SWAPIClient(base_url="https://swapi.dev/api/")
    manager = SWAPIDataManager(client)

    # Реєстрація процесорів
    manager.register_processor("people", PeopleProcessor())
    manager.register_processor("planets", PlanetsProcessor())
    manager.register_processor("films", FilmsProcessor())

    # Завантаження та обробка даних
    manager.fetch_entity("people")
    manager.fetch_entity("planets")
    manager.fetch_entity("films")

    # Збереження у файл
    manager.save_to_excel("swapi_data.xlsx")
