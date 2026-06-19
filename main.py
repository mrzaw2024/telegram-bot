import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from datetime import datetime
import json

# Logging setup
logging.basicConfig(level=logging.INFO)

# Token ကို Environment Variable ကနေယူမယ်
TOKEN = os.environ.get("BOT_TOKEN", "8893511874:AAHOtUo8GMZMhfJ75_ceHfFggoUJUIynorY")
USERS_FILE = "users.json"

# ===== User Database =====
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# ===== Bot Handlers =====
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = str(user.id)
    
    users = load_users()
    if user_id not in users:
        users[user_id] = {
            "username": user.username or "No username",
            "first_name": user.first_name,
            "last_name": user.last_name or "",
            "joined_at": datetime.now().isoformat()
        }
        save_users(users)
    
    keyboard = [
        [
            InlineKeyboardButton("💰 လစဥ်ကြေး", callback_data="monthly_fee"),
            InlineKeyboardButton("📞 Admin ဆက်သွယ်ရန်", callback_data="contact_admin")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"👋 မင်္ဂလာပါ {user.first_name}!\n\n"
        f"ကျွန်တော်တို့ရဲ့ Bot ကို ကြိုဆိုပါတယ်။\n"
        f"အောက်ပါ ခလုတ်များထဲက ရွေးချယ်ပါ။"
    )
    
    update.message.reply_text(welcome_text, reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "monthly_fee":
        text = (
            "📋 **လစဥ်ကြေးအသေးစိတ်**\n\n"
            "💰 လစဥ်ကြေး - ၁၀,၀၀၀ ကျပ်\n"
            "📅 ပေးသွင်းရမည့်ရက် - လတိုင်း (၁) ရက်နေ့\n"
            "🏦 ငွေလွှဲရန် - KBZ Pay: 09-123456789\n\n"
            "ကျေးဇူးပြု၍ ငွေလွှဲပြီးပါက ပုံအထောက်အထား တင်ပေးပါ။"
        )
    elif query.data == "contact_admin":
        text = (
            "📞 **Admin ကိုဆက်သွယ်ရန်**\n\n"
            "Admin ကို အောက်ပါနည်းလမ်းများဖြင့် ဆက်သွယ်နိုင်ပါတယ်။\n\n"
            "📱 Telegram: @admin_username\n"
            "📧 Email: admin@example.com\n"
            "📞 Phone: 09-987654321\n\n"
            "ကျေးဇူးပြု၍ မေးမြန်းချက်များကို ရှင်းလင်းစွာ မေးမြန်းပါ။"
        )
    else:
        text = "မသိသော ခလုတ်ဖြစ်ပါတယ်။"
    
    query.edit_message_text(text, parse_mode="Markdown")

def users_command(update: Update, context: CallbackContext):
    user_id = str(update.effective_user.id)
    admin_ids = ["1981957149"]
    
    if user_id not in admin_ids:
        update.message.reply_text("⛔ သင့်တွင် ဤ command ကို သုံးခွင့်မရှိပါ။")
        return
    
    users = load_users()
    if not users:
        update.message.reply_text("📭 User စာရင်း မရှိသေးပါ။")
        return
    
    text = "👥 **User စာရင်း**\n\n"
    for uid, data in users.items():
        text += f"🆔 {uid}\n"
        text += f"👤 {data['first_name']} {data['last_name']}\n"
        text += f"📛 @{data['username']}\n"
        text += f"📅 {data['joined_at']}\n"
        text += "─" * 20 + "\n"
    
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            update.message.reply_text(text[x:x+4096], parse_mode="Markdown")
    else:
        update.message.reply_text(text, parse_mode="Markdown")

def stats_command(update: Update, context: CallbackContext):
    users = load_users()
    total = len(users)
    update.message.reply_text(f"📊 စုစုပေါင်း User အရေအတွက်: {total} ဦး")

def error_handler(update, context):
    logging.error(f"Update {update} caused error {context.error}")

# ===== Main Function =====
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("users", users_command))
    dp.add_handler(CommandHandler("stats", stats_command))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_error_handler(error_handler)
    
    print("🤖 Bot is starting in POLLING mode...")
    print(f"👑 Admin ID: 1981957149")
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
