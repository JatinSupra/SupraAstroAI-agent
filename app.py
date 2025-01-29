from flask import Flask, request, jsonify, render_template
from supra_agent import SupraAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file where OPENAI_API_KEY is stored
load_dotenv()

# Initialize the Flask application and the agent
app = Flask(__name__)

# Serve static files from the 'static' directory
app.config['STATIC_FOLDER'] = 'static'

agent = SupraAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    print(f"User Input: {user_input}")
    response = agent.handle_user_input(user_input)
    print(f"Agent Response: {response}")
    return jsonify({'response': response})

@app.route('/api/get_tokens', methods=['POST'])
def get_tokens():
    wallet_address = request.json.get('wallet_address')
    print(f"Wallet Address: {wallet_address}")
    response = agent.request_faucet_tokens(wallet_address)
    print(f"Faucet Response: {response}")
    if "Error" not in response:
        return jsonify({'response': f"Testnet tokens have been sent to your wallet address: {wallet_address}"})
    else:
        return jsonify({'response': response['Error']})

if __name__ == '__main__':
    app.run(debug=True)
