import importlib
import sys
import types
from pathlib import Path


def import_agents_with_stubs():
    # Ensure repository root is on the module search path
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    autogen_stub = types.ModuleType("autogen")

    class DummyAgent:
        def __init__(self, *args, **kwargs):
            pass

        def register_for_execution(self):
            def decorator(func):
                return func
            return decorator

        def register_for_llm(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator

    class DummyGroupChat:
        def __init__(self, *args, **kwargs):
            pass

    class DummyGroupChatManager:
        def __init__(self, *args, **kwargs):
            pass

    autogen_stub.AssistantAgent = DummyAgent
    autogen_stub.UserProxyAgent = DummyAgent
    autogen_stub.GroupChat = DummyGroupChat
    autogen_stub.GroupChatManager = DummyGroupChatManager
    sys.modules["autogen"] = autogen_stub

    tweepy_stub = types.ModuleType("tweepy")

    class OAuthHandler:
        def __init__(self, *args, **kwargs):
            pass

    class API:
        def __init__(self, *args, **kwargs):
            pass

        def update_status(self, *args, **kwargs):
            pass

    tweepy_stub.OAuthHandler = OAuthHandler
    tweepy_stub.API = API
    sys.modules["tweepy"] = tweepy_stub

    dotenv_stub = types.ModuleType("dotenv")
    def load_dotenv(*args, **kwargs):
        pass
    dotenv_stub.load_dotenv = load_dotenv
    sys.modules["dotenv"] = dotenv_stub

    return importlib.import_module("agents")


def test_analyze_tweets_and_create_thread():
    agents = import_agents_with_stubs()
    csv_path = Path(__file__).with_name("sample_tweets.csv")
    thread = agents.analyze_tweets_and_create_thread(str(csv_path))

    expected_segments = [
        "User @john said: Hello world on 2023-07-15.",
        "User @jane said: Another example tweet on 2023-07-16.",
        "User @mark said: A third, slightly longer tweet on 2023-07-17.",
    ]

    for seg in expected_segments:
        assert seg in thread

    for seg in thread.split("\n\n"):
        assert len(seg) <= 280
