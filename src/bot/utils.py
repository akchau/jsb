




async def clean_all_messages_upper(update, context):
    chat_id = update.effective_chat.id
    current_message_id = update.effective_message.message_id
    for message_id in range(current_message_id - 1, current_message_id - 10, -1):
        try:
            message = await context.bot.get_message(chat_id=chat_id, message_id=message_id)
            # if message.text == "/start":
            #     continue
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            continue