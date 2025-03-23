from flask import Flask, request
import telegram
import os
import json

BOT_TOKEN = '7446987073:AAHUuVl_LJj33LQPr9Npm9RPQE9tW8HAev0'
bot = telegram.Bot(token=BOT_TOKEN)

app = Flask(__name__)

UPLOAD_FOLDER = 'screenshots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return '✅ Bridge Server is Live (Advanced Debug Mode)'

@app.route('/webhook', methods=['POST'])
def webhook():
    print("\n🔔 Webhook endpoint triggered!")
    
    try:
        # Print raw headers
        print("\n🧾 Headers:")
        for key, value in request.headers.items():
            print(f"{key}: {value}")

        # Print body as raw text
        print("\n📦 Raw request body:")
        print(request.data.decode('utf-8'))

        # Try to parse as JSON
        data = request.get_json(force=True)

        print("\n📩 [DEBUG] Parsed Telegram Update:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        update = telegram.Update.de_json(data, bot)

        if update.message:
            if update.message.photo:
                photo_file = update.message.photo[-1].get_file()
                file_path = os.path.join(UPLOAD_FOLDER, f'{update.message.message_id}.jpg')
                photo_file.download(file_path)
                print(f'📥 تم حفظ الصورة: {file_path}')
            elif update.message.document:
                print("📄 وصلك document ماشي photo!")
            else:
                print("ℹ️ توصلنا برسالة، لكن ماشي صورة.")
        else:
            print("⚠️ التحديث ما فيهش message...")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

    return 'OK'
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))