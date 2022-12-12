# We are using the revChatGPT library to interact with the GPT-3 API, we use the asuchronous version of the library to avoid blocking the main thread.
from revChatGPT.revChatGPT import AsyncChatbot as Chatbot


class Gpt:
    def __init__(self, config, conversation_id=None):
        self.chatbot = Chatbot(config, conversation_id=conversation_id)

    def get_response(self, message):
        return self.chatbot.get_response(message)
