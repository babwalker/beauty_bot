import asyncio
import logging
import os
import random
import shutil
from aiogram import Bot, types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InputMediaVideo, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from aiogram.enums import ParseMode

import re

from config import Settings
from database.db import change_user_language, create_user, get_user_language
from user_router.states import Form
from user_router.utils.service import get_docx_file, get_inline_text, get_text, show_progress, get_back_button
from user_router.utils.inline_buttons_data import BUDGET_OPTIONS, COMPOSITION_PREFERENCES, DAILY_PRODUCTS, PROCEDURES_FREQUENCY, SKIN_FEATURES, LIFESTYLES, WATER_OPTIONS, AGES, GENDERS, SKIN_TYPES, SKIN_PROBLEMS
from user_router.utils.ai_service import analysis_image, get_summary_report

settings = Settings()

bot = Bot(token=settings.BOT_TOKEN)

router = Router()

@router.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    language = callback.data.split("_")[2] 
    change_user_language(user_id=callback.from_user.id, language=language)

    language_list = {
        "ru": "🇷🇺 Русский", 
        "en": "🇬🇧 English", 
        "de": "🇩🇪 Deutsch"
    }
    user_language = get_user_language(user_id=callback.from_user.id)

    builder = InlineKeyboardBuilder()

    builder.button(
        text=get_inline_text(callback.from_user.id, "START_BUTTON", "skin_analys"),
        callback_data="start"
    )

    for language in language_list.keys():
        if user_language != language:
            builder.row(
                InlineKeyboardButton(
                    text=f"{language_list[language]}",
                    callback_data=f"set_lang_{language}"
                )
            )
    builder.adjust(1)

    await state.clear()
    await callback.message.edit_caption(caption=get_text(callback.from_user.id, "start"), reply_markup=builder.as_markup())

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    create_user(user_id=message.from_user.id)
    language_list = {
        "ru": "🇷🇺 Русский", 
        "en": "🇬🇧 English", 
        "de": "🇩🇪 Deutsch"
    }
    user_language = get_user_language(user_id=message.from_user.id)

    builder = InlineKeyboardBuilder()

    builder.button(
        text=get_inline_text(message.from_user.id, "START_BUTTON", "skin_analys"),
        callback_data="start"
    )

    for language in language_list.keys():
        if user_language != language:
            builder.row(
                InlineKeyboardButton(
                    text=f"{language_list[language]}",
                    callback_data=f"set_lang_{language}"
                )
            )
    builder.adjust(1)

    await state.clear()
    await message.delete()
    await message.answer_video(
        video="BAACAgIAAxkBAAIgm2gZ_b0ln0HIwLZbJUiusB46kMkXAAJscgACHyDQSJlB-lUffNPsNgQ", 
        caption=get_text(message.from_user.id, "start"),
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == "start")
async def process_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(get_text(user_id=callback.from_user.id, key="start_skin_analys"))
    await state.set_state(Form.name)
    await state.update_data(user_id=callback.from_user.id)
    logging.info(f"process_start - {callback.message.message_id}")
    logging.info(callback.message.from_user.id)

    await callback.answer()

@router.message(Form.name)
async def process_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get("prev_message"):
        logging.info(f"process_name if true: {data.get('prev_message')}")
        pass
    else:
        await state.update_data(prev_message=message.message_id-1)
        data = await state.get_data()
        logging.info(f"process_name if false: {data.get('prev_message')}")
    logging.info(message.from_user.id)
    message_id = data.get("prev_message")

    if len(message.text) < 2:
        await message.answer(get_text(message.from_user.id, "name_error"))
        await asyncio.sleep(3)
        await message.delete()
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)
        return
    
    await state.update_data(name=message.text)
    progress = await show_progress(state)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=f"{progress}\n\n{get_text(message.from_user.id, 'country_question')}",
        reply_markup=get_back_button("name", user_id=message.from_user.id)
    )
    await message.delete()
    await state.set_state(Form.country)

