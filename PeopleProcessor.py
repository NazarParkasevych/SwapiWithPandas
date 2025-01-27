import pandas as pd
from EntityProcessor import EntityProcessor

class PeopleProcessor(EntityProcessor):
    """
    Процесор для обробки сутності 'people'.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['full_name'] = data['name']  # Додаємо колонку full_name
        return data