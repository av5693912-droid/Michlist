"""
Bot Telegram (modalita' webhook) per hosting 24/7 su Render.com (piano gratuito).

REQUISITI: vedi requirements.txt

VARIABILI D'AMBIENTE da impostare su Render (Settings -> Environment):
    BOT_TOKEN     -> il token che ti ha dato @BotFather
    WEBAPP_URL    -> il link https:// della checklist (es. su Netlify)
    RENDER_EXTERNAL_URL -> viene impostata AUTOMATICAMENTE da Render, non toccarla

COME FUNZIONA IL DEPLOY: vedi le istruzioni nella chat.
"""

import os
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ["WEBAPP_URL"]

# Render fornisce questa variabile automaticamente con l'URL pubblico del servizio
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "")
PORT = int(os.environ.get("PORT", "10000"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = ReplyKeyboardMarkup.from_button(
        KeyboardButton(
            text="📋 Apri Checklist",
            web_app=WebAppInfo(url=WEBAPP_URL),
        ),
        resize_keyboard=True,
    )
    await update.message.reply_text(
        "Ciao! Tocca il pulsante qui sotto per aprire la tua checklist.",
        reply_markup=keyboard,
    )


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    if RENDER_EXTERNAL_URL:
        # Modalita' webhook: Render ci dice il proprio URL pubblico
        webhook_path = BOT_TOKEN  # usiamo il token come percorso segreto
        full_webhook_url = f"{RENDER_EXTERNAL_URL}/{webhook_path}"
        print(f"Avvio in modalita' webhook su {full_webhook_url}")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=webhook_path,
            webhook_url=full_webhook_url,
        )
    else:
        # Fallback: se lanciato in locale (senza RENDER_EXTERNAL_URL), usa il polling
        print("RENDER_EXTERNAL_URL non trovata: avvio in modalita' polling (uso locale).")
        app.run_polling()


if __name__ == "__main__":
    main()