# Country handler
@router.message(Form.country)
async def process_country(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("prev_message")
    
    await state.update_data(country=message.text)
    progress = await show_progress(state)

    builder = InlineKeyboardBuilder()
    for key in AGES:
        text = get_inline_text(message.from_user.id, "AGES", key)
        builder.button(text=text, callback_data=f"age_{key}")
    builder.button(text=get_text(message.from_user.id, "back_button"), callback_data="back_country")
    builder.adjust(2)

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message_id,
        text=f"{progress}\n\n{get_text(message.from_user.id, 'age_question')}",
        reply_markup=builder.as_markup()
    )
    await message.delete()
    await state.set_state(Form.age)

# @router.message(Form.email)
# async def process_email(message: types.Message, state: FSMContext):
#     # if not re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
#     #     await message.answer(get_text(message.from_user.id, "email_validation"))
#     #     await asyncio.sleep(3)
#     #     await message.delete()
#     #     await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)
#     #     return
    
#     data = await state.get_data()
#     message_id = data.get("prev_message")

#     await state.update_data(email=message.text)
#     progress = await show_progress(state)

#     builder = InlineKeyboardBuilder()
#     for key in AGES:
#         text = get_inline_text(message.from_user.id, "AGES", key)
#         builder.button(text=text, callback_data=f"age_{key}")
#     builder.button(text=get_text(message.from_user.id, "back_button"), callback_data="back_email")
#     builder.adjust(2)

#     await bot.edit_message_text(
#         chat_id=message.chat.id,
#         message_id=message_id,
#         text=f"{progress}\n\n{get_text(message.from_user.id, 'age_question')}",
#         reply_markup=builder.as_markup()
#     )
#     await message.delete()
#     await state.set_state(Form.age)


@router.callback_query(F.data.startswith("age_"))
async def process_age_callback(callback: types.CallbackQuery, state: FSMContext):
    age = callback.data.split("_")[1]
    await state.update_data(age=get_inline_text(callback.from_user.id, "AGES", age))
    progress = await show_progress(state)

    builder = InlineKeyboardBuilder()
    for key in GENDERS:
        text = get_inline_text(callback.from_user.id, "GENDERS", key)
        builder.button(text=text, callback_data=f"gender_{key}")
    builder.button(text=get_text(callback.from_user.id, "other_button"), callback_data="other")
    builder.button(text=get_text(callback.from_user.id, "back_button"), callback_data="back_age")
    builder.adjust(2)

    await callback.message.edit_text(
        f"{progress}\n\n{get_text(callback.from_user.id, 'gender_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.gender)
    await callback.answer()

@router.callback_query(F.data.startswith("gender_"))
async def process_gender_callback(callback: types.CallbackQuery, state: FSMContext):
    gender_key = callback.data.split("_")[1]
    await state.update_data(gender=get_inline_text(callback.from_user.id, "GENDERS", gender_key))
    progress = await show_progress(state)

    builder = InlineKeyboardBuilder()
    for key in SKIN_TYPES:
        text = get_inline_text(callback.from_user.id, "SKIN_TYPES", key)
        builder.button(text=text, callback_data=f"skin_{key}")
    builder.button(text=get_text(callback.from_user.id, "back_button"), callback_data="back_gender")
    builder.adjust(2)

    await callback.message.edit_text(
        f"{progress}\n\n{get_text(callback.from_user.id, 'skin_type_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.skin_type)
    await callback.answer()

@router.callback_query(F.data.startswith("skin_"))
async def process_skin_callback(callback: types.CallbackQuery, state: FSMContext):
    skin_key = callback.data.split("_")[1]
    data = await state.update_data(skin_type=get_inline_text(callback.from_user.id, 'SKIN_TYPES', skin_key))
    progress = await show_progress(state)

    selected_problems = data.get("skin_problems", [])
    user_id = callback.from_user.id

    response_text = f"{progress}\n\n{get_text(user_id, 'skin_problems_question')}"
    builder = InlineKeyboardBuilder()

    for key in SKIN_PROBLEMS:
        emoji = "✅" if get_inline_text(callback.from_user.id, "SKIN_PROBLEMS", key) in selected_problems else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(callback.from_user.id, 'SKIN_PROBLEMS', key)}",
            callback_data=f"problem_{key}"
        )

    builder.button(text=get_text(user_id, "other_button"), callback_data="other")
    builder.button(text=get_text(user_id, "done_button"), callback_data="problems_done")
    builder.button(text=get_text(user_id, "back_button"), callback_data="back_skin_type")
    builder.adjust(1)

    await callback.message.edit_text(response_text, reply_markup=builder.as_markup())
    await state.set_state(Form.skin_problems)
    await callback.answer()

