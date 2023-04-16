import telebot
import os
import datetime

my_secret = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(my_secret)

# Kullanıcıları depolamak için bir sözlük oluşturun
users = {}

# Kira tutarı
rent_amount = 2000

# Ödemeleri depolamak için bir liste oluşturun
payments = []

# Hoş geldin mesajı
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.chat.id
    users[user_id] = {
        "name": message.chat.first_name,
        "last_payment": None,
        "paid_amount": 0
    }
    bot.reply_to(message, f"Merhaba {message.chat.first_name}, hoş geldin!")

# Kira ödeme mesajı
@bot.message_handler(commands=['pay'])
def pay_command(message):
    user_id = message.chat.id
    if user_id not in users:
        bot.reply_to(message, "Önce /start komutunu kullanarak başlamalısınız.")
        return

    user_data = users[user_id]
    user_data["last_payment"] = datetime.date.today()
    try:
        amount, description = message.text.split()[1:]
        amount = float(amount)
        user_data["paid_amount"] += amount
        payments.append({
            "user_id": user_id,
            "amount": amount,
            "description": description
        })
        bot.reply_to(message, f"{amount} TL ödemeniz alındı, toplam ödemeniz {user_data['paid_amount']} TL, teşekkür ederiz!")
    except ValueError:
        bot.reply_to(message, "Lütfen ödeme miktarını ve açıklamasını girin. Örnek: /pay 100 market alışverişi")

# Tüm kullanıcıları listeleme işlevi
@bot.message_handler(commands=['list_users'])
def list_users(message):
    user_list = ""
    total_paid = 0
    for user_id, user_data in users.items():
        user_list += f"User ID: {user_id}, Name: {user_data['name']}, Last Payment: {user_data['last_payment']}, Paid Amount: {user_data['paid_amount']} TL\n"
        total_paid += user_data["paid_amount"]
    user_list += f"Toplam kullanıcı sayısı: {len(users)}, Toplam ödeme: {total_paid} TL\n"
    bot.reply_to(message, user_list)

# Aylık kira giderlerini hesaplamak ve kullanıcılara mesaj göndermek için işlev
def calculate_monthly_expenses():
    user_list = ""
    total_paid = 0
    for user_id, user_data in users.items():
        total_paid += user_data["paid_amount"]
    monthly_expenses = rent_amount + total_paid
    user_list += f"Aylık toplam gider: {monthly_expenses} TL, Kira payı: {rent_amount} TL, Ödenen miktar: {total_paid} TL\n"
    for user_id, user_data in users.items():
        user_share = round((rent_amount / len(users)), 2)
        user_balance = user_data["paid_amount"] - user_share
        if user_balance > 0:
            user_list += f"{user_data['name']} {user_balance} TL borçludur.\n"
        elif user_balance < 0:
            user_list += f"{user_data['name']} {-user_balance} TL fazla ödeme yaptı.\n"
        else:
            user_list += f"{user_data['name']} borcu bulunmamaktadır.\n"
    return user_list

# Aylık raporu göndermek için işlev
@bot.message_handler(commands=['monthly_report'])
def monthly_report(message):
    report = calculate_monthly_expenses()
    bot.reply_to(message, report)

# Ödeme özetini görüntülemek için işlev
@bot.message_handler(commands=['summary'])
def summary_command(message):
    user_id = message.chat.id
    user_data = users[user_id]
    summary = f"Toplam ödenen miktar: {user_data['paid_amount']} TL\nSon ödeme tarihi: {user_data['last_payment']}"
    bot.reply_to(message, summary)

bot.polling()