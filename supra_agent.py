import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SupraAgent:
    def __init__(self):
        self.name = 'SupraAgent'
        self.description = 'Provides information about Supra Move L1 chain and helps with testnet token funding.'
        self.personality = 'informative and friendly'
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def fetch_supra_info(self, question):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant knowledgeable about Supra Move L1 chain."},
                    {"role": "user", "content": question}
                ]
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"Error fetching information: {e}"

    def fund_account_with_faucet(self, address):
        try:
            response = requests.get(f"https://rpc-testnet.supra.com/rpc/v1/wallet/faucet/{address}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"Error": f"Failed to fund account: {response.status_code}"}
        except Exception as e:
            return {"Error": f"Exception occurred: {e}"}

    def handle_user_input(self, input_text):
        input_text_lower = input_text.lower()
        if "hello" in input_text_lower or "hi" in input_text_lower:
            return "Hello! I am here to provide information about Supra Move L1 chain and help with testnet token funding."
        elif "bye" in input_text_lower or "goodbye" in input_text_lower:
            return "Goodbye! Feel free to ask more about Supra Move L1 chain anytime."
        elif "fund" in input_text_lower and "account" in input_text_lower:
            address = input_text.split("account")[-1].strip()
            return self.fund_account_with_faucet(address)
        else:
            data = self.fetch_supra_info(input_text)
            return data

# Sample usage
if __name__ == "__main__":
    agent = SupraAgent()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Agent: Goodbye! Feel free to ask more about Supra Move L1 chain anytime.")
            break
        response = agent.handle_user_input(user_input)
        print(f"Agent: {response}")
