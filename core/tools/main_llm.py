from decouple import config
from crewai import LLM

main_llm = LLM(
    model=config('OPENAI_MODEL', default='gpt-4o-mini'),
    api_key=config('OPENAI_API_KEY'),
    temperature=config('OPENAI_DEFAULT_TEMPERATURE', default=0.5, cast=float)
)