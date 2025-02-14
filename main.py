import datetime
import os
import random
import re
import webbrowser
from typing import Dict, List

import pyttsx3
import speech_recognition as sr
from colorama import Fore, Back, Style, init


class VeronicaAssistant:
    def __init__(self):
        init(autoreset=True)
        self.engine = self._setup_tts_engine()
        self.recognizer = sr.Recognizer()
        self.commands = self._load_commands()
        self.urls = self._load_urls()

    @staticmethod
    def _setup_tts_engine() -> pyttsx3.Engine:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        return engine

    def _load_urls(self) -> Dict[str, str | List[str]]:
        return {
            'twitch': 'https://www.twitch.tv',
            'my_twitch': 'https://www.twitch.tv/michal_ivanich',
            'vk_music': 'https://vk.com/music/playlist/-88066503_56557078',
            'music': [
                'https://www.youtube.com/watch?v=ca0775s0TxM',
                'https://www.youtube.com/watch?v=M5QY2_8704o',
                'https://www.youtube.com/watch?v=qwHyfcCvBFQ'
            ]
        }

    def _load_commands(self) -> Dict[str, str]:
        return {
            'привет': self._greet,
            'что ты можешь': self._show_capabilities,
            'открой google': lambda: self._open_url('https://google.com', 'Google'),
            'открой youtube': lambda: self._open_url('https://youtube.com', 'YouTube'),
            'запусти музыку': self._play_music,
            'вк музыка': lambda: self._open_url(self.urls['vk_music'], 'ВК Музыка'),
            'twitch': self._handle_twitch,
            'поиск': self._search_web,
            'время': self._tell_time,
            'закрой': self._close_application,
            'шутка': self._tell_joke
        }

    def speak(self, text: str) -> None:
        cleaned_text = re.sub(r'[^\w\s,\.!?-]', '', text)
        self.engine.say(cleaned_text)
        self.engine.runAndWait()
        print(Fore.BLUE + f"Ответ: {text}")

    def listen_command(self) -> str:
        with sr.Microphone() as source:
            print(Fore.GREEN + "Слушаю... 🎧")
            self.recognizer.adjust_for_ambient_noise(source)
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
            except sr.WaitTimeoutError:
                self.speak("Не услышала ваш голос. Попробуйте еще раз. 🎤")
                return ""

        try:
            command = self.recognizer.recognize_google(audio, language="ru-RU").lower()
            print(Fore.YELLOW + f"Вы сказали: {command} 🗣️")
            return command
        except sr.UnknownValueError:
            self.speak("Я не поняла вашу команду. 🤔")
        except sr.RequestError as e:
            self.speak("Проблемы с соединением. Проверьте интернет. 🌐")
            print(Fore.RED + f"Ошибка сервиса: {str(e)}")
        return ""

    def process_command(self, command: str) -> None:
        for key in self.commands:
            if key in command:
                self.commands[key](command)
                return
        
        self.speak("Не распознала команду 😔")

    def _greet(self, _: str = "") -> None:
        self.speak("Привет! Как я могу помочь? 🤖")

    def _show_capabilities(self, _: str = "") -> None:
        self.speak("Я могу открывать сайты, искать информацию, говорить время и рассказывать шутки! 😊")

    def _open_url(self, url: str, service_name: str) -> None:
        webbrowser.open(url)
        self.speak(f"Открываю {service_name} 🌐")

    def _play_music(self, _: str = "") -> None:
        webbrowser.open(random.choice(self.urls['music']))
        self.speak("Включаю музыку 🎶")

    def _handle_twitch(self, command: str) -> None:
        if 'канал' in command:
            self._open_url(self.urls['my_twitch'], "ваш Twitch")
        else:
            self._open_url(self.urls['twitch'], "Twitch")

    def _search_web(self, command: str) -> None:
        query = command.split('поиск', 1)[1].strip()
        webbrowser.open(f"https://google.com/search?q={query}")
        self.speak(f"Ищу {query} 🔍")

    def _tell_time(self, _: str = "") -> None:
        time = datetime.datetime.now().strftime("%H:%M")
        self.speak(f"Сейчас {time} ⏰")

    def _close_application(self, command: str) -> None:
        if 'браузер' in command:
            os.system("taskkill /im chrome.exe /f")
            self.speak("Закрываю браузер 🖥️")
        else:
            self.speak("Не могу найти приложение для закрытия 😟")

    def _tell_joke(self, _: str = "") -> None:
        jokes = [
            "Почему программисты не ходят в лес? Потому что там много багов. 🐞",
            "Какой язык программирования предпочитают океаны? Си. 🌊",
            "Почему питоны никогда не устают? Потому что они всегда остаются гибкими. 🐍",
            "Почему Java-программисты всегда носят очки? Потому что они не могут C#. 👓",
            "Что говорят разработчики, когда их код работает? Это магия! ✨"
        ]
        joke = random.choice(jokes)
        self.speak(joke)
        print(Fore.CYAN + f"Шутка: {joke} 😄")


if __name__ == "__main__":
    assistant = VeronicaAssistant()
    assistant.speak("Голосовой помощник Вероника активирован! Чем могу помочь?")
    print(Fore.CYAN + "Голосовой помощник Вероника активирован!")
    
    try:
        while True:
            command = assistant.listen_command()
            if command:
                assistant.process_command(command)
    except KeyboardInterrupt:
        assistant.speak("Выключаюсь! До свидания! 👋")
    except Exception as e:
        print(Fore.RED + f"Критическая ошибка: {str(e)}")
        assistant.speak("Произошла критическая ошибка, экстренное выключение! ⚠️")