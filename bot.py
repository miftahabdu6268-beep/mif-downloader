import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot

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
    bot.reply_to(message, "ሰላም ሚፍታህ! የ Youtube ቪዲዮ ማውረጃ ቦትዎ በነፃ ሰርቨር ላይ 24 ሰዓት ሙሉ በሰላም እየሰራ ነው። 🔗 ሊንክ ይላኩልኝ!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"ሊንኩ ተቀብሏል: {message.text}\n(ማውረድ የሚጀምርበት ኮድ ይቀጥላል)")

# ቦቱን ማስጀመር
if __name__ == "__main__":
    bot.infinity_polling()
  
