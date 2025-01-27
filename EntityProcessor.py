from abc import ABC, abstractmethod
import pandas as pd

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
