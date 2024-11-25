import agents

agents.user_proxy.initiate_chat(
    agents.manager,
    message=f"Use the twitter bot to fetch tweets of the given competitors and format in a csv."
    "Then use the description maker to analyze the CSV and create a tweet thread."
)