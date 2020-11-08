
from emoji import get_emoji_regexp

import aiohttp
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
from os import environ

BOT_TOKEN = environ.get('BOT_TOKEN')

def start(update, context):

    update.message.reply_text(
        f'Hi! Mr {update.message.from_user.first_name}\n\nSend Me Your Link Fr Short Your Link\n\nFOR MORE TYPE /help \n\n©️ @AI_bot_projects')

def help_command(update, context):

    update.message.reply_text('**Tutorial**\n\nHello This Bot Can Short Your Link\n\nFirst <b>YOU HAVE TO GET YOUR API TOKEN OF GPLINK FROM <\b>https://gplinks.in/member/tools/api \n\nAFTER THAT COPY THAT LINK FROM GPLINK TOOLS API\nIT WILL LOOK LIKE  https://gplinks.in/api?api=6a4cb74d70edd86803333333333a&\nSENT IT TO ME\n\nNOW YOU ARE DONE JUST SEND LINK TO THIS BOT \n\nNOW YOU CAN USE THIS BOT \nTHANKS FOR USING MY BOT \n\n')


def cur_conv(update, context):
    """
    this function can get exchange rate results
    """
    if Config.CURRENCY_API is None:
        await message.edit(
            "<code>Oops!!get the API from</code> "
            "<a href='https://free.currencyconverterapi.com'>HERE</a> "
            "<code>& add it to Heroku config vars</code> (<code>CURRENCY_API</code>)",
            disable_web_page_preview=True,
            parse_mode="html", del_in=0)
        return

    filterinput = get_emoji_regexp().sub(u'', message.input_str)
    curcon = filterinput.upper().split()

    if len(curcon) == 3:
        amount, currency_to, currency_from = curcon
    else:
        await message.edit("`something went wrong!! do .help cr`")
        return

    if amount.isdigit():
        async with aiohttp.ClientSession() as ses:
            async with ses.get("https://free.currconv.com/api/v7/convert?"
                               f"apiKey={Config.CURRENCY_API}&q="
                               f"{currency_from}_{currency_to}&compact=ultra") as res:
                data = await res.json()
        result = data[f'{currency_from}_{currency_to}']
        result = float(amount) / float(result)
        result = round(result, 5)
        await message.edit(
            "**CURRENCY EXCHANGE RATE RESULT:**\n\n"
            f"`{amount}` **{currency_to}** = `{result}` **{currency_from}**")

    else:
        await message.edit(
            r"`This seems to be some alien currency, which I can't convert right now.. (⊙_⊙;)`",
            del_in=0)


def main():
    updater = Updater(
        BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(CommandHandler("cr", cur_conv))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
