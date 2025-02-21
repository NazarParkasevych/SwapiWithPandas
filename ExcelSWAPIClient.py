import pandas as pd
import logging

class ExcelSWAPIClient:
    """
    Клієнт для отримання даних з Excel-файлу, аналогічно SWAPIClient.
    """
    def __init__(self, file_path: str):
        """
        Ініціалізує клієнт із шляхом до файлу.
        """
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        self.data = self._load_excel_data()

    def _load_excel_data(self):
        """
        Завантажує всі аркуші Excel-файлу в пам'ять.
        """
        try:
            self.logger.info(f"Завантаження Excel-файлу: {self.file_path}")
            return pd.read_excel(self.file_path, sheet_name=None)
        except Exception as e:
            self.logger.error(f"Помилка при читанні файлу {self.file_path}: {e}")
            return {}

    def fetch_json(self, endpoint: str) -> list:
        """
        Повертає дані з відповідного аркуша як список словників.
        """
        if endpoint in self.data:
            return self.data[endpoint].to_dict(orient="records")
        else:
            self.logger.error(f"Помилка: Лист '{endpoint}' не знайдено у файлі {self.file_path}")
            return []
