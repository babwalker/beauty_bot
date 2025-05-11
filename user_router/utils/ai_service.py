import os
import re
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

def first_generate(user_language, user_data, user_id):
    client = text_genai.Client(
        api_key=settings.GENAI_TOKEN,
    )

    model = "gemini-2.0-flash"
    parts=[
        types.Part.from_text(text=user_data+f" write the report in {user_language}."),
    ]
    # Добавляем фотографии
    for file_name in os.listdir(f"images/{user_id}"):
        with open(f"images/{user_id}/{file_name}", "rb") as image_file:
            image_data = image_file.read()
            parts.append(types.Part.from_bytes(data=image_data, mime_type="image/jpeg"))

    contents = [
        types.Content(
            role="user",
            parts=parts
        ),
    ]
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.75,
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a cosmetologist with 20 years of experience and an expert in skin analysis. Based on:  
1) user's personal data (skin type, problems, lifestyle, wishes, budget, etc.),  
2) provided photos (if available),  
3) * * mandatory use of web search tools** to select current cosmetics and get information about their composition and cost,  
4) as well as your professional expertise,

your task is to create a * * report* * strictly consisting of six sections (Introduction, Skin condition Analysis, Lifestyle Impact, Personal care recommendations, Improvement forecast, Conclusion and support). ** The assistant's response** should contain **only** the contents of these six sections, without additional service phrases, headings, explanations, or comments.

### 1. Response structure and format

The response **must* * consist * * strictly** of the following six sections, presented sequentially and without additional opening or closing phrases in json format:

{
  \"type\": \"object\",
  \"properties\": {
    \"Introduction\": { \"type\": \"string\" },
    \"Skin Condition Analysis\": { \"type\": \"string\" },
    \"Lifestyle Impact on Skin\": { \"type\": \"string\" },
    \"Personal Skincare Recommendations\": { \"type\": \"string\" },
    \"Improvement Forecast\": { \"type\": \"string\" },
    \"Conclusion and Support\": { \"type\": \"string\" },
    \"Web search info\": { \"type\": \"string\" }
  },
  \"required\": [
    \"Introduction\",
    \"Skin Condition Analysis\",
    \"Lifestyle Impact on Skin\",
    \"Personal Skincare Recommendations\",
    \"Improvement Forecast\",
    \"Conclusion and Support\",
    \"Web search info\"
  ]
}


1. **Introduction**
- Greeting by name.  
   - A brief explanation of the report's purpose.  
   - The importance of proper care and its impact on skin health.

2. * * Skin condition analysis**
- Skin type (for example, dry, oily, combination).  
   - Main problems (peeling, pigmentation, wrinkles, etc.).
- Possible causes (improper care, lifestyle, allergies).  
   - Taking into account special features and clarifying them based on photos (if provided).

3. * * Lifestyle effects on the skin**
- How factors like stress, lack of sleep, ecology, nutrition, computer work, etc. affect the skin.  
   - Recommendations for lifestyle adjustments and the frequency of cosmetic procedures.

4. **Personal care recommendations* *
Search the Internet for products and write the current price.
   - Morning ritual (cleansing, toning, moisturizing, protection).  
   - Evening ritual (cleansing, recovery, nutrition).  
   - **Specific beauty products** (including brand names that must be found using a web search), while specifying key ingredients so that you can find analogs if necessary.  
   - Take into account allergies, budget, wishes (natural composition, lack of silicones/parabens, etc.).
- Lifestyle recommendations (sleep, nutrition, drinking regime).

5. **Forecast of improvements* *
- What changes may occur in 1 week, 1 month, or 3 months.  
   - Expected results if the recommendations are followed.

6. * * Conclusion and support**
- Final guidance: the importance of systematic care, the ability to ask questions and refine the program.
7. **Web search info**
   - Complete information about Internet search, and a report on the used links to funds. This section contains all the sites you have viewed and where you take care products from. This is a technical part of the report, and it will not be included in the main report. the user won't see it. In this part, you must provide links to sources.
### 2. Rules and restrictions

1. * * Single message**: the report must be generated by a single message from the assistant, without dividing it into several parts.  
2. **Report text only**: no official phrases like \"Here is your report\" or \"This is how we see...\" — only six sections, strictly according to the list.  
3. * * Mandatory use of web search**:
- When choosing specific cosmetics, you should request information about available products, their compositions, current prices and alternative options.  
   - Try to select funds based on the specified budget, and if necessary, mention analogues from a more expensive or more affordable price category.  
