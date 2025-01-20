import logging
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Initialize the sheet data (CSV or Excel)
data_file = 'data.csv'  # Change to your file path
df = pd.read_csv(data_file)

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start Command Handler
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! to st thomas info bot Use /help to see how to use the bot.")

# Help Command Handler
def help(update: Update, context: CallbackContext):
    update.message.reply_text("Use /searchdata to search for a person by name, phone, email, or role. Just type the detail you're looking for. Example: 'Achu' or 'john@example.com'.")

# Search Data Command Handler
def search_data(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter the search parameter (Name, Role(Faculty,Student), Email, Phone). Just type the detail you're looking for. Example: 'Achu' or 'john@example.com'.")

# Handle user input and search the sheet
# Handle user input and search the sheet
# Handle user input and search the sheet
def handle_search(update: Update, context: CallbackContext):
    search_query = update.message.text.lower()  # Convert to lower case for case-insensitive search
    result = None

    # Search across multiple fields: Name, Role, Email, Phone
    result = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

    # Check if result is empty
    if result.empty:
        update.message.reply_text("No match found. Please try again with different details.")
    else:
        # Initialize a list to store all matched results
        response = "Found the following matching entries:\n\n"

        # Loop through all matching rows and append them to the response
        for _, details in result.iterrows():
            response += f"Name: {details['Name']}\nEmail: {details['Email']}\nPhone: {details['Phone']}\nRole: {details['Role']}\nGuardian: {details['Guardian']}\n\n"

        update.message.reply_text(response)



# Main function to start the bot
def main():
    # Telegram bot token (replace with your bot's token)
    token = "7779472936:AAHQk5Sgz2filNalLdn7dC_7U7EH14Jkffo"  # Replace with your bot's token

    # Create Updater and pass in your bot's token
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("searchdata", search_data))

    # Message handler to handle search input
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_search))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
