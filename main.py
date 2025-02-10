from functions import speak, listen, execute_command, check_system
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Запуск программы")
    speak("Привет! Я Вероника. Чем могу помочь?")
    if check_system():
        speak("Система готова к работе")
        logging.info("Система готова к работе")
        while True:
            command = listen()
            if command:
                execute_command(command)
    else:
        speak("Проблема с системой. Проверьте установку библиотек.")
        logging.error("Проблема с системой. Проверьте установку библиотек.")

if __name__ == "__main__":
    main()