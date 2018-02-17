import random
from typing import Optional, List

from telegram import Message, Chat, Update, Bot
from telegram import ParseMode
from telegram.ext import run_async
from telegram.utils.helpers import escape_markdown

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user


@run_async
def birthday(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    user_id = extract_user(update.effective_message, args)
    if user_id:
        target_user = bot.get_chat(user_id)
        if target_user.id == bot.id:
            msg.reply_text("Bots don't have birthdays, right?")
            return ""
        elif target_user.username:
            target_user = "@" + escape_markdown(target_user.username)
        else:
            target_user = "[{}](tg://user?id={})".format(target_user.first_name,
                                                   target_user.id)
    else:
        if not args:
            msg.reply_text("I see what you did there...")
        return ""


    count = random.randint(1, 10)
    repl = format("Happy birthday, {}!\n".format(target_user) * count)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@run_async
def nou(bot: Bot, update: Update):
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    no_count = random.randint(1, 50)
    no_text = "No" * no_count
    repl = format("{}U".format(no_text))

    reply_text(repl)


__help__ = """
 - /birthday: wish an user a happy birthday 1-10 times 😂.
 - /nou: (No \* [1-50])U
"""

__mod_name__ = "Misc 2"

BIRTHDAY_HANDLER = DisableAbleCommandHandler("birthday", birthday, pass_args=True)
NOU_HANDLER = DisableAbleCommandHandler("nou", nou)

dispatcher.add_handler(BIRTHDAY_HANDLER)
dispatcher.add_handler(NOU_HANDLER)
