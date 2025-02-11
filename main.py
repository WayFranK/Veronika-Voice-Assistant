from functions import speak, listen, execute_command, check_system, check_updates, recognize_speaker, encrypt_data, decrypt_data, detect_anomalies
import logging
from config import setup_logging

# Настройка логирования
setup_logging()

def main():
    logging.info("Запуск программы")
    speak("Привет! Я Вероника. Чем могу помочь?")
    recognize_speaker()  # Аутентификация пользователя
    if check_system():
        speak("Система готова к работе")
        logging.info("Система готова к работе")
        logging.info("Программа работает корректно")
        check_updates()  # Проверка обновлений при запуске программы
        while True:
            command = listen()
            if command:
                execute_command(command)
    else:
        speak("Проблема с системой. Проверьте установку библиотек.")
        logging.error("Проблема с системой. Проверьте установку библиотек.")
        logging.error("Программа не может быть запущена")

if __name__ == "__main__":
    main()