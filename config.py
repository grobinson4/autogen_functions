import os
import dotenv

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