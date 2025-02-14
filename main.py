import speech_recognition as sr
import pyttsx3
import os
import json
import requests
import webbrowser
import datetime
import random
from vosk import Model, KaldiRecognizer

# Настройка голосового синтезатора
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Инициализация модели Vosk
model = Model("vosk-model-small-ru-0.22")
recognizer = KaldiRecognizer(model, 48000)

API_KEY = "sk-1be11ebf4d8942f59804f01b9fe4feac"
API_URL = "https://api.deepseek.com/process"

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для распознавания речи
def listen_command():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("Слушаю...")
        audio = r.listen(source)
    
    data = audio.get_wav_data()
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        return result.get("text", "").lower()
    return ""

# Функция для обработки текста через DeepSeek API
def process_text_with_deepseek(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"text": text}
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        print("Ответ от сервера:", response.text)  # Вывод ответа для отладки
        response.raise_for_status()
        response_json = response.json()
        return response_json.get("result", "Нет ответа от API")
    except json.decoder.JSONDecodeError:
        return "Ошибка: сервер вернул некорректный JSON"
    except requests.exceptions.RequestException as e:
        return f"Ошибка запроса: {str(e)}"

# Функция для рассказа шуток
def tell_joke():
    jokes = [
        "Почему программисты не ходят в лес? Потому что там много багов.",
        "Какой язык программирования предпочитают океаны? Си.",
        "Почему питоны никогда не устают? Потому что они всегда остаются гибкими."
    ]
    speak(random.choice(jokes))

# Функция для получения текущего времени
def get_current_time():
    now = datetime.datetime.now()
    speak(f"Сейчас {now.hour} часов и {now.minute} минут.")

# Функция для открытия приложения
def open_application(app_name):
    if app_name == 'блокнот':
        os.system('notepad.exe')
        speak("Блокнот открыт.")
    else:
        speak(f"Не могу открыть приложение {app_name}.")

# Функция для завершения работы программы
def close_program():
    speak("Завершаю работу. До свидания!")
    exit()

# Обработка команд
def process_command(command):
    if 'привет' in command:
        speak("Привет! Как я могу помочь?")
    elif 'поиск' in command:
        query = command.replace('поиск', '').strip()
        speak(f"Ищу {query} в интернете.")
        webbrowser.open(f"https://ya.ru//search?q={query}")
    elif 'расскажи шутку' in command:
        tell_joke()
    elif 'время' in command:
        get_current_time()
    elif 'открыть' in command:
        app_name = command.replace('открыть', '').strip()
        open_application(app_name)
    elif 'закрыть программу' in command:
        close_program()
    else:
        deepseek_result = process_text_with_deepseek(command)
        speak(f"DeepSeek отвечает: {deepseek_result}")

if __name__ == "__main__":
    speak("Голосовой помощник запущен. Готов к работе.")
    while True:
        command = listen_command()
        if command:
            process_command(command)