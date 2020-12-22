from os import environ
import datetime
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
BOT_TOKEN = environ.get('BOT_TOKEN')
API_KEY = environ.get('API_KEY')


bot = Client('clickyfly bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=10)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        text=f"**Hi {message.chat.first_name}!** \n\nThis is **Bestz URL Shorter Bot**. Just send me any big link and get short link.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('❤ Bots Updates Channel ❤', url='https://t.me/naijabestz'),
                    InlineKeyboardButton('Feedback 🤷‍♂️', url='https://t.me/bestzbrothers')
                ],
                [
                    InlineKeyboardButton('⭐ Support Group ⭐', url='https://t.me/naija_bestz')
                    InlineKeyboardButton('Source 😜', url='https://github.com/Davoe-D/FileRenameBot')
                ]
            ]
        )
    )


@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    link = message.matches[0].group(0)
    try:
        short_link = await get_shortlink(link)
        await message.reply(
            text=f"Here is your short link: {short_link}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Open Link', url=short_link)
                    ]
                ]
            ),
            quote=True
        )
        now = datetime.datetime.now()
        chat_id = environ.get('LOG_CHANNEL', -1001283278354)
        uname = f"[{message.from_user.first_name}](tg://openmessage?user_id={message.from_user.id})"
        await bot.send_message(chat_id, f"**#SHORTEN: \n\n@ClickyFly_Bot Shortened** {link} **to** {short_link} **for** {uname} **at** `{now}`", parse_mode="markdown", disable_web_page_preview=True)
        #await bot.send_message(chat_id, f"**#SHORTEN: \n\n@ClickyFly_Bot Shortened** {link} **to** {short_link} **at** `{now}`", parse_mode="markdown", disable_web_page_preview=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


async def get_shortlink(link):
    url = 'https://cutt.ly/api'
    params = {'api': '59902e5ebd09119342dc8ee0f5ff4ff1d1641', 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]


bot.run()
