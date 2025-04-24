import asyncio

from aiogram.types import Message
from aiogram import Bot
from aiogram.types import Message, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from aiogram.types.input_media_video import InputMediaVideo
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import Settings

settings = Settings()

bot = Bot(token=settings.BOT_TOKEN) 

send_indicator = 0

media_list = []

message_ids = []

async def handle_only_one_message(count, chat_id, prev_message, state):
    global send_indicator
    global media_list
    global message_ids

    if count == 1:
        await asyncio.sleep(1)
        send_indicator = 0

        buttons = [
            [InlineKeyboardButton(text="Все верно", callback_data="confirm")],
            [InlineKeyboardButton(text="Изменить", callback_data="edit")],
        ]

        if len(message_ids) > 1:
            delete_message_ids = ([id for id in range((message_ids[-1]+1), message_ids[-1]+1+len(message_ids))])
        else:
            delete_message_ids = ([message_ids[0]+1])

        await bot.delete_message(chat_id=chat_id, message_id=prev_message)
        await state.update_data(prev_message=delete_message_ids)

        print(delete_message_ids)

        if len(media_list) > 1:
            for i in range(1, len(media_list)): # делаем так чтобы только у одного элемента осталось caption
                media_list[i].caption = None 
        await state.update_data(media=media_list)
        
        await bot.send_media_group(
            chat_id=chat_id, 
            media=media_list,
        )
        await bot.send_message(
            chat_id=chat_id,
            text="Правильно ли все указано?",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        )
        media_list = []
        return True
    else:
        pass

async def handle_albums(message: Message, text, data, state):
    global send_indicator
    global media_list
    global message_ids

    try:
        if message.video:
            file_id = message.video.file_id
            media_list.append(InputMediaVideo(media=file_id, caption=text))
        elif message.photo:
            file_id = message.photo[-1].file_id
            media_list.append(InputMediaPhoto(media=file_id, caption=text))

        send_indicator += 1

        message_ids.append(message.message_id)

        time_message = await handle_only_one_message(
            count=send_indicator, 
            chat_id=message.chat.id, 
            prev_message=data.get("prev_message", None), 
            state=state)
        if time_message:
            return True
        else:
            return "blank for correct return"
        
    except TelegramBadRequest as e:
        print(e)
        return False
