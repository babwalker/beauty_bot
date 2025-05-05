import os
from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

from user_router.utils.service import get_text, show_progress, get_back_button, get_inline_text
from user_router.utils.inline_buttons_data import AGES, BUDGET_OPTIONS, COMPOSITION_PREFERENCES, DAILY_PRODUCTS, GENDERS, PROCEDURES_FREQUENCY, SKIN_TYPES, SKIN_FEATURES, LIFESTYLES, WATER_OPTIONS, SKIN_PROBLEMS
from user_router.states import Form

router = Router()

@router.callback_query(F.data.startswith("back_"))
async def process_back(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    back_to = callback.data.split("_")[1:]
    if len(back_to) > 1:
        back_to = "_".join(back_to)
    else:
        back_to = back_to[0]
    await state.update_data(**{back_to: ""})
    progress = await show_progress(state)

    if back_to == "name":
        await callback.message.edit_text(get_text(user_id, "start_skin_analys"))
        await state.set_state(Form.name)

    elif back_to == "country":
        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'country_question')}",
            reply_markup=get_back_button("name", user_id=user_id)
        )
        await state.set_state(Form.country)

    # elif back_to == "email":
    #     await callback.message.edit_text(
    #         f"{progress}\n\n{get_text(user_id, 'email_question')}",
    #         reply_markup=get_back_button("country", user_id=user_id)
    #     )
    #     await state.set_state(Form.email)

    elif back_to == "age":
        builder = InlineKeyboardBuilder()
        for key in AGES:
            builder.button(text=get_inline_text(user_id, "AGES", key), callback_data=f"age_{key}")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_country")
        builder.adjust(2)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'age_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.age)

    elif back_to == "gender":
        builder = InlineKeyboardBuilder()
        for key in GENDERS:
            builder.button(text=get_inline_text(user_id, "GENDERS", key), callback_data=f"gender_{key}")
        builder.button(text=get_text(user_id, "other_button"), callback_data="other")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_age")
        builder.adjust(2)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'gender_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.gender)

    elif back_to == "skin_type":
        builder = InlineKeyboardBuilder()
        for key in SKIN_TYPES:
            builder.button(text=get_inline_text(user_id, "SKIN_TYPES", key), callback_data=f"skin_{key}")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_gender")
        builder.adjust(2)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'skin_type_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.skin_type)

    elif back_to == "skin_problems":
        await state.update_data(**{back_to: []})
        data = await state.get_data()
        selected_problems = data.get("skin_problems", [])
        builder = InlineKeyboardBuilder()

        for key in SKIN_PROBLEMS:
            button_text = get_inline_text(user_id, "SKIN_PROBLEMS", key)
            emoji = "✅" if button_text in selected_problems else "◻️"
            builder.button(text=f"{emoji} {button_text}", callback_data=f"problem_{key}")

        builder.button(text=get_text(user_id, "other_button"), callback_data="other")
        builder.button(text=get_text(user_id, "done_button"), callback_data="problems_done")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_skin_type")
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'skin_problems_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.skin_problems)

    elif back_to == "skin_features":
        builder = InlineKeyboardBuilder()
        for key in SKIN_FEATURES:
            builder.button(text=get_inline_text(user_id, "SKIN_FEATURES", key), callback_data=f"feature_{key}")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_skin_problems")
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'skin_features_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.skin_features)

    elif back_to == "lifestyles":
        await state.update_data(**{back_to: []})
        data = await state.get_data()
        selected_lifestyles = data.get("lifestyles", [])
        builder = InlineKeyboardBuilder()

        for key in LIFESTYLES:
            button_text = get_inline_text(user_id, "LIFESTYLES", key)
            emoji = "✅" if button_text in selected_lifestyles else "◻️"
            builder.button(text=f"{emoji} {button_text}", callback_data=f"lifestyle_{key}")

        builder.button(text=get_text(user_id, "done_button"), callback_data="lifestyle_done")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_skin_features")
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'lifestyle_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.lifestyle)

    elif back_to == "water_intake":
        builder = InlineKeyboardBuilder()
        for key in WATER_OPTIONS:
            builder.button(text=get_inline_text(user_id, "WATER_OPTIONS", key), callback_data=f"water_{key}")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_lifestyles")
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'water_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.water_intake)

    elif back_to == "daily_products":
        await state.update_data(**{back_to: []})
        data = await state.get_data()
        builder = InlineKeyboardBuilder()
        for key in DAILY_PRODUCTS:
            button_text = get_inline_text(user_id, "DAILY_PRODUCTS", key)
            emoji = "✅" if button_text in data.get("daily_products", []) else "◻️"
            builder.button(text=f"{emoji} {button_text}", callback_data=f"product_{key}")
        builder.button(text=get_text(callback.from_user.id, "other_button"), callback_data="other")
        builder.button(text=get_text(user_id, "done_button"), callback_data="products_done")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_water_intake")
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'products_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.daily_products)

    elif back_to == "procedures_frequency":
        builder = InlineKeyboardBuilder()
        for key in PROCEDURES_FREQUENCY:
            builder.button(text=get_inline_text(user_id, "PROCEDURES_FREQUENCY", key), callback_data=f"procedure_{key}")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_daily_products")
        builder.adjust(2)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'procedures_frequency_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.procedures_frequency)

    elif back_to == "budget":
        builder = InlineKeyboardBuilder()
        for key in BUDGET_OPTIONS:
            builder.button(text=get_inline_text(user_id, "BUDGET_OPTIONS", key), callback_data=f"budget_{key}")
        builder.button(text=get_text(user_id, "back_button"), callback_data="back_procedures_frequency")
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'budget_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.budget)

    elif back_to == "composition":
        builder = InlineKeyboardBuilder()
        data = await state.get_data()
        selected_prefs = data.get("composition_prefs", [])
        for key in COMPOSITION_PREFERENCES:
            emoji = "✅" if get_inline_text(user_id, "COMPOSITION_PREFERENCES", key) in selected_prefs else "◻️"
            builder.button(
                text=f"{emoji} {get_inline_text(user_id, 'COMPOSITION_PREFERENCES', key)}",
                callback_data=f"composition_{key}"
            )
        builder.button(
            text=get_text(user_id, "done_button"),
            callback_data="done_composition"
        )
        builder.button(
            text=get_text(user_id, "back_button"),
            callback_data="back_budget"
        )
        builder.adjust(1)

        await callback.message.edit_text(
            f"{progress}\n\n{get_text(user_id, 'composition_question')}",
            reply_markup=builder.as_markup()
        )
        await state.set_state(Form.composition_preferences)

    elif back_to == "photo_full_face":
        data = await state.get_data()
        if os.path.exists(f"images/{callback.from_user.id}/{data.get('photo_full_face_id')}.jpg"):
            os.remove(f"images/{callback.from_user.id}/{data.get("photo_full_face_id")}.jpg")
        await state.update_data(full_face=None)
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

    elif back_to == "photo_right_profile_face":
        data = await state.get_data()
        if os.path.exists(f"images/{callback.from_user.id}/{data.get('photo_right_profile_face_id')}.jpg"):
            os.remove(f"images/{callback.from_user.id}/{data.get("photo_right_profile_face_id")}.jpg")
        await state.update_data(right_side_face=None)
        progress = await show_progress(state)

        builder = InlineKeyboardBuilder()
        builder.button(
            text=get_text(callback.from_user.id, "back_button"),
            callback_data="back_photo_full_face"
        )
        
        response = (
            f"{progress}\n\n"
            f"{get_text(callback.from_user.id, 'upload_right_profile_photo')}"
        )
        
        await callback.message.edit_text(response, reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
        await state.set_state(Form.photo_right_profile_face)
        await callback.answer()
