import os
import telebot

# የቴሌግራም ቦት ቶከን
TOKEN = "9106323264:AAFZw0cRU4teUFarImydtfd5DwIIe-zcuuc"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message,
      "ሰላም! ሚፍታህ ዶሎደር ቦት (Mif Fresh Downloader Bot) አሁን በሰርቨር ላይ 24 ሰዓት"
      " እየሰራ ነው። ማውረድ የሚፈልጉትን ሊንክ ይላኩ!",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  bot.reply_to(
      message, f"ሊንኩ ደርሶኛል: {message.text}\nማውረድ በቅርቡ ይከናወናል!"
  )


if __name__ == "__main__":
  print("Bot is starting...")
  bot.infinity_polling()
  
