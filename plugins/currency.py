
from emoji import get_emoji_regexp

import aiohttp
import os
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton
import config
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

CURRENCY_API = os.environ.get("CURRENCY_API", None)

@pyrogram.Client.on_message(pyrogram.Filters.command(["cr", "cnv"]))
async def cur_conv(bot, update):
    """
    this function can get exchange rate results
    """
    if CURRENCY_API is None:
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
                               f"apiKey={config.CURRENCY_API}&q="
                               f"{currency_from}_{currency_to}&compact=ultra") as res:
                data = await res.json()
        result = data[f'{currency_from}_{currency_to}']
        result = float(amount) / float(result)
        result = round(result, 5)
        await message.edit(
            "**CURRENCY EXCHANGE RATE RESULT:**\n\n"
            f"`{amount}` **{currency_to}** = `{result}` **{currency_from}**")
        await CHANNEL.log("`cr` command executed sucessfully")

    else:
        await message.edit(
            r"`This seems to be some alien currency, which I can't convert right now.. (⊙_⊙;)`",
            del_in=0)
