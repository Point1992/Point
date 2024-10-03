import telebot
from telebot import types

# أدخل الـ token الخاص بك من BotFather
API_TOKEN = '7503221296:AAEx57bGj6_z--M1OQVULt0etCLAAMvOkZI'

bot = telebot.TeleBot(API_TOKEN)

# قاعدة بيانات وهمية لتخزين النقاط
user_points = {}

# دالة للتحقق من عدد النقاط للمستخدم
def get_user_points(user_id):
    return user_points.get(user_id, 0)

# دالة لإضافة نقاط للمستخدم
def add_points(user_id, points):
    if user_id in user_points:
        user_points[user_id] += points
    else:
        user_points[user_id] = points

# الترحيب بالمستخدم الجديد
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"مرحبًا بك! يمكنك تجميع النقاط هنا.\n لديك حاليًا {get_user_points(user_id)} نقاط.")
    
    # عرض الأزرار (مثال: دعوة الأصدقاء)
    markup = types.ReplyKeyboardMarkup(row_width=1)
    invite_button = types.KeyboardButton('دعوة صديق')
    watch_ad_button = types.KeyboardButton('مشاهدة إعلان')
    markup.add(invite_button, watch_ad_button)
    bot.send_message(message.chat.id, "اختر طريقة لتجميع النقاط:", reply_markup=markup)

# التعامل مع الأزرار
@bot.message_handler(func=lambda message: message.text == 'دعوة صديق')
def invite_friend(message):
    user_id = message.from_user.id
    add_points(user_id, 10)  # إضافة 10 نقاط عند دعوة صديق
    bot.reply_to(message, f"تم إضافة 10 نقاط! لديك الآن {get_user_points(user_id)} نقاط.")

@bot.message_handler(func=lambda message: message.text == 'مشاهدة إعلان')
def watch_ad(message):
    user_id = message.from_user.id
    add_points(user_id, 5)  # إضافة 5 نقاط عند مشاهدة إعلان
    bot.reply_to(message, f"تم إضافة 5 نقاط! لديك الآن {get_user_points(user_id)} نقاط.")

# استبدال النقاط بالمكافآت
@bot.message_handler(commands=['redeem'])
def redeem_points(message):
    user_id = message.from_user.id
    points = get_user_points(user_id)
    
    if points >= 50:
        bot.reply_to(message, "تهانينا! يمكنك استبدال 50 نقطة بمكافأة.")
        user_points[user_id] -= 50  # خصم النقاط بعد الاستبدال
    else:
        bot.reply_to(message, f"عذراً، تحتاج إلى 50 نقطة على الأقل. لديك حاليًا {points} نقاط.")

# هذا الكود في الاسفل جديد بالكامل

# قاعدة بيانات لتخزين الدعوات والمستخدمين المدعوين
user_points = {}
user_invitations = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    # التحقق إذا كان المستخدم قادمًا من رابط دعوة
    args = message.text.split()
    
    if len(args) > 1:
        inviter_id = args[1]  # هذا هو معرف المستخدم الذي أرسل الدعوة
        new_user_id = message.from_user.id
        
        # التأكد من أن المستخدم الجديد لم يتم دعوته من قبل
        if new_user_id not in user_invitations:
            # إضافة الدعوة إلى القاموس
            user_invitations[new_user_id] = inviter_id
            
            # إضافة النقاط للمستخدم الذي أرسل الدعوة
            add_points(int(inviter_id), 10)
            bot.reply_to(message, f"تم دعوة هذا المستخدم بواسطة {inviter_id} وحصل على 10 نقاط!")
        else:
            bot.reply_to(message, "لقد تم دعوك من قبل!")
    
    # إرسال رسالة الترحيب المعتادة
    bot.reply_to(message, "مرحبًا بك في البوت! يمكنك تجميع النقاط عبر الدعوات.")

#دعوت الاصدقاء عن طريق رابط خاص بالمستخدم
@bot.message_handler(commands=['invite'])
def send_invite_link(message):
    user_id = message.from_user.id
    invite_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    bot.reply_to(message, f"استخدم هذا الرابط لدعوة أصدقائك: {invite_link}")

#إظهار عدد النقاط:
@bot.message_handler(commands=['points'])
def show_points(message):
    user_id = message.from_user.id
    points = get_user_points(user_id)
    bot.reply_to(message, f"لديك {points} نقاط.")


#عدد الاصدقاء الدعويين
@bot.message_handler(commands=['invites'])
def show_invites(message):
    user_id = message.from_user.id
    invited_users = [user for user, inviter in user_invitations.items() if inviter == str(user_id)]
    bot.reply_to(message, f"لقد دعوت {len(invited_users)} مستخدمين بنجاح.")


def get_bot_info():
    bot_info = bot.get_me()
    print(f"اسم البوت: {bot_info.first_name}")
    print(f"اسم المستخدم: {bot_info.username}")
    print(f"ID البوت: {bot_info.id}")

# استدعاء الدالة
get_bot_info()


# بدء البوت
bot.polling()
