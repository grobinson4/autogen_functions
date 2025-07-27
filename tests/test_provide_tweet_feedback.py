import importlib
import sys
import types


# Copied helper from test_analyze_tweets to stub external dependencies

def import_agents_with_stubs():
    project_root = __file__.rsplit('/', 2)[0]
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

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


def test_provide_tweet_feedback():
    agents = import_agents_with_stubs()

    assert (
        agents.provide_tweet_feedback("short")
        == "The tweet is very short; consider adding more context."
    )

    assert (
        agents.provide_tweet_feedback("this is a reasonably sized tweet")
        == "The tweet length looks good."
    )

    long_tweet = "a" * 201
    assert (
        agents.provide_tweet_feedback(long_tweet)
        == "Consider reducing the length of the tweet for better engagement."
    )

