import os
import json
import logging
import telegram

from commands import command_handler, default_handler, is_command, parse_command
from exceptions import CommandNotFound, CharacterNotFound

from telegram.ext import Updater
from telegram.ext import CommandHandler

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 500,
    'body': json.dumps('Oops, something went wrong!')
}

def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)

def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    bot = configure_telegram()
    logger.info('Event: {}'.format(event))

    if event.get('httpMethod') == 'POST' and event.get('body'):
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)

        if not is_command(update):
            return ERROR_RESPONSE

        username = update.message.from_user.username if update.message.from_user.username else update.message.from_user.first_name
        command = parse_command(update.message.text)
        txt_args = update.message.text.split(' ')[1:]

        try:
            command_handler(command)(bot, update, command, txt_args)
            return OK_RESPONSE
        except CommandNotFound:
            default_handler(bot, update, f'Command {command} not found')
            return ERROR_RESPONSE
        except CharacterNotFound:
            default_handler(bot, update, f'Character not found. Cannot execute {update.message.text}')
            return ERROR_RESPONSE

    return ERROR_RESPONSE


def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """

    logger.info('Event: {}'.format(event))
    bot = configure_telegram()
    url = 'https://{}/{}/'.format(
        event.get('headers').get('Host'),
        event.get('requestContext').get('stage'),
    )
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE
