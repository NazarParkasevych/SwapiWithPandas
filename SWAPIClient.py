import requests
import logging


class SWAPIClient:
    """
    Клієнт для роботи з API SWAPI.
    """

    def __init__(self, base_url: str):
        """
        Ініціалізує клієнт з базовим URL для API.
        """
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
            try:
                self.logger.info(f"Отримання даних з: {url}")
                response = requests.get(url)
                response.raise_for_status()  # Перевірка на помилки HTTP
                data = response.json()
                all_data.extend(data['results'])
                url = data.get('next')  # Наступна сторінка, якщо доступна
            except requests.RequestException as e:
                self.logger.error(f"Помилка при запиті до {url}: {e}")
                break

        return all_data
