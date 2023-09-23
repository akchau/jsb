from core.send_schdule import ScheduleSender
from telegram import Update
from telegram.ext import ContextTypes

async def load_and_sent_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ScheduleSender({}).get_shedule()
    )
    