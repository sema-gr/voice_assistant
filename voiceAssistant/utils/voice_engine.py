import edge_tts
import time, asyncio, os, pygame
import threading


pygame.mixer.init()

def speak_task(text):
    file_name = f"voice_{int(time.time())}.mp3"
    VOICE = "uk-UA-OstapNeural" # uk-UA-PolinaNeural

    try:

        async def generate():
            communicate = edge_tts.Communicate(
                text,
                voice= VOICE
            )
            await communicate.save(file_name)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(generate())
        loop.close()

        if os.path.exists(file_name):
            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            time.sleep(1)
            os.remove(file_name)
            print(f"file {file_name} deleted")
    except Exception as error:
        print(error)

def speak_async(text):
    threading.Thread(target = speak_task, args = (text,), daemon = True).start()

# speak_task("Привіт це тест синхронного озвучування")
# print("тест speak_task")

# speak_async("Привіт це тест асинхронного озвучування")
# print("тест speak_async")

# time.sleep(5)
# print("тест завершено")


       
        


