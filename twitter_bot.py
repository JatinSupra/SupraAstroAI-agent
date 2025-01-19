import tweepy
import os
import requests
from dotenv import load_dotenv
from supra_agent import SupraAgent

# Load environment variables from .env file
load_dotenv()

# Set up Twitter API credentials
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Verify that all environment variables are set
if not all([BEARER_TOKEN, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise ValueError("One or more Twitter API credentials are missing in the .env file")

# Authenticate with the Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET_KEY, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

# Initialize the agent
agent = SupraAgent()

class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        user_handle = tweet.author_id
        tweet_id = tweet.id
        user_input = tweet.text.lower()

        if 'gettokens' in user_input:
            response = "Please provide your wallet address to receive testnet tokens."
            self._pending_requests[user_handle] = tweet_id
        elif user_handle in self._pending_requests:
            wallet_address = user_input.strip()
            response = self.request_testnet_tokens(wallet_address)
            del self._pending_requests[user_handle]
        elif 'supra' in user_input:
            response = self.get_supra_info()
        else:
            response = agent.handle_user_input(user_input)

        reply_text = f"@{user_handle} {response}"
        try:
            client.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet_id)
        except tweepy.TweepyException as e:
            print(f"Error creating tweet: {e}")

    def on_error(self, status_code):
        print(f"Error: {status_code}")
        return False  # Disconnects the stream

    def request_testnet_tokens(self, wallet_address: str) -> str:
        faucet_url = f"https://rpc-testnet.supra.com/rpc/v1/wallet/faucet/{wallet_address}"
        try:
            response = requests.get(faucet_url)
            if response.status_code == 200:
                return f"Testnet tokens have been sent to your wallet address: {wallet_address}"
            else:
                return f"Error: {response.json().get('message', 'Failed to request testnet tokens.')}"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_supra_info(self) -> str:
        return (
            "Supra is a Layer 1 blockchain, previously known as SupraOracles. It is designed to provide a robust and scalable "
            "infrastructure for decentralized applications. With high throughput and low latency, Supra aims to deliver "
            "enterprise-grade performance for smart contracts and decentralized finance (DeFi) projects."
        )

    def __init__(self, bearer_token):
        super().__init__(bearer_token)
        self._pending_requests = {}

def main():
    listener = MyStreamListener(bearer_token=BEARER_TOKEN)
    try:
        rules = listener.get_rules()
        if rules.data:
            rule_ids = [rule.id for rule in rules.data]
            listener.delete_rules(rule_ids)
        listener.add_rules(tweepy.StreamRule(value='@YourTwitterHandle'))
    except tweepy.TweepyException as e:
        print(f"Error adding rules: {e}")
        return

    try:
        listener.filter()
    except tweepy.TweepyException as e:
        print(f"Error starting stream: {e}")

if __name__ == "__main__":
    main()
