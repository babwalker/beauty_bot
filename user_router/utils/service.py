from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from docxtpl import DocxTemplate
import os

from database.db import get_user_language
from user_router.utils.locales import translations, fields_translations
from user_router.utils.inline_buttons_data import inline_translations

def sync_show_progress(data):
    user_language = get_user_language(user_id=data.get("user_id"))

    # Получаем переводы для текущего языка, или используем английский по умолчанию
    translations = fields_translations.get(user_language)

    fields = {
        translations["name"]: data.get("name"),
        translations["country"]: data.get("country"),
        translations["email"]: data.get("email"),
        translations["age"]: data.get("age"),
        translations["gender"]: data.get("gender"),
        translations["skin_type"]: data.get("skin_type"),
        translations["skin_problems"]: ", ".join(data.get("skin_problems")) if data.get("skin_problems") else None,
        translations["skin_features"]: data.get("skin_features"),
        translations["lifestyles"]: ", ".join(data.get("lifestyles")) if data.get("lifestyles") else None,
        translations["water_intake"]: data.get("water_intake"),
        translations["daily_products"]: ", ".join(data.get("daily_products")) if data.get("daily_products") else None,
        translations["procedures_frequency"]: data.get("procedures_frequency"),
        translations["budget"]: data.get("budget"),
        translations["composition_prefs"]: ", ".join(data.get("composition_prefs")) if data.get("composition_prefs") else None,
        translations["full_face"]: data.get("full_face"),
        translations["right_side_face"]: data.get("right_side_face"),
        translations["left_side_face"]: data.get("left_side_face")
    }

    progress_text = "\n".join(
        f"• {key}: {value}" 
        for key, value in fields.items() 
        if value is not None and value != ""
    )

    return progress_text

async def show_progress(state: FSMContext):
    data = await state.get_data()
    user_language = get_user_language(user_id=data.get("user_id"))

    # Получаем переводы для текущего языка, или используем английский по умолчанию
    translations = fields_translations.get(user_language)

    fields = {
        translations["name"]: data.get("name"),
        translations["country"]: data.get("country"),
        translations["email"]: data.get("email"),
        translations["age"]: data.get("age"),
        translations["gender"]: data.get("gender"),
        translations["skin_type"]: data.get("skin_type"),
        translations["skin_problems"]: ", ".join(data.get("skin_problems")) if data.get("skin_problems") else None,
        translations["skin_features"]: data.get("skin_features"),
        translations["lifestyles"]: ", ".join(data.get("lifestyles")) if data.get("lifestyles") else None,
        translations["water_intake"]: data.get("water_intake"),
        translations["daily_products"]: ", ".join(data.get("daily_products")) if data.get("daily_products") else None,
        translations["procedures_frequency"]: data.get("procedures_frequency"),
        translations["budget"]: data.get("budget"),
        translations["composition_prefs"]: ", ".join(data.get("composition_prefs")) if data.get("composition_prefs") else None,
        translations["full_face"]: data.get("full_face"),
        translations["right_side_face"]: data.get("right_side_face"),
        translations["left_side_face"]: data.get("left_side_face")
    }

    progress_text = "\n".join(
        f"• {key}: {value}" 
        for key, value in fields.items() 
        if value is not None and value != ""
    )

    return progress_text

def get_back_button(state: str, user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(user_id=user_id, key="back_button"), callback_data=f"back_{state}")
    return builder.as_markup()

def get_docx_file(data: dict, user_id: int, state_data) -> any:
    language = get_user_language(user_id=user_id)

    doc = DocxTemplate(f"templates/{language}_template.docx")
    context = { 
        'name' : state_data.get("name"),
        'introduction': data.get("Introduction"),
        'skin_condition_analysis': data.get("Skin Condition Analysis"),
        'lifestyle_impact_on_skin' : data.get("Lifestyle Impact on Skin"),
        'personal_skincare_recommendations': data.get("Personal Skincare Recommendations"),
        'improvement_forecast': data.get("Improvement Forecast"),
        'conclusion_and_support': data.get("Conclusion and Support")
    }
    # print(context)
    doc.render(context)
    doc.save(f"images/{user_id}/{get_text(user_id=user_id, key="report")}.docx") 

def get_text(user_id: int, key: str, **kwargs) -> str:
    lang = get_user_language(user_id=user_id)

    text = translations[lang].get(key, f"[{key}]")
    return text.format(**kwargs)

def get_inline_text(user_id: int, category: str, key: str) -> str:
    lang = get_user_language(user_id=user_id)

    return inline_translations[lang][category][key]