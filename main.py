import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

message_history = list()
openai.api_key = 'YOUR OPENAI API KEY'
OWNER_ID = 'YOUR USER ID'


def chat(inp: str, role="user") -> str:
    global message_history
    message_history.append({'role': role, 'content': inp})
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_history
        )
    reply_content = completion.choices[0].message.content
    message_history.append({'role': 'assistant', 'content': reply_content})
    return reply_content


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.chat_id) != OWNER_ID:
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="I only help my masters!"
            )
    else:
        text_inp = ' '.join(context.args)
        answer = chat(inp=text_inp)
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=answer
            )


if __name__ == '__main__':
    logger.info("Application is started...")
    application = ApplicationBuilder().token('YOUR BOT TOKEN').build()
    ask_handler = CommandHandler('ask', ask)
    application.add_handler(ask_handler)

    application.run_polling()
