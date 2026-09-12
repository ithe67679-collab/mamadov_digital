import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==== SOZLAMALAR ====
# Railway'da "Variables" bo'limiga BOT_TOKEN nomli o'zgaruvchi qo'shing.
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8965830878:AAFbtlCc2iGc0duXQklhnlZw0eI1Q7kKs40")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ==== XIZMATLAR VA NARXLAR (shu yerdan o'zgartirasiz) ====
SERVICES = {
    "tgbot": {
        "title": "🤖 Telegram bot",
        "items": [
            ("Oddiy bot (menyu, javob berish)", "300 000 so'm"),
            ("O'rtacha bot (baza bilan, buyurtma qabul qilish)", "700 000 so'm"),
            ("Murakkab bot (to'lov, admin panel, integratsiya)", "1 500 000 so'm dan"),
        ],
    },
    "logo": {
        "title": "🎨 Logotip",
        "items": [
            ("Basic (1 variant, PNG)", "80 000 so'm"),
            ("Standard (3 variant, PNG+SVG)", "150 000 so'm"),
            ("Premium (5+ variant, barcha format, brendbook)", "300 000 so'm"),
        ],
    },
    "web": {
        "title": "🌐 Veb-sayt",
        "items": [
            ("Landing page (1 sahifa)", "800 000 so'm"),
            ("Vizitka sayt (3-5 sahifa)", "1 500 000 so'm"),
            ("Katalog / biznes sayt (admin panel bilan)", "3 000 000 so'm dan"),
        ],
    },
}


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🤖 Telegram bot narxi", callback_data="svc_tgbot")],
        [InlineKeyboardButton("🎨 Logotip narxi", callback_data="svc_logo")],
        [InlineKeyboardButton("🌐 Veb-sayt narxi", callback_data="svc_web")],
        [InlineKeyboardButton("📞 Bog'lanish", callback_data="contact")],
    ]
    return InlineKeyboardMarkup(keyboard)


def service_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ Buyurtma berish", callback_data="order")],
        [InlineKeyboardButton("⬅️ Bosh menyu", callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Assalomu alaykum!\n\n"
        "Xizmatlarimiz: Telegram bot, Logotip dizayn, Veb-sayt yaratish.\n"
        "Narxlarni bilish uchun kerakli bo'limni tanlang:"
    )
    await update.message.reply_text(text, reply_markup=main_menu_keyboard())


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back_main":
        text = "👋 Bosh menyu:"
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())

    elif data.startswith("svc_"):
        key = data.replace("svc_", "")
        svc = SERVICES[key]
        lines = "\n".join([f"• {name} — *{price}*" for name, price in svc["items"]])
        text = f"{svc['title']} narxlari:\n\n{lines}"
        await query.edit_message_text(
            text, reply_markup=service_keyboard(), parse_mode="Markdown"
        )

    elif data == "order":
        text = (
            "✅ So'rovingiz qabul qilindi!\n\n"
            "Menejerimiz siz bilan tez orada bog'lanadi.\n"
            "Yoki to'g'ridan-to'g'ri yozing: @mamadov_13"
        )
        await query.edit_message_text(text, reply_markup=main_menu_keyboard())

    elif data == "contact":
        text = (
            "📞 *Bog'lanish:*\n\n"
            "Telegram: @mamadov_13\n"
            "Tel: +998 90 695 60 60\n"
            "Instagram: @devx.uz"
        )
        await query.edit_message_text(
            text, reply_markup=main_menu_keyboard(), parse_mode="Markdown"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