4. * * Follow the format**: do not add additional sections, subthemes, or non-standard headings.
5. **Budget accounting**: if the user's budget is low, indicate more affordable funds, but you can briefly mark alternatives in the middle or premium segment.  
6. * * Photos**: If the photos are provided, mention your visual observations in the skin condition analysis. If not, make a reservation that the withdrawal is based only on personal data.  
7. * * Style**: write in a friendly, professional and clear manner, avoiding unnecessarily complex medical terms.
"""),
        ],
    )

    response = []
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            response.append(chunk.text) 
    return "".join(response)

def get_summary_report(user_id: any, data):
    user_language = get_user_language(user_id=user_id)
    user_data = sync_show_progress(data)
    first_generate_response = first_generate(user_language=user_language, user_data=user_data, user_id=user_id)
    client = text_genai.Client(
        api_key=settings.GENAI_TOKEN,
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=first_generate_response),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.65,
        response_mime_type="application/json",
        response_schema=text_genai.types.Schema(
            type = text_genai.types.Type.OBJECT,
            required = ["Introduction", "Skin Condition Analysis", "Lifestyle Impact on Skin", "Personal Skincare Recommendations", "Improvement Forecast", "Conclusion and Support"],
            properties = {
                "Introduction": text_genai.types.Schema(
                    type = text_genai.types.Type.STRING,
                    description = "Текст введения отчёта, начинающийся с эмодзи ✨ Введение",
                ),
                "Skin Condition Analysis": text_genai.types.Schema(
                    type = text_genai.types.Type.STRING,
                    description = "Описание текущего состояния кожи на основе фото, начинающееся с эмодзи 🔎 Анализ состояния кожи",
                ),
                "Lifestyle Impact on Skin": text_genai.types.Schema(
                    type = text_genai.types.Type.STRING,
                    description = "Как образ жизни влияет на кожу, начинающееся с эмодзи 🌱 Влияние образа жизни",
                ),
                "Personal Skincare Recommendations": text_genai.types.Schema(
                    type = text_genai.types.Type.STRING,
                    description = "Персональные рекомендации по уходу, начинающиеся с эмодзи 💧 Персональная программа ухода",
                ),
                "Improvement Forecast": text_genai.types.Schema(
                    type = text_genai.types.Type.STRING,
                    description = "Ожидаемые изменения при соблюдении рекомендаций, начинающееся с эмодзи 📈 Прогноз улучшений",
                ),
                "Conclusion and Support": text_genai.types.Schema(
                    type = text_genai.types.Type.STRING,
                    description = "Заключение и поддержка, начинающееся с эмодзи 🏁 Заключение и поддержка",
                ),
            },
        ),
                system_instruction=[
            types.Part.from_text(text="""Ты — высококвалифицированная модель-редактор отчётов. На вход ты получаешь JSON-объект со следующими полями:

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
2. Сохранять оригинальный текст всех полей дословно, без изменений, особенно раздел рекомендаций, за исключением любой Markdown-разметки. Допустимы изменения пунктуации, создание переносов строки и абзацев внутри логических блоков.
3. Удалить всю Markdown-разметку: заголовки уровня `#`, списковые маркеры `-`, `*`, цифры перед пунктами, подчёркивания и т. п.
4. Сформировать логические абзацы, переносы строк. Исправить пунктуацию, и сделать текст внутри каждого блока более читаемым за счет абзацев и переносов строки.
5. В начале каждого текстового поля вставить соответствующий эмодзи-заголовок (✨ для Introduction, 🔎 для Skin Condition Analysis, 🌱 для Lifestyle Impact on Skin, 💧 для Personal Skincare Recommendations, 📈 для Improvement Forecast, 🏁 для Conclusion and Support).
6. Удалить любые числа в квадратных скобках — считать их техническим мусором.
7. Не оставлять ссылок, скобочных ссылок или других технических пометок.
8. Вывести только один JSON-объект, строго соответствующий указанной схеме.
9. Важно проверить, чтобы весь отчет был написан от лица женщины Нади Ульри, а значит, в женском роде, когда это требуется. Например: Я всегда готова помочь.                                 
"""),
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

        cleaned_json = clean_response_text(json_data)
        print(cleaned_json)
        # Парсим в словарь
        data_dict = json.loads(cleaned_json)
        
        return data_dict
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return None
    
def clean_response_text(text: str) -> str:
    """Очищает текст ответа: удаляет квадратные скобки и форматирует для JSON"""
    # Удаляем квадратные скобки с цифрами
    # text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', text)
    # Дополнительная очистка (если нужно)
    text = text.strip('```json').strip('```').strip()
    # .replace("*", "")
    return text