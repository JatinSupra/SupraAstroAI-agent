import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from supra_agent import SupraAgent
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the agent
agent = SupraAgent()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define command handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! I am here to provide information about Supra Move L1 chain and help with testnet token funding.')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('You can ask me about Supra Move L1 chain or request testnet token funding.')

async def get_tokens(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Please provide your wallet address to receive testnet tokens.')

async def handle_wallet_address(update: Update, context: CallbackContext) -> None:
    wallet_address = update.message.text
    response = request_testnet_tokens(wallet_address)
    await update.message.reply_text(response)

def request_testnet_tokens(wallet_address: str) -> str:
    faucet_url = f"https://rpc-testnet.supra.com/rpc/v1/wallet/faucet/{wallet_address}"

    try:
        response = requests.get(faucet_url)
        if response.status_code == 200:
            return f"Testnet tokens have been sent to your wallet address: {wallet_address}"
        else:
            return f"Error: {response.json().get('message', 'Failed to request testnet tokens.')}"
    except Exception as e:
        return f"Error: {str(e)}"

def main() -> None:
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("gettokens", get_tokens))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet_address))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
