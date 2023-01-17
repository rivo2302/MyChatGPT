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
from utils.ai import OpenAI
<<<<<<< HEAD
=======
from utils.tools import correct_split
>>>>>>> 086f94eb448730b0e058275d596b888e23252f88


query = Model(Configuration())
chat = Messenger()
gpt = OpenAI(env.get("OPENAI_API_KEY"))

chat.get_started("/GET_STARTED")


@ampalibe.command("/")
def main(sender_id, lang, cmd, **ext):
<<<<<<< HEAD
    print("here")
=======
>>>>>>> 086f94eb448730b0e058275d596b888e23252f88
    send_persistant(sender_id, lang, cmd, **ext)
    chat.send_action(sender_id, Action.typing_on)
    response = gpt.generate(prompt=cmd, temperature=0.5, max_tokens=4000)
    if response:
<<<<<<< HEAD
        chat.send_message(sender_id, response)
    else:
        chat.send_message(sender_id, translate("error", lang))
    print(response)
=======
        response = correct_split(response)
        for r in response:
            chat.send_text(sender_id, r)
    else:
        chat.send_text(sender_id, translate("error_gpt", lang))
    chat.send_action(sender_id, Action.typing_off)
>>>>>>> 086f94eb448730b0e058275d596b888e23252f88


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
    chat.send_action(sender_id, Action.typing_on)
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