@router.callback_query(F.data.startswith("problem_"), Form.skin_problems)
async def select_skin_problems(callback: types.CallbackQuery, state: FSMContext):
    problem_key = callback.data.split("_")[1]
    user_id = callback.from_user.id
    problem_text = get_inline_text(user_id, "SKIN_PROBLEMS", problem_key)

    data = await state.get_data()
    selected_problems = data.get("skin_problems", [])

    if problem_text in selected_problems:
        selected_problems.remove(problem_text)
    else:
        if len(selected_problems) >= 3:
            await callback.answer(get_text(user_id, "max_amount_warning"), show_alert=True)
            return
        selected_problems.append(problem_text)

    await state.update_data(skin_problems=selected_problems)
    progress = await show_progress(state)

    builder = InlineKeyboardBuilder()
    for key in SKIN_PROBLEMS:
        emoji = "✅" if get_inline_text(callback.from_user.id, "SKIN_PROBLEMS", key) in selected_problems else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(callback.from_user.id, 'SKIN_PROBLEMS', key)}",
            callback_data=f"problem_{key}"
        )

    builder.button(text=get_text(user_id, "other_button"), callback_data="other")
    builder.button(text=get_text(user_id, "done_button"), callback_data="problems_done")
    builder.button(text=get_text(user_id, "back_button"), callback_data="back_skin_type")
    builder.adjust(1)

    try:
        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'skin_problems_question')}",
            reply_markup=builder.as_markup()
        )
    except:
        pass

    await callback.answer()

