import os 
import platform
import subprocess 
import threading 
from django.core.management.base import BaseCommand
from core.models import AppCommand, VoiceResponse 
from utils.finder import find_app_path 
from utils.voice_engine import speak_async
import speech_recognition as sr

from core.management.commands.add_commands import add_new_app_command_voice

APP_CACHE = {}

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Assitant was launched.."))
        
        recogniser = sr.Recognizer()
        mic = sr.Microphone()
        
        with mic as source:
            self.stdout.write(self.style.SUCCESS(f"Setting background noise "))
            recogniser.adjust_for_ambient_noise(source, 1)
            self.stdout.write(self.style.SUCCESS(f"Microphone was activated"))
            
            while True:
                try:
                    audio = recogniser.listen(source, None, 10)
                    command_text = recogniser.recognize_google(audio, language="uk-UA")
                    self.stdout.write(f"Ви сказали: {command_text}")
                    self.process_command(command_text, source)

                except sr.UnknownValueError:
                    continue
                except Exception as error:
                    self.stdout.write(self.style.ERROR(f"Error: {error}"))

    def process_command(self, text, source):
        text = text.lower().strip()

        if "додати команду" in text:
            add_new_app_command_voice()
            return

        if "відкрий" not in text:
            for resp in VoiceResponse.objects.all():
                if resp.keyword and resp.keyword.lower() in text:
                    speak_async(resp.response)
                    return
            return    
        
        found_app = None

        for app in AppCommand.objects.all():
            if app.keyword and app.keyword.lower() in text:
                found_app = app  
                break

        if not found_app:
            speak_async("Я не знайшов таку команду")
            return
        
        if found_app.app_name in APP_CACHE and os.path.exists(APP_CACHE[found_app.app_name]):
            speak_async(f'Відкриваю {found_app.app_name}')
            self.launch_app(APP_CACHE[found_app.app_name])
            return
        
        speak_async(f"Шукаю {found_app.app_name}")

        def find_and_launch():
            found_path = find_app_path(found_app.app_name)
            if found_path:
                APP_CACHE[found_app.app_name] = found_path
                found_app.path = found_path
                found_app.save()
                self.launch_app(found_path)
            else:
                speak_async(f'Не знайшов шлях до данної програми ')
        
        threading.Thread(target=find_and_launch, daemon = True).start()
    
    def launch_app(self, path):
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(path)
            elif system == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen([path])
        except Exception as error:
            self.stdout.write(self.style.ERROR(f"Error: {error}"))
    