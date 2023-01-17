import openai


class OpenAI:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate(
        self, prompt, engine="text-davinci-003", temperature=0, max_tokens=4000
    ):
        try:
            response = openai.Completion.create(
                model=engine,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as e:
            print(e)
            return None
        return response.choices[0].text
