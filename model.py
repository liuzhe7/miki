from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pydantic import SecretStr

load_dotenv()
model = ChatOpenAI(
    base_url="https://api.moonshot.cn/v1",
    api_key=SecretStr(os.getenv("KIMI_API_KEY", "placeholder_api_key")),
    model="moonshot-v1-8k",
    temperature=0.5,
    timeout=10,
)
