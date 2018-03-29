from telegram.ext import Updater, RegexHandler, ConversationHandler
import logging
import random


HEARTS = ['❤', '💛', '💚', '💙', '💜', '🖤']
REGULAR_STATE = 0

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def send_heart(bot, update):
    bot.send_message(chat_id=update.effective_chat.id, text=random.choice(HEARTS))
    return REGULAR_STATE


def handle_error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.error('Update "%s" caused error "%s"', update, error)


def main():
    with open('token.txt', 'r') as token_file:
        updater = Updater(token_file.read().strip())

    hearts_regex_handler = RegexHandler('^.*(' + '|'.join(HEARTS) + ').*$', send_heart)#, pass_user_data=True)
    
    conversation_handler = ConversationHandler(
        entry_points=[ hearts_regex_handler ],
        states={ REGULAR_STATE: [ hearts_regex_handler ] },
        fallbacks=[]
    )

    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_error_handler(handle_error)

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()