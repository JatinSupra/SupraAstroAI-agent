# Supra AI Agent: Robbie

This repository contains an AI agent that provides information about Supra Move L1 chain and helps with testnet token funding using OpenAI's GPT-3.5-turbo model. The agent can be deployed on both Telegram and Twitter.

## Features

- Provides detailed information about Supra Move L1 chain.
- Helps fund accounts with testnet tokens via faucet.
- Deployable on Telegram and Twitter.

## Setup and Usage

### Prerequisites

- Python 3.6 or higher
- OpenAI API key
- Telegram Bot token

### Installation

1. Locate this repository:

```bash
git clone https://github.com/JatinSupra/SupraAstroAI-agent.git
cd SupraAstroAI-agent
```

2. Create a virtual environment and activate it:

```bash
python -m venv supra-env
source supra-env/Scripts/activate  # On Windows
source supra-env/bin/activate   # On macOS and Linux
```

3. Install the required dependencies:

```bash
pip install openai==0.28 requests python-dotenv python-telegram-bot tweepy
```

### Configuration
1. Obtain an API key from OpenAI, a Telegram bot token, and Twitter API keys and tokens.

2. Create a `.env` file in the project directory and add your API keys and tokens:

```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-api-key
```

### Running the AI Agent on Telegram
Run the Telegram bot script:

```bash
python telegram_bot.py
```

## Running the Frontend to Interact with Agent
Run the below script:

```bash
python app.py
```

**NOTE:** To keep your Twitter bot running continuously, you can use a process manager like `npm install -g pm2` and follow Instructions OR deploy it on a cloud service.

## Contributing
Feel free to open issues and submit pull requests for improvements and new features.
