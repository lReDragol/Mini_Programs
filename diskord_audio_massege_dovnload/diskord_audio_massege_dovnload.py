import requests
from pydub import AudioSegment
import os

def download_voice_message(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Голосовое сообщение сохранено в {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании голосового сообщения: {e}")

def convert_to_mp3(input_path, output_path):
    if os.path.exists(input_path):
        audio = AudioSegment.from_ogg(input_path)
        audio.export(output_path, format="mp3")
        print(f"Конвертация завершена. Файл сохранён как {output_path}")
    else:
        print(f"Файл {input_path} не найден. Конвертация не выполнена.")

url = input("Введите ссылку на голосовое сообщение: ")

save_path_ogg = "voice-message.ogg"
save_path_mp3 = "voice-message.mp3"
download_voice_message(url, save_path_ogg)
convert_to_mp3(save_path_ogg, save_path_mp3)
