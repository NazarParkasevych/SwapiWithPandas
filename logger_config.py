import logging

# Налаштування логера
logging.basicConfig(
    level=logging.INFO,  # Мінімальний рівень логування (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат повідомлення
    datefmt="%Y-%m-%d %H:%M:%S"  # Формат часу
)

# Головний логер, який можна імпортувати
logger = logging.getLogger("SWAPIDataManager")
