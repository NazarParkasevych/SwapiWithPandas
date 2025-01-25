import pandas as pd
import requests
import logging

from pywin.tools.TraceCollector import outputWindow

# Налаштування Логера
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
def fetch_all_entities(base_url):
    """
    Отримання всіх сутностей з API з пагінацією
    Аргументи:
    base_url(str): Базова URL-адреса кінцевої точки SWAPI (наприклад, "https://swapi.dev/api/people/")
    Повертає:
    pd.DataFrame: DataFrame, о містить усі сутності.
    """
    all_data = []
    url = base_url # Почати з першої сторінки

    while url:
       # логування запиту
       logger.info(f"Отримання даних з: {url}")

       # Отримання даних з API
       response = requests.get(url)
       response.raise_for_status() # Генерація помилок для нневдалих відповідей
       data = response.json()

       # Додавання результатів до списку
       all_data.extend(data['results'])

       # Перехід до наступної сторінки
       url = data.get('next')

    # Перетворення списку даних у DataFrame
    return pd.DataFrame(all_data)

# Отримання сутностей
logger.info("Отримання даних про людей...")
people_df = fetch_all_entities("https://swapi.dev/api/people/")

logger.info("Отримання даних про планети...")
planets_df = fetch_all_entities("https://swapi.dev/api/planets/")

# Вихідний файл
output_file = 'swapi.xlsx'

# Запис у Excel з окремими листами
logger.info(f"Запис даних у Excel файл: {output_file}")
with pd.ExcelWriter(output_file) as writer:
    people_df.to_excel(writer, sheet_name="People", index=False) # Запис першого DataFrame
    planets_df.to_excel(writer, sheet_name="Planets", index=False) # Запис Другого DataFrame
logger.info("Дані успішно записано у Excel.")





