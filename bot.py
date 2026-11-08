import os
import telebot
import yt_dlp

# የቦትህን ቶከን እዚህ ጋር "YOUR_BOT_TOKEN_HERE" በሚለው ቦታ ላይ በግልጽ ማስገባት ትችላለህ
# (ለምሳሌ: "7123456789:AAH...") ወይም Render ላይ Environment Variable ላይ BOT_TOKEN ብለህ አስቀምጠው
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message,
      "ሰላም! የ TikTok፣ YouTube፣ Instagram እና ሌሎች ፕላትፎርሞች ቪዲዮ ሊንክ"
      " ላክልኝ፣ አውርጄ አሰጥሃለሁ።",
  )


@bot.message_handler(func=lambda message: True)
def download_video(message):
  url = message.text.strip()
  if not url.startswith("http"):
    bot.reply_to(
        message,
        "⚠️ እባክዎ ትክክለኛ የቪዲዮ ሊንክ (URL) ይላኩ! (ለምሳሌ: TikTok ወይም YouTube"
        " ሊንክ)",
    )
    return

  msg = bot.reply_to(
      message, "⏳ ቪዲዮውን በማውረድ ላይ ነው፣ እባክዎ ትንሽ ይጠብቁ..."
  )

  ydl_opts = {
      "outtmpl": "video.mp4",
      "format": "best",
  }

  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      filename = ydl.prepare_filename(info)

    with open(filename, "rb") as video:
      bot.send_video(message.chat.id, video)

    bot.delete_message(message.chat.id, msg.message_id)

    if os.path.exists(filename):
      os.remove(filename)

  except Exception as e:
    bot.edit_message_text(
        f"❌ ቪዲዮውን ማውረድ አልተቻለም: {e}", message.chat.id, msg.message_id
    )


if __name__ == "__main__":
  bot.infinity_polling()
  
