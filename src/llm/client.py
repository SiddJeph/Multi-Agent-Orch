from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings


def get_llm(**kwargs) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=kwargs.pop("model", settings.llm_model),
        google_api_key=settings.google_api_key,
        temperature=kwargs.pop("temperature", 0.2),
        **kwargs,
    )
