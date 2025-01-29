import openai
import requests
import os
from dotenv import load_dotenv

# make sure you have all API keys and tokens in .env file and you have installed all the required libraries as well else you will get an error
load_dotenv()

# SupraAgent class to provide information about Supra Move L1 chain and help with testnet token funding
class SupraAgent:
    def __init__(self):
        self.name = 'Robbie'
        self.description = 'Provides information about Supra Layer 1 Blockchain and helps with testnet $SUPRA token funding.'
        self.personality = 'informative and friendly'
        openai.api_key = os.getenv('OPENAI_API_KEY')

# Fetch information about Supra Move L1 chain using GPT-3.5 model FOR WHICH you need the api you will get from OpenAI Dashboard
    def fetch_info(self, question):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about Supra Layer 1 Blockchain."},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"Error fetching information: {e}"

# Fund a Supra Move L1 chain account with testnet tokens using the faucet API, I got this from Supra docs so check that out
    def request_faucet_tokens(self, address):
        try:
            response = requests.get(f"https://rpc-testnet.supra.com/rpc/v1/wallet/faucet/{address}")
            if response.status_code == 200:
                return f"Testnet tokens have been sent to your wallet address: {address}"
            else:
                return {"Error": f"Failed to request tokens: {response.status_code}"}
        except Exception as e:
            return {"Error": f"Exception occurred: {e}"}

    def handle_user_input(self, input_text):
        input_text_lower = input_text.lower()
        if "hello" in input_text_lower or "hi" in input_text_lower:
            return "Hello! I am Robbie, here to provide information about Supra Layer 1 Blockchain and help with testnet token funding."
        elif "bye" in input_text_lower or "goodbye" in input_text_lower:
            return "Goodbye! Feel free to ask more about Supra Layer 1 Blockchain anytime."
        elif "fund" in input_text_lower and "account" in input_text_lower:
            return "Please provide your wallet address to receive testnet tokens."
        elif "wallet address" in input_text_lower:
            address = input_text.split("wallet address")[-1].strip()
            return self.request_faucet_tokens(address)
        else:
            return self.fetch_info(input_text)

# Sample usage
if __name__ == "__main__":
    agent = SupraAgent()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Robbie: Goodbye! Feel free to ask more about Supra Layer 1 Blockchain anytime.")
            break
        response = agent.handle_user_input(user_input)
        print(f"Robbie: {response}")
