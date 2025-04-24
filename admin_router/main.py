from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from admin_router.service import handle_albums
from admin_router.states import Form
from config import Settings
from database.db import get_users

settings = Settings()

router = Router()
bot = Bot(token=settings.BOT_TOKEN)

def navigation_buttons():
    """Кнопки для отмены или возвращения назад."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться назад", callback_data="back")]
            # [InlineKeyboardButton(text="Отменить", callback_data="cancel")],
        ]
    )

@router.message(Command("admin"))
async def admin_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🇷🇺 Рассылка на русском", callback_data="ru_mailing")
    builder.button(text="🇬🇧 Рассылка на английском", callback_data="en_mailing")
    builder.button(text="🇩🇪 Рассылка на немецков", callback_data="de_mailing")
    builder.adjust(1)

    await message.answer("Выберите для какого языка нужна рассылка", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("ru_mailing"))
async def callback_ru_mailing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите текст для рассылки на русском языке")
    await callback.answer()

    await state.update_data(prev_message=callback.message.message_id)
    await state.set_state(Form.ru_mailing)

@router.message(Form.ru_mailing)
async def process_ru_text(message: types.Message, state: FSMContext):
    await state.update_data(mailing_text=message.text)
    await state.update_data(language="ru")

    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data="ru_yes")
    builder.button(text="Нет", callback_data="ru_no")
    await bot.edit_message_text(text="Добавить медиа файлы к рассылке?", chat_id=message.chat.id, message_id=message.message_id, reply_markup=builder.as_markup())

@router.callback_query(F.data == "ru_yes", Form.ru_mailing)
async def callback_ru_yes(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Отправьте фото/видео для рассылки")
    await callback.answer()

    await state.set_state(Form.ru_media)

@router.callback_query(F.data.startswith("en_mailing"))
async def callback_en_mailing(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(prev_message=callback.message.message_id)

    await callback.message.answer("Рассылка на английском языке")

@router.callback_query(F.data.startswith("de_mailing"))
async def callback_de_mailing(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(prev_message=callback.message.message_id)

    await callback.message.answer("Рассылка на немецком языке")

@router.message(F.content_type.in_([types.ContentType.VIDEO, types.ContentType.PHOTO]))
async def process_collect_videos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = await data.get("mailing_text")

    await message.delete()

    media_list = await handle_albums(message=message, text=f"{text}", data=data, state=state)

    if media_list:
        pass
    else:
        await message.answer("Размер одного из файлов превышает 20 МБ")
        return

@router.callback_query(F.data == "confirm")
async def confirm_publication(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_ids = data.get("prev_message")
    media_list = data.get("media")

    users = get_users(language=data.get("language"))

    if users:
        for user in users:
            await bot.send_media_group(chat_id=user.id, media=media_list)

    await callback.answer()

    await bot.delete_messages(chat_id=callback.from_user.id, message_ids=message_ids)
    await callback.message.edit_text(text="Рассылка успешно выполнена")

@router.callback_query(F.data == "edit")
async def edit_data(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_ids = data.get("prev_message")
    await bot.delete_messages(chat_id=callback.from_user.id, message_ids=message_ids)

    text = await data.get("mailing_text")
    await callback.message.edit_text(f"{text}\n\nПришлите фото/видео для рассылки", reply_markup=navigation_buttons())

    await state.update_data(prev_message=callback.message.message_id)

@router.callback_query(F.data == "back")
async def go_back(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    # Определяем, куда возвращать пользователя в зависимости от текущего состояния
    if current_state in [Form.ru_mailing, Form.de_mailing, Form.en_mailing]:
        builder = InlineKeyboardBuilder()
        builder.button(text="🇷🇺 Рассылка на русском", callback_data="ru_mailing")
        builder.button(text="🇬🇧 Рассылка на английском", callback_data="en_mailing")
        builder.button(text="🇩🇪 Рассылка на немецков", callback_data="de_mailing")
        builder.adjust(1)

        await state.clear()
        await callback.answer()
        await callback.message.edit_text("Выберите для какого языка нужна рассылка", reply_markup=builder.as_markup())
    
    elif current_state == Form.ru_media:
        await callback.message.edit_text("Введите текст для рассылки на русском языке")
        await callback.answer()

        await state.update_data(prev_message=callback.message.message_id)
        await state.update_data(mailing_text=None)
        await state.set_state(Form.ru_mailing)
    
    elif current_state == Form.en_media:
        await callback.message.edit_text("Введите текст для рассылки на английском языке")
        await callback.answer()

        await state.update_data(prev_message=callback.message.message_id)
        await state.update_data(mailing_text=None)
        await state.set_state(Form.en_mailing)

    elif current_state == Form.de_media:
        await callback.message.edit_text("Введите текст для рассылки на немецком языке")
        await callback.answer()

        await state.update_data(prev_message=callback.message.message_id)
        await state.update_data(mailing_text=None)
        await state.set_state(Form.de_mailing)