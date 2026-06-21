from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings


def get_llm(**kwargs) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=kwargs.pop("model", settings.LLM_MODEL),
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=kwargs.pop("temperature", 0.2),
        **kwargs,
    )
