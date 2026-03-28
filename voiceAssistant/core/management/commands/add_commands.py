import time
from utils.voice_engine import speak_async, speak_task
import speech_recognition as sr
from core.models import AppCommand

def get_voice_input():
    time.sleep(0.5)
    try:
        with sr.Microphone(device_index=1) as source:
            print("listening")
            recogniser = sr.Recognizer()
            recogniser.adjust_for_ambient_noise(source, 1)
            audio = recogniser.listen(source, None, phrase_time_limit=5)
        print("Recognasing")
        text = recogniser.recognize_google(audio, language="uk-UA")
        return text 
    except Exception as error :
        speak_async(f"Помилка  {error}")
        return ""

def add_new_app_command_voice():
    speak_task("Щоб додати команду скажіть ключове слово")
    keyword = get_voice_input()
    
    if not keyword: 
        speak_task("Я не почув слово, спробуйте ще раз")
        return
    
    speak_task(f"Ваше слово {keyword}. Підтвердити?")
    confirm = get_voice_input()
    
    print(f"Ассистент почув {confirm}")
    
    if "підтвер" not in str(confirm):
        speak_task("Дію скасовано")
        return
    
    speak_task("Скажіть назву додатку")
    app_name = get_voice_input()
    
    if not app_name: 
        speak_task("Я не почув назву додатку, спробуйте ще раз")
        return
    
    app_name = app_name.replace("крапка", ".").replace(" ", "")
    speak_task(f"Назва додатку {app_name}. Підтвердити?")
    
    confirm_app = get_voice_input()
    print(f"Асистент почув: {confirm_app}")

    if "підтвер" not in str(confirm_app):
        speak_task("Дію скасовано")
        return
    
    AppCommand.objects.create(
        keyword=keyword,
        app_name=app_name
    )

    speak_task(f"Ваша команда {keyword} успішно додана")
    print(f"Збережено: {keyword} - {app_name}")