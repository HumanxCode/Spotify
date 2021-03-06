from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice
from pytgcalls.types.input_stream import InputAudioStream
from Client import callsmusic, queues

import converter
from youtube import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, QUE_IMG, GROUP_SUPPORT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ACTV_CALLS = []

@Client.on_message(command("audio") & other_filters)
@errors
async def stream(_, message: Message):
    chat_id = message.chat.id

    lel = await message.reply("๐ **๐ฉ๐ซ๐จ๐๐๐ฌ๐ฌ๐ข๐ง๐ ** ๐ฌ๐จ๐ฎ๐ง๐...")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="โจ ษขสแดแดแด",
                        url=f"https://t.me/SpotifySupport_id"),
                    InlineKeyboardButton(
                        text="๐ป แดสแดษดษดแดส",
                        url=f"https://t.me/SpotifyBotProject")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"๐๐ข๐๐๐จ๐ฌ ๐ฅ๐จ๐ง๐ ๐๐ซ ๐ญ๐ก๐๐ง {DURATION_LIMIT} ๐ฆ๐ข๐ง๐ฎ๐ญ๐(๐ฌ) ๐๐ซ๐๐ง'๐ญ ๐๐ฅ๐ฅ๐จ๐ฐ๐๐ ๐ญ๐จ ๐ฉ๐ฅ๐๐ฒ!"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("! ๐ฒ๐จ๐ฎ ๐๐ข๐ ๐ง๐จ๐ญ ๐ ๐ข๐ฏ๐ ๐ฆ๐ ๐๐ฎ๐๐ข๐จ ๐๐ข๐ฅ๐ ๐จ๐ซ ๐ฒ๐ญ ๐ฅ๐ข๐ง๐ค ๐ญ๐จ ๐ฌ๐ญ๐ซ๐๐๐ฆ!")
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))    
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
        photo=f"{QUE_IMG}",
        reply_markup=keyboard,
        caption=f"#โฃ  ๐ฒ๐จ๐ฎ๐ซ ๐ซ๐๐ช๐ฎ๐๐ฌ๐ญ๐๐ ๐ฌ๐จ๐ง๐  ๐ฐ๐๐ฌ ๐๐๐๐๐ ๐ญ๐จ *๐ช๐ฎ๐๐ฎ๐* ๐๐ญ ๐ฉ๐จ๐ฌ๐ข๐ญ๐ข๐จ๐ง {position}!\n\nโก __Powered by Spotify A.I__")
        return await lel.delete()
    else:
        await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            ) 
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"๐ง **๐๐จ๐ฐ ๐ฉ๐ฅ๐๐ฒ๐ข๐ง๐ ** ๐ ๐ฌ๐จ๐ง๐  ๐ซ๐๐ช๐ฎ๐๐ฌ๐ญ๐๐ ๐๐ฒ {costumer}!\n\nโก __Powered by Spotify A.I__"
        )
        return await lel.delete()