@router.callback_query(F.data == "problems_done", Form.skin_problems)
async def process_problems_done(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()

    if not data.get("skin_problems"):
        await callback.answer(get_text(user_id, "min_amount_warning"), show_alert=True)
        return

    progress = await show_progress(state)
    builder = InlineKeyboardBuilder()

    for key in SKIN_FEATURES:
        builder.button(
            text=get_inline_text(callback.from_user.id, "SKIN_FEATURES", key),
            callback_data=f"feature_{key}"
        )

    builder.button(
        text=get_text(user_id, "back_button"), 
        callback_data="back_skin_problems"
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"{progress}\n\n{get_text(user_id, 'skin_features_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.skin_features)
    await callback.answer()

@router.callback_query(F.data.startswith("feature_"), Form.skin_features)
async def process_skin_feature(callback: types.CallbackQuery, state: FSMContext):
    feature_key = callback.data.split("_")[1]
    user_id = callback.from_user.id
    await state.update_data(skin_features=get_inline_text(user_id, "SKIN_FEATURES", feature_key))
    progress = await show_progress(state)

    selected = (await state.get_data()).get("lifestyles", [])
    builder = InlineKeyboardBuilder()

    for key in LIFESTYLES:
        emoji = "✅" if get_inline_text(callback.from_user.id, "LIFESTYLES", key) in selected else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(callback.from_user.id, 'LIFESTYLES', key)}",
            callback_data=f"lifestyle_{key}"
        )

    builder.button(
        text=get_text(user_id, "done_button"), 
        callback_data="lifestyle_done"
    )
    builder.button(
        text=get_text(user_id, "back_button"), 
        callback_data="back_skin_features"
    )
    builder.adjust(1)

    await callback.message.edit_text(
        f"{progress}\n\n{get_text(user_id, 'lifestyle_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.lifestyle)
    await callback.answer()

@router.callback_query(F.data.startswith("lifestyle_"), Form.lifestyle)
async def process_lifestyle(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    data = await state.get_data()
    selected = data.get("lifestyles", [])

    if action == "done":
        if not selected:
            await callback.answer(
                get_text(callback.from_user.id, "min_amount_warning"),
                show_alert=True
            )
            return

        progress = await show_progress(state)

        builder = InlineKeyboardBuilder()
        for key in WATER_OPTIONS:
            builder.button(
                text=get_inline_text(callback.from_user.id, "WATER_OPTIONS", key),
                callback_data=f"water_{key}"
            )
        builder.button(
            text=get_text(callback.from_user.id, "back_button"),
            callback_data="back_lifestyles"
        )
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(callback.from_user.id, 'water_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.water_intake)
    else:
        lifestyle_value = get_inline_text(callback.from_user.id, "LIFESTYLES", action)
        if lifestyle_value in selected:
            selected.remove(lifestyle_value)
        else:
            if len(selected) >= 3:
                await callback.answer(
                    get_text(callback.from_user.id, "max_amount_warning"),
                    show_alert=True
                )
                return
            selected.append(lifestyle_value)

        await state.update_data(lifestyles=selected)
        await update_lifestyle_keyboard(callback.message, state, selected)

    await callback.answer()

async def update_lifestyle_keyboard(message: types.Message, state: FSMContext, selected: list):
    progress = await show_progress(state)
    builder = InlineKeyboardBuilder()
    for key in LIFESTYLES:
        emoji = "✅" if get_inline_text(message.chat.id, "LIFESTYLES", key) in selected else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(message.chat.id, 'LIFESTYLES', key)}",
            callback_data=f"lifestyle_{key}"
        )
    
    builder.button(
        text=get_text(message.chat.id, "done_button"), 
        callback_data="lifestyle_done"
    )
    builder.button(
        text=get_text(message.chat.id, "back_button"), 
        callback_data="back_skin_features"
    )
    builder.adjust(1)
    
    await message.edit_text(
        f"{progress}\n\n{get_text(message.chat.id, 'lifestyle_question')}",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data.startswith("water_"), Form.water_intake)
async def process_water(callback: types.CallbackQuery, state: FSMContext):
    water_key = callback.data.split("_")[1]
    await state.update_data(water_intake=get_inline_text(callback.from_user.id, "WATER_OPTIONS", water_key))

    progress = await show_progress(state)
    data = await state.get_data()
    selected_products = data.get("daily_products", [])
    
    builder = InlineKeyboardBuilder()
    for key in DAILY_PRODUCTS:
        emoji = "✅" if get_inline_text(callback.from_user.id, "DAILY_PRODUCTS", key) in selected_products else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(callback.from_user.id, 'DAILY_PRODUCTS', key)}",
            callback_data=f"product_{key}"
        )

    builder.button(
        text=get_text(callback.from_user.id, "other_button"), 
        callback_data="other"
    )
    builder.button(
        text=get_text(callback.from_user.id, "done_button"), 
        callback_data="products_done"
    )
    builder.button(
        text=get_text(callback.from_user.id, "back_button"), 
        callback_data="back_water_intake"
    )
    builder.adjust(1)
    
    await callback.message.edit_text(
        f"{progress}\n\n{get_text(callback.from_user.id, 'products_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.daily_products)
    await callback.answer()

@router.callback_query(F.data.startswith("product_"), Form.daily_products)
async def process_products(callback: types.CallbackQuery, state: FSMContext):
    product_key = callback.data.split("_")[1]
    data = await state.get_data()
    selected_products = data.get("daily_products", [])
    
    product_text = get_inline_text(callback.from_user.id, "DAILY_PRODUCTS", product_key)
    
    if product_text in selected_products:
        selected_products.remove(product_text)
    else:
        selected_products.append(product_text)
    
    await state.update_data(daily_products=selected_products)
    await update_products_keyboard(callback.message, state)
    await callback.answer()

async def update_products_keyboard(message: types.Message, state: FSMContext):
    progress = await show_progress(state)
    data = await state.get_data()
    selected_products = data.get("daily_products", [])
    
    builder = InlineKeyboardBuilder()
    for key in DAILY_PRODUCTS:
        emoji = "✅" if get_inline_text(message.chat.id, "DAILY_PRODUCTS", key) in selected_products else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(message.chat.id, 'DAILY_PRODUCTS', key)}",
            callback_data=f"product_{key}"
        )
    
    builder.button(
        text=get_text(message.chat.id, "other_button"), 
        callback_data="other"
    )
    builder.button(
        text=get_text(message.chat.id, "done_button"), 
        callback_data="products_done"
    )
    builder.button(
        text=get_text(message.chat.id, "back_button"), 
        callback_data="back_water_intake"
    )
    builder.adjust(1)
    
    await message.edit_text(
        f"{progress}\n\n{get_text(message.chat.id, 'products_question')}",
        reply_markup=builder.as_markup()
    )

