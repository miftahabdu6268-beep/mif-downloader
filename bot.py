import os
import telebot
import yt_dlp

# የቦትህን ቶከን ከ Render Environment Variable ይወስዳል
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! የ YouTube፣ Instagram፣ Pinterest እና TikTok ቪዲዮዎችን ማውረድ እችላለሁ። የምትፈልገውን ሊንክ ላክልኝ! 🔗")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    if not url.startswith('http'):
        bot.reply_to(message, "⚠️ እባክዎ ትክክለኛ የቪዲዮ ሊንክ (URL) ይላኩ! (ለምሳሌ: TikTok፣ YouTube ወይም ሌሎች)")
        return
    
    msg = bot.reply_to(message, "⏳ ቪዲዮውን በማውረድ ላይ ነው፣ እባክዎ ትንሽ ይጠብቁ...")
    
    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
            
        bot.delete_message(message.chat.id, msg.message_id)
        
        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        bot.edit_message_text(f"❌ ቪዲዮውን ማውረድ አልተቻለም: {e}", message.chat.id, msg.message_id)

if __name__ == '__main__':
    bot.infinity_polling()
  
