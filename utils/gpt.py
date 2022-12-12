# We are using the revChatGPT library to interact with the GPT-3 API, we use the asuchronous version of the library to avoid blocking the main thread.
from revChatGPT.revChatGPT import AsyncChatbot as Chatbot
from os import environ as env


class Gpt:
    def __init__(self, config, conversation_id=None):
        self.chatbot = Chatbot(config, conversation_id=conversation_id)

    def get_response(self, message):
        return self.chatbot.get_response(message)


# conf_gpt = {
#     "session_token": env.get("GPT_TOKEN"),
#     "cf_clearance": env.get("GPT_CF_CLEARANCE"),
#     "user_agent": env.get("GPT_USER_AGENT"),
# }
# gpt = Gpt(conf_gpt)
# bot = gpt.chatbot
