from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from airtable import Airtable

# Airtable setup
AIRTABLE_BASE = 'jQalyxng3IeZtp'
AIRTABLE_TABLE = 'Message Team'
AIRTABLE_API_KEY = 'patuQ0hWwM12hYFJt.a3138c036c32e3ebcedb93e1ddf88684347dd352c414b63720a9bc83e5744c3d'
airtable = Airtable(jQalyxng3IeZtp, Message Team, patuQ0hWwM12hYFJt.a3138c036c32e3ebcedb93e1ddf88684347dd352c414b63720a9bc83e5744c3d)

# Function to check if an option is already in use
def is_option_in_use(option):
    records = airtable.get_all(filters={'Option': option, 'Status': 'Working'})
    return len(records) > 0

# Start command
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Messenger", callback_data='Messenger')],
        [InlineKeyboardButton("Comment", callback_data='Comment')],
        [InlineKeyboardButton("WhatsApp", callback_data='WhatsApp')],
        [InlineKeyboardButton("Instagram", callback_data='Instagram')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

# Button press handler
def button(update, context):
    query = update.callback_query
    username = query.from_user.username
    option = query.data

    # Check if someone is already working on this option
    if is_option_in_use(option):
        query.answer(f"{username} is already working on this option. Please choose another option.", show_alert=True)
    else:
        # Mark the user as working on this option
        airtable.insert({'Username': username, 'Option': option, 'Status': 'Working'})
        query.answer(f"{username} has started working on the {option}.", show_alert=True)

        # Update the message
        query.edit_message_text(text=f"{username} started working on {option}. Type /end to stop.")

# End command to stop work
def end(update, context):
    username = update.message.from_user.username
    # Get the user’s current work from Airtable
    records = airtable.get_all(filters={'Username': username, 'Status': 'Working'})
    
    if records:
        for record in records:
            option = record['fields']['Option']
            airtable.update(record['id'], {'Status': 'Available'})
            update.message.reply_text(f"{username} stopped working on {option}.")
    else:
        update.message.reply_text("You are not working on any option.")

# Main function to set up the bot
def main():
    updater = Updater("Done! Congratulations on your new bot. You will find it at t.me/manarahmgsbot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
7820196441:AAF1d2RyhbR16G6_qEvsK12pCcl8RGcs_So
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("end", end))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
