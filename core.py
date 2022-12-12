from os import environ as env
import ampalibe
from ampalibe.ui import QuickReply, Type, Button
from ampalibe.messenger import Action
from ampalibe import (
    Payload,
    Messenger,
    translate,
    Model,
    Logger,
    Configuration,
)
import asyncio
from utils.gpt import Gpt
from utils.tools import correct_split

conf_gpt = {
    "session_token": env.get("GPT_TOKEN"),
    "cf_clearance": env.get("GPT_CF_CLEARANCE"),
    "user_agent": env.get("GPT_USER_AGENT"),
}

new_config = {
    "Authorization": env.get("GPT_SESSION_TOKEN"),
}


query = Model(Configuration())
chat = Messenger()


chat.get_started("/GET_STARTED")


@ampalibe.command("/")
def main(sender_id, lang, cmd, **ext):
    send_persistant(sender_id, lang, cmd, **ext)
    try:
        gpt = Gpt(conf_gpt)
        # gpt = Gpt(new_config)
        bot = gpt.chatbot

    except Exception as e:
        Logger.error(e)
        chat.send_message(sender_id, translate("error_gpt", lang))
        chat.send_message(
            env.get("ADMIN_SENDER_ID"),
            "Tu peux voir s'il te plaît j'ai encore un problème de token",
        )
        return
    # I get the message from the user , send it to the GPT-3 API and get the response
    chat.send_action(sender_id, Action.typing_on)
    message = asyncio.run(bot.get_chat_response(cmd))["message"]
    message = correct_split(message)
    for text in message:
        chat.send_message(sender_id, text)


def send_persistant(sender_id, lang, cmd, **ext):
    persistent_menu = [
        Button(
            type=Type.postback,
            title=translate("about", lang),
            payload=Payload("/me"),
        ),
        Button(
            type=Type.postback,
            title=translate("language", lang),
            payload=Payload("/language"),
        ),
        Button(
            type=Type.postback,
            title=translate("buy_me_a_coffee", lang),
            payload=Payload("/buy_me_a_coffee"),
        ),
    ]

    chat.persistent_menu(sender_id, persistent_menu)


@ampalibe.before_receive()
def before_process(sender_id, cmd, **ext):
    chat.send_action(sender_id, Action.mark_seen)
    return True


@ampalibe.command("/me")
def about_me(sender_id, lang, cmd, **ext):
    send_persistant(sender_id, lang, cmd, **ext)
    chat.send_message(sender_id, translate("about_me", lang))
    buttons = [
        Button(
            type=Type.web_url,
            title=translate("go_github", lang),
            url="https://github.com/rivo2302/MyChatGPT",
        )
    ]

    chat.send_button(sender_id, buttons, translate("voir_repos", lang))


@ampalibe.command("/GET_STARTED")
def start(sender_id, lang, cmd, **ext):

    # Send the first Message to user
    send_persistant(sender_id, lang, cmd, **ext)
    chat.send_message(sender_id, translate("greetings", lang))
    chat.send_text(sender_id, translate("about_me", lang))


@ampalibe.command("/language")
def send_language(sender_id, lang, cmd, **ext):
    send_persistant(sender_id, lang, cmd, **ext)
    # Send the language menu
    language_menu = [
        QuickReply(
            title="🇲🇬MG",
            payload=Payload("/SET_LANGUAGE", value="mg"),
        ),
        QuickReply(
            title="🇨🇵FR",
            payload=Payload("/SET_LANGUAGE", value="fr"),
        ),
        QuickReply(
            title="🇬🇧EN",
            payload=Payload("/SET_LANGUAGE", value="en"),
        ),
    ]
    chat.send_quick_reply(
        sender_id,
        language_menu,
        translate("language_question", lang),
    )


@ampalibe.command("/SET_LANGUAGE")
def set_language(sender_id, lang, cmd, **ext):

    if ext.get("value"):
        value = ext.get("value")
        if value in ["mg", "fr", "en"]:
            query.set_lang(sender_id, value)
            send_persistant(sender_id, value, cmd, **ext)
            chat.send_message(sender_id, translate("language_changed", value))
        else:
            chat.send_message(
                sender_id, translate("language_not_changed", lang)
            )
            Logger.error("Language value invalid")
    else:
        Logger.error("No value language found")
        chat.send_message(sender_id, translate("language_not_changed", lang))
    query.set_action(sender_id, None)


@ampalibe.command("/buy_me_a_coffee")
def buy_me_a_coffee(sender_id, lang, cmd, **ext):
    chat.send_message(sender_id, translate("buy_me_a_coffee_response", lang))
