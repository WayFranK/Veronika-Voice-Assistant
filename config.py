import logging

def setup_logging():
    # Настройка логирования
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')