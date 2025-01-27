import pandas as pd
from EntityProcessor import EntityProcessor

class PlanetsProcessor(EntityProcessor):
    """
    Процесор для обробки сутності 'planets'.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['population'] = pd.to_numeric(data['population'], errors='coerce')  # Перетворюємо на числовий формат
        return data
