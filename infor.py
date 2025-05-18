from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# أدخل الـ Token الخاص بك هنا
TOKEN = '7834239805:AAH7JYokRQ3txZbH8KvJgPNl6_xyUr0h8RY'

# دالة تعرض القائمة الرئيسية عند كتابة /start
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("خيار 1", callback_data='option_1')],
        [InlineKeyboardButton("خيار 2", callback_data='option_2')],
        [InlineKeyboardButton("خيار 3", callback_data='option_3')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('اختر خيارًا:', reply_markup=reply_markup)

# دالة لمعالجة الاختيارات
async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    # استجابة لكل خيار مع إرسال الصور عبر الروابط
    if query.data == 'option_1':
        image_url = 'https://w7.pngwing.com/pngs/273/716/png-transparent-bungee-silhouette-thumbnail.png'
        await query.message.reply_photo(photo=image_url, caption="هذه صورة الخيار 1")
    elif query.data == 'option_2':
        image_url = 'https://example.com/image2.jpg'
        await query.message.reply_photo(photo=image_url, caption="هذه صورة الخيار 2")
    elif query.data == 'option_3':
        image_url = 'https://example.com/image3.jpg'
        await query.message.reply_photo(photo=image_url, caption="هذه صورة الخيار 3")

# إعداد البوت وتفعيل الأوامر
def main():
    application = Application.builder().token(TOKEN).build()

    # ربط الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # بدء البوت واستخدام polling
    application.run_polling()

if __name__ == '__main__':
    main()