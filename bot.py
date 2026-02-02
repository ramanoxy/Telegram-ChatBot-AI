from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from google import genai

BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'

client = genai.Client(api_key=GEMINI_API_KEY)

chat_memory = {}
MAX_HISTORY = 6

async def replay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    
    if user_id not in chat_memory:
        chat_memory[user_id] = []
    
    chat_memory[user_id].append(f"user: {user_message}")
    
    if len(chat_memory[user_id]) > MAX_HISTORY:
        chat_memory[user_id] = chat_memory[user_id][-MAX_HISTORY:]

    full_prompt = (
        "Lu adalah AI yang jadi temen ngobrol yang hangat, perhatian, dan bisa dengerin cerita.\n"
        "Jawaban lu empatik, sedikit romantis (manis tapi sopan), dan ga bertele-tele.\n"
        "Gunakan bahasa santai, kayak ngobrol berdua.\n"
        "Kalo user capek atau sedih, validasi perasaannya dulu sebelum kasih saran.\n\n"
        + "\n".join(chat_memory[user_id])
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )   

    ai_replay = response.candidates[0].content.parts[0].text
    chat_memory[user_id].append(f"AI: {ai_replay}")
    await update.message.reply_text(ai_replay)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, replay))

print("Bot started...")
app.run_polling()
