import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from datetime import time

# Logging beállítása
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ConversationHandler állapotok
WAITING_NAME, WAITING_COMPANY = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Üdvözlő üzenet és főmenü"""
    user = update.effective_user
    welcome_text = (
        f"👋 Szia {user.first_name}!\n\n"
        f"🤖 Telegram Bot Demo vagyok!\n\n"
        f"Készítette: Ecsedi Tamás\n"
        f"Verzió: 1.0 Proto Demo\n\n"
        f"Íme, amit tudok neked bemutatni:"
    )

    keyboard = [
        [InlineKeyboardButton("📹 Videó küldés", callback_data="send_video")],
        [InlineKeyboardButton("🎵 Hang küldés", callback_data="send_audio")],
        [InlineKeyboardButton("💬 Interaktív beszélgetés", callback_data="start_conversation")],
        [InlineKeyboardButton("⏰ Emlékeztető beállítás", callback_data="set_reminder")],
        [InlineKeyboardButton("📊 Statisztikák", callback_data="show_stats")],
        [InlineKeyboardButton("ℹ️ Információ", callback_data="info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

    # Statisztika növelése
    context.bot_data['total_starts'] = context.bot_data.get('total_starts', 0) + 1


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline gombok kezelése"""
    query = update.callback_query
    await query.answer()  # Kötelező!

    if query.data == "send_video":
        await query.edit_message_text("📹 Videó küldése folyamatban...")
        # YouTube videó küldése
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🎬 Bemutató videó:\n\n"
                 "https://www.youtube.com/watch?v=rLGtnc4yDo0\n\n"
                 "A Telegram botok képesek videók, YouTube linkek "
                 "és média tartalmak megosztására!"
        )
        await show_back_button(query.message.chat_id, context)

    elif query.data == "send_audio":
        await query.edit_message_text("🎵 Hang küldése folyamatban...")
        try:
            # MP3 fájl küldése
            with open("music-track.mp3", "rb") as audio_file:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio_file,
                    title="Demo Zene",
                    performer="Ecsitomi Bot",
                    caption="🎼 A bot képes hangfájlok, zenék küldésére!"
                )
        except FileNotFoundError:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="❌ A music-track.mp3 fájl nem található!\n\n"
                     "Kérlek töltsd fel a fájlt ugyanoda, ahol a bot fut."
            )
        await show_back_button(query.message.chat_id, context)

    elif query.data == "start_conversation":
        await query.edit_message_text(
            "💬 Interaktív beszélgetés:\n\n"
            "Kérlek használd a /regisztracio parancsot, "
            "hogy elindítsd az interaktív regisztrációs folyamatot!"
        )
        await show_back_button(query.message.chat_id, context)

    elif query.data == "set_reminder":
        chat_id = query.message.chat_id

        # Emlékeztető beállítása 30 másodperc múlva
        context.job_queue.run_once(
            reminder_callback,
            30,
            chat_id=chat_id,
            name=f"reminder_{chat_id}"
        )

        await query.edit_message_text(
            "⏰ Emlékeztető beállítva!\n\n"
            "30 másodperc múlva küldök neked egy emlékeztetőt.\n\n"
            "A bot képes:\n"
            "• Egyszeri emlékeztetőkre\n"
            "• Ismétlődő feladatokra\n"
            "• Napi időzített üzenetekre"
        )
        await show_back_button(query.message.chat_id, context)

    elif query.data == "show_stats":
        total_starts = context.bot_data.get('total_starts', 0)
        total_conversations = context.bot_data.get('total_conversations', 0)

        stats_text = (
            f"📊 Bot Statisztikák:\n\n"
            f"🚀 Összes indítás: {total_starts}\n"
            f"💬 Regisztrációk: {total_conversations}\n"
            f"👤 Te vagy: {query.from_user.first_name}\n"
            f"🆔 User ID: {query.from_user.id}\n\n"
            f"A bot képes felhasználói és chat adatok tárolására!"
        )
        await query.edit_message_text(stats_text)
        await show_back_button(query.message.chat_id, context)

    elif query.data == "info":
        info_text = (
            "ℹ️ Bot Képességek:\n\n"
            "✅ Szöveg, képek, videók, hangok küldése\n"
            "✅ Interaktív gombok (inline keyboard)\n"
            "✅ Többlépcsős beszélgetések\n"
            "✅ Időzített üzenetek és emlékeztetők\n"
            "✅ Felhasználói adatok tárolása\n"
            "✅ Statisztikák gyűjtése\n"
            "✅ Parancsok kezelése\n"
            "✅ Hiba kezelés\n\n"
            "🔧 Technológia: Python Telegram Bot (PTB)\n"
            "📦 Verzió: 22.5+"
            "\nA parancsok megtekintéséhez használd a /help utasítást!"
        )
        await query.edit_message_text(info_text)
        await show_back_button(query.message.chat_id, context)

    elif query.data == "back_to_menu":
        welcome_text = (
            "🤖 Főmenü\n\n"
            "Válassz az alábbi opciók közül:"
        )
        keyboard = [
            [InlineKeyboardButton("📹 Videó küldés", callback_data="send_video")],
            [InlineKeyboardButton("🎵 Hang küldés", callback_data="send_audio")],
            [InlineKeyboardButton("💬 Interaktív beszélgetés", callback_data="start_conversation")],
            [InlineKeyboardButton("⏰ Emlékeztető beállítás", callback_data="set_reminder")],
            [InlineKeyboardButton("📊 Statisztikák", callback_data="show_stats")],
            [InlineKeyboardButton("ℹ️ Információ", callback_data="info")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(welcome_text, reply_markup=reply_markup)


async def show_back_button(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    """Vissza gomb megjelenítése"""
    keyboard = [[InlineKeyboardButton("🔙 Vissza a főmenübe", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat_id,
        text="👉 Használd a gombot a visszalépéshez:",
        reply_markup=reply_markup
    )


async def reminder_callback(context: ContextTypes.DEFAULT_TYPE):
    """Emlékeztető callback"""
    job = context.job
    await context.bot.send_message(
        job.chat_id,
        text="🔔 Emlékeztető!\n\nEz egy időzített üzenet volt. "
             "A bot képes bármilyen időzítést kezelni!"
    )


# ConversationHandler funkciók
async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Regisztráció indítása"""
    await update.message.reply_text(
        "👤 Kezdjük a regisztrációt!\n\n"
        "Mi a neved?"
    )
    return WAITING_NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Név fogadása"""
    name = update.message.text
    context.user_data['name'] = name

    await update.message.reply_text(
        f"Köszönöm, {name}! 👍\n\n"
        f"Milyen cégnél dolgozol?"
    )
    return WAITING_COMPANY


async def receive_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cég fogadása"""
    company = update.message.text
    name = context.user_data.get('name', 'Ismeretlen')

    context.user_data['company'] = company

    # Statisztika növelése
    context.bot_data['total_conversations'] = context.bot_data.get('total_conversations', 0) + 1

    await update.message.reply_text(
        f"✅ Sikeres regisztráció!\n\n"
        f"📝 Adatok:\n"
        f"Név: {name}\n"
        f"Cég: {company}\n\n"
        f"Ezeket az adatokat a bot eltárolja és később is elérheti!\n\n"
        f"Használd a /start parancsot a főmenühöz."
    )
    return ConversationHandler.END


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Beszélgetés megszakítása"""
    await update.message.reply_text(
        "❌ Regisztráció megszakítva.\n\n"
        "Használd a /start parancsot a főmenühöz."
    )
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Súgó parancs"""
    help_text = (
        "📖 Elérhető parancsok:\n\n"
        "/start - Főmenü megnyitása\n"
        "/help - Súgó megjelenítése\n"
        "/regisztracio - Interaktív regisztráció\n"
        "/cancel - Regisztráció megszakítása\n"
        "/info - Bot információk\n\n"
        "💡 Használd a gombokat a könnyebb navigációhoz!"
    )
    await update.message.reply_text(help_text)


async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Szöveg visszaküldése"""
    user_text = update.message.text
    await update.message.reply_text(
        f"📝 Ezt írtad: {user_text}\n\n"
        f"A bot képes minden üzenetet feldolgozni és válaszolni rá.\n\n"
        f"Használd a /start parancsot a főmenühöz."
    )


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Info parancs"""
    user = update.effective_user
    user_info = context.user_data.get('name', 'Nincs mentve')

    info_text = (
        f"👤 Felhasználói információk:\n\n"
        f"Telegram név: {user.first_name}\n"
        f"User ID: {user.id}\n"
        f"Mentett név: {user_info}\n\n"
        f"🤖 Bot információk:\n"
        f"Verzió: 1.0 Demo\n"
        f"Technológia: Python Telegram Bot\n"
        f"Státusz: Aktív ✅"
    )
    await update.message.reply_text(info_text)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Hibakezelő"""
    logger.error("Hiba történt:", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Hiba történt a feldolgozás során.\n\n"
            "Kérlek próbáld újra, vagy használd a /start parancsot."
        )


def main():
    """Bot indítása"""
    # Token betöltése a config.py fájlból
    from config import BOT_TOKEN

    # Application építése
    application = Application.builder().token(BOT_TOKEN).build()

    # ConversationHandler regisztráció
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("regisztracio", start_registration)],
        states={
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
            WAITING_COMPANY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_company)]
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)]
    )

    # Handler-ek hozzáadása
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_handler))

    # Error handler
    application.add_error_handler(error_handler)

    # Bot indítása
    logger.info("Bot indítása...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()