import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class ExcelSWAPIClient:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_json(self, endpoint: str) -> list:
        # Відповідність між сутністю та назвою листа в Excel
        sheet_name_map = {
            "people": "people",
            "planets": "planets",
            "films": "films"
        }

        # Перевірка на допустимий endpoint
        if endpoint not in sheet_name_map:
            raise ValueError(f"Невідомий endpoint: {endpoint}")

        sheet_name = sheet_name_map[endpoint]

        try:
            # Читання даних з відповідного листа
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            logger.info(f"Читання даних з файлу {self.file_path}, лист {sheet_name}")
            return df.to_dict(orient='records')
        except ValueError as e:
            # Якщо лист не знайдений у файлі
            raise ValueError(f"Помилка при зчитуванні даних з файлу {self.file_path}: {e}")
        except Exception as e:
            # Інші помилки
            logger.error(f"Не вдалося зчитати дані з файлу: {e}")
            raise