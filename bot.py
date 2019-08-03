import sys
import time
import telepot
import logging
from logging.handlers import TimedRotatingFileHandler
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent

convertFrom = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
convertTo = "𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃"
conversionTable = dict(zip(convertFrom, convertTo))

startText = """This bot will help you to convert text to 𝓬𝓾𝓻𝓼𝓲𝓿𝓮.
To use this bot in your chats, type @CursiveTextBot <your message> into any chat's message box.
Alternatively, you may chat with this bot directly and copy the cursive text to any application you want!
"""

LOG_PATH = ''
FILE_NAME = 'log'

def getLogger():
    logFormatter = logging.Formatter(u"%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fileHandler = TimedRotatingFileHandler(LOG_PATH + FILE_NAME,when="d",encoding='utf-8',interval=1,backupCount=30)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    return logger

logger = getLogger()

logger.info('Starting up Telegram bot server...')

def convert(s):
    split = list(s)
    split = [conversionTable[x] if x in conversionTable else x for x in split]
    return "".join(split)

def on_chat_message(msg):

    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':

        if msg['text'] in ('/start', '/help'):

            bot.sendMessage(chat_id, startText)
            return

        bot.sendMessage(chat_id, convert(msg['text']))
        logger.info(f"{chat_type} message - {msg['from']['username']} said {msg['text']}")
    else:
        logger.info(f"{chat_type} message - {msg['from']['username']} sent {content_type}")

def on_inline_query(msg):
    def compute():
        query_string = telepot.glance(msg, flavor='inline_query')[2]

        logger.info(f"inline query message - {msg['from']['username']} sent {query_string}")

        articles = []
        if len(query_string) > 0: 
            articles = [InlineQueryResultArticle(
                        id='reply',
                        title=query_string,
                        description=convert(query_string),
                        input_message_content=InputTextMessageContent(
                            message_text = convert(query_string)
                        )
                   )]

        return articles

    answerer.answer(msg, compute)

TOKEN = ""

bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

MessageLoop(bot, {'chat': on_chat_message,
                  'inline_query': on_inline_query}).run_as_thread()

while 1:
    time.sleep(10)