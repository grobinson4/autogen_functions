import csv
import autogen
import config
import tweepy
from typing import List


from typing import List, Dict

# Assuming autogen and config are predefined modules similar to the initial setup
linkedin_bot = autogen.AssistantAgent(
    name="linkedin_bot",
    system_message="For twitter posts, only use the functions you have been provided with. Notify the description maker when the task is done.",
    llm_config=config.llm_config,
)

description_maker = autogen.AssistantAgent(
    name="description_maker",
    system_message="You are to create a tweet thread based on the analysis of competitor tweets. Only write the description and reply TERMINATE when the task is done.",
    llm_config=config.llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "code",
        "use_docker": False
    }
)

# Initialize Tweepy with Twitter API credentials
def authenticate_twitter_api(consumer_key: str, consumer_secret: str, access_token: str, access_token_secret: str):
    """
    Authenticate to Twitter API using Tweepy.

    :param consumer_key: Twitter API consumer key.
    :param consumer_secret: Twitter API consumer secret.
    :param access_token: Twitter API access token.
    :param access_token_secret: Twitter API access token secret.
    :return: Authenticated Tweepy API object.
    """
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def postTweet(api, tweet_text: str):
    """
    Post a tweet using the authenticated Twitter API object.

    :param api: Authenticated Tweepy API object.
    :param tweet_text: Text content of the tweet to be posted.
    """
    try:
        # Post the tweet
        api.update_status(tweet_text)
        print("Tweet posted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    consumer_key = 'CTcqMGYZ1WVOejUyzR4IGukCD'
    consumer_secret = 'M0tODYQj936VCfBtFPM9wYt1norJ4EXdcF4wxQcdvOPZJYLRzR'
    access_token = '1281380815188963328-hWzlbxAnoF1WCnsYS9znFhWhnz1xMH'
    access_token_secret = '8l2uYhtaOqAhdEDTrkBHJaBcCfHxVCQ9jNxq8vG5kLdA2'

    # Authenticate to Twitter
    api = authenticate_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)

    # Specify the username
    tweet_text = "Hello, world! This is my first tweet using Tweepy and the Twitter API."

    # Post the tweet
    postTweet(api, tweet_text)

@user_proxy.register_for_execution()
@linkedin_bot.register_for_llm(description="Fetch and format competitor posts.")
def fetch_and_format_posts():
    consumer_key = 'CTcqMGYZ1WVOejUyzR4IGukCD'
    consumer_secret = 'M0tODYQj936VCfBtFPM9wYt1norJ4EXdcF4wxQcdvOPZJYLRzR'
    access_token = '1281380815188963328-hWzlbxAnoF1WCnsYS9znFhWhnz1xMH'
    access_token_secret = '8l2uYhtaOqAhdEDTrkBHJaBcCfHxVCQ9jNxq8vG5kLdA2'
    api = authenticate_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret)

    tweet_text = "Hello, world! This is my first tweet using Tweepy and the Twitter API."

    # Post the tweet
    postTweet(api, tweet_text)
    return 'done'

# Function for the description maker to analyze the CSV and create a tweet thread
@description_maker.register_for_llm(description="Create tweet thread from competitor post analysis.")
def analyze_tweets_and_create_thread(csv_file_path: str) -> str:
    tweets = []
    # Read the CSV file
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tweets.append(row)

    # Simulate analysis and create a thread
    # For simplicity, this example just concatenates tweets, but you should implement actual analysis
    tweet_thread = []
    for tweet in tweets:
        # For the sake of this example, let's just append each tweet to our thread
        # In a real scenario, you'd perform analysis to determine how to construct your thread
        tweet_thread.append(f"User @{tweet['user']} said: {tweet['tweet']} on {tweet['date']}.")
    
    # Combine the individual tweets into a single string to simulate a tweet thread
    tweet_thread_str = "\n\n".join(tweet_thread)
    
    # Check if the thread is too long and truncate if necessary (Twitter has a character limit per tweet)
    if len(tweet_thread_str) > 280:
        tweet_thread_str = tweet_thread_str[:277] + "..."
    
    return tweet_thread_str

group_chat = autogen.GroupChat(agents=[user_proxy, linkedin_bot, description_maker], messages=[], max_round=5)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=config.llm_config)