# Обработчик завершения выбора продуктов
@router.callback_query(F.data == "products_done", Form.daily_products)
async def process_products_done(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("daily_products", []):
        await callback.answer(get_text(callback.from_user.id, "min_amount_warning"), show_alert=True)
        return

    progress = await show_progress(state)
    
    builder = InlineKeyboardBuilder()
    for key in PROCEDURES_FREQUENCY:
        builder.button(
            text=get_inline_text(callback.from_user.id, "PROCEDURES_FREQUENCY", key),
            callback_data=f"procedure_{key}"
        )
    builder.button(
        text=get_text(callback.from_user.id, "back_button"),
        callback_data="back_daily_products"
    )
    builder.adjust(2)
    
    await callback.message.edit_text(
        f"{progress}\n\n{get_text(callback.from_user.id, 'procedures_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.procedures_frequency)
    await callback.answer()

# Обработчик выбора частоты процедур
@router.callback_query(F.data.startswith("procedure_"), Form.procedures_frequency)
async def process_procedures(callback: types.CallbackQuery, state: FSMContext):
    freq_key = callback.data.split("_")[1]
    await state.update_data(procedures_frequency=get_inline_text(callback.from_user.id, "PROCEDURES_FREQUENCY", freq_key))  

    progress = await show_progress(state)
    
    builder = InlineKeyboardBuilder()
    for key in BUDGET_OPTIONS:
        builder.button(
            text=get_inline_text(callback.from_user.id, "BUDGET_OPTIONS", key),
            callback_data=f"budget_{key}"
        )

    builder.button (
        text=get_text(callback.from_user.id, "back_button"),
        callback_data="back_procedures_frequency"
    )
    builder.adjust(1)
    
    await callback.message.edit_text(
        f"{progress}\n\n{get_text(callback.from_user.id, 'budget_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.budget)
    await callback.answer()

# Обработчик выбора бюджета
@router.callback_query(F.data.startswith("budget_"), Form.budget)
async def process_budget(callback: types.CallbackQuery, state: FSMContext):
    budget_key = callback.data.split("_")[1]
    await state.update_data(budget=get_inline_text(callback.from_user.id, "BUDGET_OPTIONS", budget_key))
    progress = await show_progress(state)
    data = await state.get_data()
    selected_prefs = data.get("composition_prefs", [])
    
    builder = InlineKeyboardBuilder()
    for key in COMPOSITION_PREFERENCES:
        if key == "no-preference": continue
        emoji = "✅" if get_inline_text(callback.from_user.id, "COMPOSITION_PREFERENCES", key) in selected_prefs else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(callback.from_user.id, 'COMPOSITION_PREFERENCES', key)}",
            callback_data=f"composition_{key}"
        )
    
    builder.button(
        text=get_inline_text(callback.message.chat.id, "COMPOSITION_PREFERENCES", "no-preference"),
        callback_data="no_preferenece"
    )
    builder.button(
        text=get_text(callback.from_user.id, "done_button"),
        callback_data="done_composition"
    )
    builder.button(
        text=get_text(callback.from_user.id, "back_button"),
        callback_data="back_budget"
    )
    builder.adjust(1)
    
    await callback.message.edit_text(
        f"{progress}\n\n{get_text(callback.from_user.id, 'composition_question')}",
        reply_markup=builder.as_markup()
    )
    await state.set_state(Form.composition_preferences)
    await callback.answer()

# Обработчик выбора предпочтений по составу
@router.callback_query(F.data.startswith("composition_"), Form.composition_preferences)
async def process_composition(callback: types.CallbackQuery, state: FSMContext):
    pref_key = callback.data.split("_")[1]
    data = await state.get_data()
    selected_prefs = data.get("composition_prefs", [])
    
    pref_text = get_inline_text(callback.from_user.id, "COMPOSITION_PREFERENCES", pref_key)
    
    if pref_text in selected_prefs:
        selected_prefs.remove(pref_text)
    else:
        selected_prefs.append(pref_text)
    
    await state.update_data(composition_prefs=selected_prefs)
    await update_composition_keyboard(callback.message, state)
    await callback.answer()

async def update_composition_keyboard(message: types.Message, state: FSMContext):
    progress = await show_progress(state)
    data = await state.get_data()
    selected_prefs = data.get("composition_prefs", [])
    
    builder = InlineKeyboardBuilder()
    for key in COMPOSITION_PREFERENCES:
        if key == "no-preference": continue
        emoji = "✅" if get_inline_text(message.chat.id, "COMPOSITION_PREFERENCES", key) in selected_prefs else "◻️"
        builder.button(
            text=f"{emoji} {get_inline_text(message.chat.id, 'COMPOSITION_PREFERENCES', key)}",
            callback_data=f"composition_{key}"
        )

    builder.button(
        text=get_inline_text(message.chat.id, "COMPOSITION_PREFERENCES", "no-preference"),
        callback_data="no_preferenece"
    )
    
    builder.button(
        text=get_text(message.chat.id, "done_button"),
        callback_data="done_composition"
    )
    builder.button(
        text=get_text(message.chat.id, "back_button"),
        callback_data="back_budget"
    )
    builder.adjust(1)
    
    await message.edit_text(
        f"{progress}\n\n{get_text(message.chat.id, 'composition_question')}",
        reply_markup=builder.as_markup()
    )

#Обработчик выбора косметики без предпочтений
@router.callback_query(F.data == "no_preferenece", Form.composition_preferences)
async def process_no_preference(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(composition_prefs=[])
    await state.update_data(composition_prefs=get_inline_text(callback.from_user.id, "COMPOSITION_PREFERENCES", "no-preference"))

    progress = await show_progress(state)

    builder = InlineKeyboardBuilder()
    builder.button(
        text=get_text(callback.from_user.id, "back_button"),
        callback_data="back_composition"
    )
    
    response = (
        f"{progress}\n\n"
        f"{get_text(callback.from_user.id, 'upload_full_face_photo')}"
    )
    
    await callback.message.edit_text(response, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
    await state.set_state(Form.photo_full_face)
    await callback.answer()

# Обработчик завершения выбора состава
@router.callback_query(F.data == "done_composition", Form.composition_preferences)
async def process_composition_done(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("composition_prefs", []):
        await callback.answer(get_text(callback.from_user.id, "min_amount_warning"), show_alert=True)
        return    

    progress = await show_progress(state)

    builder = InlineKeyboardBuilder()
    builder.button(
        text=get_text(callback.from_user.id, "back_button"),
        callback_data="back_composition"
    )
    
    response = (
        f"{progress}\n\n"
        f"{get_text(callback.from_user.id, 'upload_full_face_photo')}"
    )
    
    await callback.message.edit_text(response, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
    await state.set_state(Form.photo_full_face)
    await callback.answer()

@router.message(Command("test"))
async def test(message: types.Message, state: FSMContext):
    await message.answer("test")
    await state.set_state(Form.photo_full_face)

@router.message(F.content_type == types.ContentType.PHOTO, Form.photo_full_face)
async def process_photo_full_face(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Перечитываем обновленные данные
    if data.get("error_message"):
        await message.delete(data.get("error_message"))
        await state.update_data(error_message=None)
    if "image_count" not in data:
        await state.update_data(image_count=0)
        data = await state.get_data()
    
    # Увеличиваем счетчик и сохраняем
    new_count = data["image_count"] + 1
    await state.update_data(image_count=new_count)
    await message.delete()
    if data.get("image_count") > 0:
        return

    await message.answer(text=get_text(message.from_user.id, "processing_photo"))

    builder = InlineKeyboardBuilder()
    builder.button(
        text=get_text(message.from_user.id, "back_button"),
        callback_data="back_photo_full_face"
    )

    file_id = message.photo[-1].file_id
    file_name = random.randint(100000, 1000000)
    file_path = f"images/{message.from_user.id}/{file_name}.jpg"

    # Создаем папку если не существует
    os.makedirs(f"images/{message.from_user.id}", exist_ok=True)

    await bot.download(file=file_id, destination=file_path)
    response = analysis_image(image_path=file_path)
    await state.update_data(photo_full_face_id=file_name)
    data = await state.get_data()
    prev_message = data.get("prev_message")

    if response["face"] == True:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")))
        await state.update_data(full_face=get_text(message.from_user.id, "full_face"))
        progress = await show_progress(state)
        await bot.edit_message_text(
            message_id=prev_message,
            chat_id=message.chat.id,
            text=(
                f"{progress}\n\n"
                f"{get_text(message.from_user.id, 'upload_right_profile_photo')}"
            ),
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.HTML
        )
        await state.update_data(image_count=0)
        await state.set_state(Form.photo_right_profile_face)
        await message.answer("✅")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")) + 1)
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")))
        await message.answer(get_text(message.from_user.id, "no_face_error"))
        os.remove(f"images/{message.from_user.id}/{file_name}.jpg")
        await state.update_data(error_message=message.message_id + int(data.get("image_count")) + 1)
        await state.update_data(image_count=0)

@router.message(F.content_type == types.ContentType.PHOTO, Form.photo_right_profile_face)
async def process_photo_right_profile_face(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Перечитываем обновленные данные
    if data.get("error_message"):
        await message.delete(data.get("error_message"))
        await state.update_data(error_message=None)
    if "image_count" not in data:
        await state.update_data(image_count=0)
        data = await state.get_data()
    
    # Увеличиваем счетчик и сохраняем
    new_count = data["image_count"] + 1
    await state.update_data(image_count=new_count)
    await message.delete()
    if data["image_count"] > 0:
        return
    
    await message.answer(text=get_text(message.from_user.id, "processing_photo"))
    data = await state.get_data()
    prev_message = data.get("prev_message")

    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(message.from_user.id, "back_button"), callback_data="back_photo_right_profile_face")
    file_id = message.photo[-1].file_id
    file_name = random.randint(100000, 1000000)
    file_path = f"images/{message.from_user.id}/{file_name}.jpg"

    await bot.download(file=file_id, destination=file_path)
    response = analysis_image(image_path=file_path)
    await state.update_data(photo_right_profile_face_id=file_name)

    if response["face"] == True:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")))
        await state.update_data(right_side_face = get_text(message.from_user.id, "full_face"))
        progress = await show_progress(state)
        await bot.edit_message_text(
            message_id=prev_message,
            chat_id=message.chat.id,
            text=f"{progress}\n\n{get_text(message.from_user.id, "upload_left_profile_photo")}",
            reply_markup=builder.as_markup(),
            parse_mode=ParseMode.HTML
        )
        await state.update_data(image_count=0)
        await state.set_state(Form.photo_left_side_face)
        await message.answer("✅")
        await asyncio.sleep(2)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")) + 1)
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")))
        await message.answer(get_text(message.from_user.id, "no_face_error"))
        os.remove(f"images/{message.from_user.id}/{file_name}.jpg")
        await state.update_data(error_message=message.message_id + int(data.get("image_count")) + 1)
        await state.update_data(image_count=0)

@router.message(F.content_type == types.ContentType.PHOTO, Form.photo_left_side_face)
async def process_photo_left_side_face(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Перечитываем обновленные данные
    if data.get("error_message"):
        await message.delete(data.get("error_message"))
        await state.update_data(error_message=None)
    if "image_count" not in data:
        await state.update_data(image_count=0)
        data = await state.get_data()
    
    # Увеличиваем счетчик и сохраняем
    new_count = data["image_count"] + 1
    await state.update_data(image_count=new_count)
    await message.delete()
    if data["image_count"] > 0:
        return
    
    await message.answer(text=get_text(message.from_user.id, "processing_photo"))
    data = await state.get_data()
    prev_message = data.get("prev_message")

    builder = InlineKeyboardBuilder()
    builder.button(text=get_text(message.from_user.id, "back_button"), callback_data="back_full_face")

    file_id = message.photo[-1].file_id
    file_name = random.randint(100000, 1000000)
    file_path = f"images/{message.from_user.id}/{file_name}.jpg"

    await bot.download(file=file_id, destination=file_path)
    response = analysis_image(image_path=file_path)

    if response["face"] == True:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")))
        await message.answer(text=get_text(message.from_user.id, key="processing_care_program"))
        await state.update_data(left_side_face = get_text(message.from_user.id, "full_face"))
        data = await state.get_data()
        progress = await show_progress(state)
        
        response = (
            # f"{progress}\n\n"
            get_text(message.from_user.id, "final_report_message")
        )
        
        builder = InlineKeyboardBuilder()
        builder.button(text=get_inline_text(user_id=message.from_user.id, category="FINAL_REPORT", key="our_courses"), url="https://bwa-akademy.online/courses")
        builder.button(text=get_inline_text(user_id=message.from_user.id, category="FINAL_REPORT", key="master_certification"), url="https://bwa-akademy.online/zertifizierung_offiziell/")
        builder.button(text=get_inline_text(user_id=message.from_user.id, category="FINAL_REPORT", key="trainer_certification"), url="https://bwa-akademy.online/zertifizierung_offiziell/")
        builder.button(text=get_inline_text(user_id=message.from_user.id, category="FINAL_REPORT", key="our_instagram"), url="https://www.instagram.com/beauty.akademy.world/")
        builder.adjust(1)

        summary_report = get_summary_report(message.from_user.id, data)
        if summary_report:
            get_docx_file(data=summary_report, user_id=message.from_user.id, state_data=data)
        else:
            while True:
                summary_report = get_summary_report(message.from_user.id, data)
                if summary_report:
                    get_docx_file(data=summary_report, user_id=message.from_user.id, state_data=data)
                    break
                else:
                    await asyncio.sleep(60)
        document = FSInputFile(path=f"images/{message.from_user.id}/{get_text(user_id=message.from_user.id, key="report")}.pdf")

        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")) + 1)

        await bot.edit_message_text(
            message_id=prev_message,
            chat_id=message.chat.id,
            text=response,
            reply_markup=builder.as_markup()
        )
        await bot.send_document(chat_id=message.chat.id, document=document)

        shutil.rmtree(f"images/{message.from_user.id}")
        await state.clear()
        await asyncio.sleep(60)
        await message.answer(get_text(message.from_user.id, "final_message"))
        # await state.set_state(Form.photo_right_profile_face)
    else:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + int(data.get("image_count")))
        await message.answer(get_text(message.from_user.id, "no_face_error"))
        os.remove(f"images/{message.from_user.id}/{file_name}.jpg")
        await state.update_data(error_message=message.message_id + int(data.get("image_count")) + 1)
        await state.update_data(image_count=0)

@router.message()
async def other_message(message: types.Message, state: FSMContext):
    await message.answer(get_text(message.from_user.id, "other_message"))
    await asyncio.sleep(5)
    await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)