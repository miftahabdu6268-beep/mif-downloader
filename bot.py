import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot
import yt_dlp

# የቴሌግራም ቦት ቶከን
TOKEN = "9106323264:AAFZw0cRU4teUFarImydtfd5DwIIe-zcuuc"
bot = telebot.TeleBot(TOKEN)

# Render ፖርት እንዲያገኝ የሚረዳ ትንሽ ዌብ ሰርቨር
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Mif Fresh Downloader Bot is running live!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# ዌብ ሰርቨሩን ከበስተጀርባ (Background) ማስጀመር
threading.Thread(target=run_web_server, daemon=True).start()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ሚፍታህ! የ **YouTube፣ Instagram፣ Pinterest እና TikTok** ቪዲዮዎችን ማውረጃ ቦትዎ ዝግጁ ነው። እባክዎ ከየትኛውም ፕላትፎርም የፈለጉትን ሊንክ ይላኩልኝ! 🔗")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    if not url.startswith("http"):
        bot.reply_to(message, "⚠️ እባክዎ ትክክለኛ የቪዲዮ ሊንክ (YouTube, Instagram, Pinterest, TikTok) ይላኩ!")
        return
        
    processing_msg = bot.reply_to(message, "⏳ ቪዲዮው እየወረደ ነው, እባክዎ ትንሽ ይጠብቁ...")
    
    output_template = '%(id)s.%(ext)s'
    ydl_opts = {
        'outtmpl': output_template,
        'format': 'best/bestvideo+bestaudio/best',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
    }
    
    filename = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video_file:
            bot.send_video(message.chat.id, video_file, caption="✅ በተሳካ ሁኔታ ወርዷል!")
            
        # ፋይሉ ከወረደ በኋላ ከሰርቨር መሰረዝ
        if filename and os.path.exists(filename):
            os.remove(filename)
            
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
    except Exception as e:
        if filename and os.path.exists(filename):
            os.remove(filename)
        bot.edit_message_text(f"❌ ማውረድ አልተቻለም: {str(e)[:100]}", message.chat.id, processing_msg.message_id)

# ቦቱን ማስጀመር
if __name__ == "__main__":
    bot.infinity_polling()
    
