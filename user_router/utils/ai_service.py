import os
import google.generativeai as genai
from google import genai as text_genai
from google.genai import types
from google.ai.generativelanguage_v1beta.types import content
from pathlib import Path
import json

from config import Settings
from database.db import get_user_language
from user_router.utils.service import show_progress, sync_show_progress

settings = Settings()

photo_analys_text = """
Ты — высококвалифицированная модель для проверки пригодности фотографий лица к анализу состояния кожи. Оцени изображение по пяти параметрам:

1. Освещённость

   * Нет пере- или недоэкспонированных областей
   * Отсутствуют блики и глубокие тени

2. Резкость

   * Изображение в фокусе (Laplacian Variance выше порога)

3. Положение лица

   * Лицо занимает от 65% кадра
   * Ракурс фронтальный, отклонение не более 15 °

4. Отсутствие косметики и фильтров

   * Нет явных тональных изменений, постобработки или наложенных фильтров

5. Разрешение и качество

   * Минимум 640×640 px
   * Отсутствие сильных артефактов сжатия

Если не менее четырёх из пяти критериев соблюдены, модель отвечает `true`, иначе — `false`. Отвечай исключительно одним словом: `true` или `false`.
"""

def analysis_image(image_path: str):
    genai.configure(api_key=settings.GENAI_TOKEN)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            properties = {
            "face": content.Schema(
                type = content.Type.BOOLEAN,
            ),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=photo_analys_text,
    )

    # Загрузка изображения
    image_path = f"{image_path}"
    image_data = {
        'mime_type': 'image/jpeg',
        'data': Path(image_path).read_bytes()
    }
    # chat_session = model.start_chat(
    #   history=[
    #   ]
    # )

    # Отправка сообщения с изображением
    response = model.generate_content(
        contents={
            'parts': [
                image_data
            ]
        }
    )

    print(response.text)
    return json.loads(response.text)

summary_report_text = """
Ты — высококвалифицированная модель-редактор отчётов. На вход ты получаешь JSON-объект со следующими полями:

{
  "Introduction": string,
  "Skin Condition Analysis": string,
  "Lifestyle Impact on Skin": string,
  "Personal Skincare Recommendations": string,
  "Improvement Forecast": string,
  "Conclusion and Support": string,
  "Web search info": string,
  "Google Search Suggestions": [string]
}

Твоя задача — вывести ОДИН JSON-объект строго по этой схеме:

{
  "type": "object",
  "properties": {
    "Introduction": {
      "type": "string",
      "description": "✨ Введение и текст введения отчёта"
    },
    "Skin Condition Analysis": {
      "type": "string",
      "description": "🔎 Анализ состояния кожи на основе фото"
    },
    "Lifestyle Impact on Skin": {
      "type": "string",
      "description": "🌱 Влияние образа жизни на кожу"
    },
    "Personal Skincare Recommendations": {
      "type": "string",
      "description": "💧 Персональная программа ухода в полном объёме"
    },
    "Improvement Forecast": {
      "type": "string",
      "description": "📈 Прогноз улучшений при соблюдении рекомендаций"
    },
    "Conclusion and Support": {
      "type": "string",
      "description": "🏁 Заключение и поддержка"
    }
  },
  "required": [
    "Introduction",
    "Skin Condition Analysis",
    "Lifestyle Impact on Skin",
    "Personal Skincare Recommendations",
    "Improvement Forecast",
    "Conclusion and Support"
  ],
  "additionalProperties": false
}

Правила преобразования:
1. Поля `Web search info` и `Google Search Suggestions` удалить; они не должны попасть в финальный вывод.
2. Сохранять оригинальный текст всех полей дословно, без изменений, особенно раздел рекомендаций, за исключением любой Markdown-разметки.
3. Удалить всю Markdown-разметку: заголовки уровня `#`, списковые маркеры `-`, `*`, цифры перед пунктами, подчёркивания и т. п.
4. В начале каждого текстового поля вставить соответствующий эмодзи-заголовок (✨ для Introduction, 🔎 для Skin Condition Analysis, 🌱 для Lifestyle Impact on Skin, 💧 для Personal Skincare Recommendations, 📈 для Improvement Forecast, 🏁 для Conclusion and Support).
5. Удалить любые числа в квадратных скобках — считать их техническим мусором.
6. Не оставлять ссылок, скобочных ссылок или других технических пометок.
7. Вывести только один JSON-объект, строго соответствующий указанной схеме.
"""

def get_summary_report(user_id: any, data):
    user_language = get_user_language(user_id=user_id)
    user_data = sync_show_progress(data)
    client = text_genai.Client(
        api_key=settings.GENAI_TOKEN,
    )

    model = "gemini-2.0-flash"
    
    # Создаем части контента
    parts = [
        types.Part.from_text(text=user_data),  # Ваш текстовый запрос
    ]
    
    # Добавляем фотографии
    for file_name in os.listdir(f"images/{user_id}"):
        # try:
            with open(f"images/{user_id}/{file_name}", "rb") as image_file:
                image_data = image_file.read()
                # print(len(image_data))
                parts.append(types.Part.from_bytes(data=image_data, mime_type="image/jpeg"))
        # except Exception as e:
        #     print(f"Error loading image {user_id}/{file_name}: {str(e)}")
        #     continue

    contents = [
        types.Content(
            role="user",
            parts=parts,
        ),
    ]

    tools = [
        types.Tool(google_search=types.GoogleSearch())
    ]

    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=summary_report_text+f" write the report in {user_language}."),  # Ваша текущая инструкция
        ],
    )

    try:
        response = []
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                response.append(chunk.text)
                # print(chunk.text, end="")

        json_data = "".join(response)

        cleaned_json = json_data.strip('```json').strip('```').strip().replace("*", "")
        print(cleaned_json)
        # Парсим в словарь
        data_dict = json.loads(cleaned_json)
        
        return data_dict
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None