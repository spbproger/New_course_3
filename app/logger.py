import logging

def create_logger():
    """
    Создаем логгер
    """
    logger = logging.getLogger("basic")
    logger.setLevel("DEBUG")                # Определяем режим логгирования

    file_handler = logging.FileHandler("logs/api.log", encoding="utf-8")        # Записываем данные логгирования в файле
    logger.addHandler(file_handler)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")    # Определяем формат записи данных логгирования в файле
    file_handler.setFormatter(formatter)

    return logger