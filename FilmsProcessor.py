import pandas as pd
from EntityProcessor import EntityProcessor

class FilmsProcessor(EntityProcessor):
    """
    Процесор для обробки сутності 'films'.
    """

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data['title_length'] = data['title'].apply(len)  # Додаємо довжину назви фільму
        return data
