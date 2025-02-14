import datetime
import os
import random
import re
import webbrowser
import socket
from typing import Dict, List, Callable
import pyttsx3
import speech_recognition as sr
from colorama import Fore, init

class VeronicaAssistant:
    def __init__(self):
        init(autoreset=True)
        self.engine = self._setup_tts_engine()
        self.recognizer = sr.Recognizer()
        self.commands = self._load_commands()
        self.urls = self._load_urls()
        socket.setdefaulttimeout(12)

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
            ],
            'yandex': 'https://ya.ru',
            'yandex_browser': 'C:\\Program Files (x86)\\Yandex\\YandexBrowser\\Application\\browser.exe'
        }

    def _load_commands(self) -> Dict[str, Callable]:
        return {
            'привет': self._greet,
            'что ты можешь': self._show_capabilities,
            'открой яндекс': lambda _: self._open_url(self.urls['yandex'], 'Яндекс'),
            'запусти браузер': lambda _: self._launch_browser('Яндекс.Браузер'),
            'открой youtube': lambda _: self._open_url('https://youtube.com', 'YouTube'),
            'запусти музыку': self._play_music,
            'вк музыка': lambda _: self._open_url(self.urls['vk_music'], 'ВК Музыка'),
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
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            try:
                audio = self.recognizer.listen(
                    source, 
                    phrase_time_limit=8
                )
            except sr.WaitTimeoutError:
                self.speak("Не услышала ваш голос. Попробуйте еще раз. 🎤")
                return ""

        for attempt in range(3):
            try:
                command = self.recognizer.recognize_google(
                    audio,
                    language="ru-RU",
                    show_all=False
                ).lower()
                print(Fore.YELLOW + f"Вы сказали: {command} 🗣️")
                return command
            except sr.UnknownValueError:
                self.speak("Я не поняла вашу команду. 🤔")
                return ""
            except sr.RequestError as e:
                if attempt < 2:
                    print(Fore.YELLOW + f"Повторная попытка распознавания ({attempt+1}/3)")
                    continue
                self._handle_network_error(e)
            except Exception as e:
                print(Fore.RED + f"Неожиданная ошибка: {str(e)}")
        return ""

    def _handle_network_error(self, error: Exception):
        error_msg = str(error).lower()
        if '10060' in error_msg or 'timed out' in error_msg:
            self.speak("Ошибка соединения: превышено время ожидания. Проверьте интернет. 🌐")
            print(Fore.RED + "Рекомендации:")
            print(Fore.RED + "1. Проверьте интернет-подключение")
            print(Fore.RED + "2. Отключите VPN/Прокси")
            print(Fore.RED + "3. Временно отключите антивирус")
        else:
            self.speak("Ошибка сети. Повторите попытку позже. 🔄")
        print(Fore.RED + f"Техническая информация: {str(error)}")

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
        try:
            webbrowser.open(url)
            self.speak(f"Открываю {service_name} 🌐")
        except Exception as e:
            self.speak(f"Не удалось открыть {service_name} 😟")
            print(Fore.RED + f"Ошибка: {str(e)}")

    def _launch_browser(self, browser_name: str) -> None:
        try:
            os.startfile(self.urls['yandex_browser'])
            self.speak(f"Запускаю {browser_name} 🌐")
        except Exception as e:
            self.speak(f"Не могу найти {browser_name} 😟")
            print(Fore.RED + f"Ошибка: {str(e)}")

    def _play_music(self, _: str = "") -> None:
        try:
            webbrowser.open(random.choice(self.urls['music']))
            self.speak("Включаю музыку 🎶")
        except Exception as e:
            self.speak("Не удалось включить музыку 😟")
            print(Fore.RED + f"Ошибка: {str(e)}")

    def _handle_twitch(self, command: str) -> None:
        try:
            if 'канал' in command:
                self._open_url(self.urls['my_twitch'], "ваш Twitch")
            else:
                self._open_url(self.urls['twitch'], "Twitch")
        except Exception as e:
            self.speak("Ошибка доступа к Twitch 😟")
            print(Fore.RED + f"Ошибка: {str(e)}")

    def _search_web(self, command: str) -> None:
        try:
            query = command.split('поиск', 1)[1].strip()
            webbrowser.open(f"https://yandex.ru/search/?text={query}")
            self.speak(f"Ищу в Яндексе: {query} 🔍")
        except Exception as e:
            self.speak("Не удалось выполнить поиск 😟")
            print(Fore.RED + f"Ошибка: {str(e)}")

    def _tell_time(self, _: str = "") -> None:
        time = datetime.datetime.now().strftime("%H:%M")
        self.speak(f"Сейчас {time} ⏰")

    def _close_application(self, command: str) -> None:
        try:
            if 'браузер' in command:
                os.system("taskkill /im browser.exe /f")
                self.speak("Закрываю Яндекс.Браузер 🖥️")
            else:
                self.speak("Не могу найти приложение для закрытия 😟")
        except Exception as e:
            self.speak("Ошибка при закрытии приложения 😟")
            print(Fore.RED + f"Ошибка: {str(e)}")

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
        assistant.speak("Произошла системная ошибка! Выключаюсь. ⚠️")