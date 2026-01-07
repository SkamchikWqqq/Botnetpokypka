from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SUPPORT
markupUser = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💣 Снос', callback_data='snos'),
         InlineKeyboardButton(text='👨‍💻 Поддержка', url=SUPPORT)],
        [InlineKeyboardButton(text='💎 Купить подписку', callback_data='buySub')]
    ]
)

markupAdmin = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💣 Снос', callback_data='snos'),
         InlineKeyboardButton(text='👨‍💻 Поддержка', url=SUPPORT)],
        [InlineKeyboardButton(text='💎 Купить подписку', callback_data='buySub'),
         InlineKeyboardButton(text='⚙️ Админ панель', callback_data='adminpanel')]
    ]
)

markupBuySub = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='💎 Неделя - 3$', callback_data='BuySub3'),
         InlineKeyboardButton(text='💎 Месяц - 6$', callback_data='BuySub6')],
        [InlineKeyboardButton(text='💎 Год - 9$', callback_data='BuySub9'),
         InlineKeyboardButton(text='💎 Навсегда - 15$', callback_data='BuySub15')],
        [InlineKeyboardButton(text='💎 Оплата по карте', url=SUPPORT)]
    ]
)

markupAdminPanel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='✅ Выдать подписку', callback_data='giveSub'),
         InlineKeyboardButton(text='❌ Забрать подписку', callback_data='closeSub')]
    ]
)