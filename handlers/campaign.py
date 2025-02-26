from database import Database

def handler(bot, update, command, txt_args):
    db = Database()
    chat_id = update.message.chat.id
    text = update.message.text
    if command == '/start_campaign':
        response = start_campaign(chat_id, txt_args, db)
    elif command == '/close_campaign':
        response = close_campaign(chat_id, db)

    bot.send_message(chat_id=update.message.chat_id, text=response, parse_mode="Markdown")

def start_campaign(chat_id, text, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    if campaign_id != None or campaign != None:
        return 'There is an active campaign for this group. Close the active campaign before creating a new one'

    db.create_campaign(chat_id, text)
    return "Campaign created successfully!"

def close_campaign(chat_id, db):
    campaign_id, campaign = db.get_campaign(chat_id)
    if campaign_id == None or campaign == None:
        return 'There are no active campaigns for this group'

    db.close_campaign(campaign_id)
    return "Campaign closed successfully!"

if __name__ == "__main__":
    db = Database()
    print(start_campaign('3383241', 'TEst', db))

