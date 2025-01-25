import requests
import logging


class SWAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)

    def fetch_json(self, endpoint: str) -> list:
        """
        Отримання даних з API з пагінацією.
        """
        url = f"{self.base_url}{endpoint}"
        all_data = []
        while url:
            self.logger.info(f"Отримання даних з: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            all_data.extend(data['results'])
            url = data.get('next')
        return all_data
