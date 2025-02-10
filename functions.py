import os
import webbrowser
import datetime
import pyttsx3
import speech_recognition as sr
import logging

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    logging.info(f"Вероника сказала: {text}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Слушаю...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="ru-RU")
            logging.info(f"Вы сказали: {command}")
            return command.lower()
        except sr.UnknownValueError:
            logging.error("Не удалось распознать речь")
            return ""
        except sr.RequestError:
            logging.error("Ошибка при подключении к сервису распознавания")
            return ""

def execute_command(command):
    logging.debug(f"Команда: {command}")
    if "открой браузер" in command:
        speak("Открываю браузер")
        webbrowser.open("https://www.google.com")
        logging.info("Команда выполнена: Открыть браузер")
    elif "включи музыку" in command:
        speak("Включаю музыку")
        os.system("start wmplayer")
        logging.info("Команда выполнена: Включить музыку")
    elif "сколько времени" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"Сейчас {now}")
        logging.info(f"Команда выполнена: Сообщить время ({now})")
    elif "создай папку" in command:
        folder_name = "Новая папка"
        folder_path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(folder_path, exist_ok=True)
        speak(f"Папка {folder_name} создана")
        logging.info(f"Команда выполнена: Создать папку ({folder_name})")
    elif "создай файл" in command:
        file_name = "новый_файл.txt"
        file_path = os.path.join(os.getcwd(), file_name)
        with open(file_path, 'w') as file:
            file.write("Привет, мир!")
        speak(f"Файл {file_name} создан")
        logging.info(f"Команда выполнена: Создать файл ({file_name})")
    elif "выключи компьютер" in command:
        speak("Выключаю компьютер")
        os.system("shutdown /s /t 1")
        logging.info("Команда выполнена: Выключить компьютер")
    elif "стоп" in command or "выход" in command:
        speak("До свидания!")
        logging.info("Команда выполнена: Остановить программу")
        exit()
    else:
        speak("Извините, я не понимаю эту команду")
        logging.warning("Команда не распознана")

def check_system():
    try:
        engine = pyttsx3.init()
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.listen(source, timeout=1)
        logging.info("Система проверки пройдена успешно")
        return True
    except Exception as e:
        logging.error(f"Ошибка системы: {e}")
        return False