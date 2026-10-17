from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


class LLM:
    def __init__(self):
        load_dotenv()
        model = os.getenv("MODEL_LLM")
        base_url = os.getenv("BASE_URL_SERVER")
        api_key = os.getenv("API_KEY_SERVER")

        modelo = ChatOpenAI(
            model = model,
            base_url = base_url,
            api_key = api_key,
            temperature = 0
            )
        self.model = modelo

    def get_llm_model(self):
        return self.model


#resp = modelo.invoke("Olá")
#print(resp.text)