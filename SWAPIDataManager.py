import pandas as pd
import logging


class SWAPIDataManager:
    def __init__(self, client):
        self.client = client
        self.data = {}
        self.logger = logging.getLogger(__name__)

    def fetch_entity(self, endpoint: str):
        """
        Завантаження сутності з API та збереження у внутрішньому словнику.
        """
        self.logger.info(f"Отримання даних для сутності: {endpoint}")
        json_data = self.client.fetch_json(endpoint)
        self.data[endpoint] = pd.DataFrame(json_data)

    def apply_filter(self, endpoint: str, columns_to_drop: list):
        """
        Видалення стовпців із DataFrame.
        """
        if endpoint in self.data:
            self.logger.info(f"Застосування фільтру для: {endpoint}")
            self.data[endpoint].drop(columns=columns_to_drop, inplace=True)
        else:
            self.logger.warning(f"Сутність '{endpoint}' не завантажена!")

    def save_to_excel(self, filename: str):
        """
        Збереження всіх завантажених даних у Excel.
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
