import os
try:
    import dotenv
except ModuleNotFoundError:  # pragma: no cover - runtime fallback
    class dotenv:
        @staticmethod
        def load_dotenv(*args, **kwargs):
            """Fallback no-op if python-dotenv is unavailable."""
            pass

dotenv.load_dotenv()

config_list = [
    {
        "model": os.getenv("MODEL"),
        "api_key": os.getenv("OPENAI_API_KEY"),
    }
]

llm_config = {
    "config_list": config_list,
    "timeout": 120,
}
